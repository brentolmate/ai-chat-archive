#!/usr/bin/env python3
"""
AI Chat Archive Import Script

Imports raw AI chat exports (Claude, ChatGPT) into the AI-CHAT-ARCHIVE system.
Supports optional Human OS context integration for intelligent domain and tag detection.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Try to import optional dependencies
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


# ============================================================================
# CONFIGURATION SYSTEM
# ============================================================================

def load_config() -> Dict:
    """
    Load configuration with priority: env vars → config.yaml → defaults

    Priority order:
    1. Environment variables (ARCHIVE_PATH, IMPORT_ROOT, HUMAN_OS_ROOT, etc.)
    2. config/config.yaml (if exists)
    3. Hardcoded defaults
    """
    config = {
        "archive": {"path": "~/AI-CHAT-ARCHIVE"},
        "import_sources": {
            "claude": "~/RAW-AI-CHAT-IMPORT/claude export/conversations.json",
            "chatgpt": "~/RAW-AI-CHAT-IMPORT/CHAT GPT Archive/conversations.json"
        },
        "human_os": {
            "enabled": True,
            "path": "~/Human",
            "domains": ["brent", "gal", "loopwalker", "pulsekeeper", "shadow-institute", "unlimited-band"]
        },
        "domains": {
            "default": "system",
            "custom": {
                "@loopwalker": ["music", "song", "loopwalker", "shadow work", "frequency", "audio", "lyrics", "melody"],
                "@pulsekeeper": ["heart", "coherence", "adhd", "2e", "frequency", "nervous system", "regulation"],
                "@shadow-institute": ["dyslexia", "twice-exceptional", "2e", "gifted", "neurodivergent", "learning difference"],
                "@unlimited-band": ["band", "collaboration", "music group", "bandmate"],
                "@brent": ["hyperfocus", "dyslexia", "pattern recognition", "brand", "positioning", "website"],
                "@gal": ["connection", "outreach", "networking", "crm", "warm", "dm", "comment"],
                "@system": ["sprint", "workflow", "process", "system", "automation", "skill"]
            }
        },
        "anthropic": {
            "api_key_env": "ANTHROPIC_API_KEY",
            "model": "claude-3-haiku-20240307",
            "max_tokens_summary": 200,
            "max_tokens_outputs": 300
        }
    }

    # 1. Try to load from config.yaml
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    if config_path.exists() and YAML_AVAILABLE:
        try:
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    # Deep merge user config with defaults
                    for section in user_config:
                        if section in config and isinstance(config[section], dict):
                            config[section].update(user_config[section])
                        else:
                            config[section] = user_config[section]
        except Exception as e:
            print(f"Warning: Error loading config.yaml: {e}")

    # 2. Override with environment variables
    if os.environ.get("ARCHIVE_PATH"):
        config["archive"]["path"] = os.environ["ARCHIVE_PATH"]
    if os.environ.get("IMPORT_ROOT"):
        import_root = Path(os.environ["IMPORT_ROOT"])
        config["import_sources"]["claude"] = str(import_root / "claude export/conversations.json")
        config["import_sources"]["chatgpt"] = str(import_root / "CHAT GPT Archive/conversations.json")
    if os.environ.get("HUMAN_OS_ROOT"):
        config["human_os"]["path"] = os.environ["HUMAN_OS_ROOT"]
    if os.environ.get("HUMAN_OS_ENABLED"):
        config["human_os"]["enabled"] = os.environ["HUMAN_OS_ENABLED"].lower() == "true"

    return config


# Load configuration at module level
CONFIG = load_config()

# Expand paths (handle ~)
ARCHIVE_ROOT = Path(CONFIG["archive"]["path"]).expanduser()
IMPORT_ROOT = Path(CONFIG["import_sources"]["claude"]).parent.parent  # Get parent of claude export/
HUMAN_OS_ROOT = Path(CONFIG["human_os"]["path"]).expanduser() if CONFIG["human_os"]["enabled"] else None

# Domain keywords from config
DOMAIN_KEYWORDS = CONFIG["domains"]["custom"]

# Month names for folder structure
MONTH_NAMES = {
    1: "01-January", 2: "02-February", 3: "03-March", 4: "04-April",
    5: "05-May", 6: "06-June", 7: "07-July", 8: "08-August",
    9: "09-September", 10: "10-October", 11: "11-November", 12: "12-December"
}


# ============================================================================
# CLAUDE API FUNCTIONS
# ============================================================================

def generate_summary_with_claude(title: str, transcript: str, domain: str, api_key: str) -> str:
    """Generate a high-quality summary using Claude API."""
    if not ANTHROPIC_AVAILABLE:
        return generate_summary(title, transcript, domain)

    try:
        client = anthropic.Anthropic(api_key=api_key)

        # Get first part of transcript for context (limit to avoid token issues)
        transcript_preview = transcript[:8000]

        prompt = f"""Analyze this AI conversation and generate a concise 2-3 sentence summary.

Title: {title}
Domain: {domain}

Transcript:
{transcript_preview}

Focus on:
1. What was discussed/main topic
2. Any decisions made or key insights
3. Relevance to the domain

Keep it to 2-3 sentences maximum. Be specific and concise."""

        model = CONFIG["anthropic"]["model"]
        max_tokens = CONFIG["anthropic"]["max_tokens_summary"]

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip()

    except Exception as e:
        print(f"  Warning: Claude API error ({e}), falling back to rule-based summary")
        return generate_summary(title, transcript, domain)


def extract_key_outputs_with_claude(transcript: str, api_key: str) -> List[str]:
    """Extract key outputs using Claude API."""
    if not ANTHROPIC_AVAILABLE:
        return extract_key_outputs(transcript)

    try:
        client = anthropic.Anthropic(api_key=api_key)

        # Get first part of transcript
        transcript_preview = transcript[:8000]

        prompt = f"""Extract 2-3 key outputs, decisions, or insights from this conversation.

Transcript:
{transcript_preview}

Return as a bulleted list with one line per item. Focus on:
- Decisions made
- Action items
- Key insights
- Files/code created
- Agreements reached

Format:
- First key point
- Second key point
- Third key point"""

        model = CONFIG["anthropic"]["model"]
        max_tokens = CONFIG["anthropic"]["max_tokens_outputs"]

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.content[0].text.strip()
        # Parse into list
        outputs = [line.strip() for line in result.split('\n') if line.strip().startswith('-')]
        return outputs[:3] if outputs else ["- [Key insights from this conversation]"]

    except Exception as e:
        print(f"  Warning: Claude API error ({e}), falling back to rule-based extraction")
        return extract_key_outputs(transcript)


# ============================================================================
# CONTEXT LOADING
# ============================================================================

def load_context() -> Dict:
    """Load context from Human OS for intelligent tagging."""
    context = {
        "sprint": {},
        "domains": {},
        "active_domains": [],
        "sprint_priorities": []
    }

    # Skip if Human OS is disabled
    if not CONFIG["human_os"]["enabled"] or not HUMAN_OS_ROOT:
        return context

    # Load Sprint.md
    sprint_path = HUMAN_OS_ROOT / "SYSTEM/00-Index/Sprint.md"
    if sprint_path.exists():
        content = sprint_path.read_text()
        context["sprint"]["raw"] = content
        # Extract flagship
        flagship_match = re.search(r'\*\*Flagship:\*\*\s*(.+)', content)
        if flagship_match:
            context["sprint"]["flagship"] = flagship_match.group(1).strip()

    # Load domain INDEX files
    domains_to_load = CONFIG["human_os"].get("domains", [])
    for domain_name in domains_to_load:
        index_path = HUMAN_OS_ROOT / f"@{domain_name}-INDEX.md"
        if index_path.exists():
            content = index_path.read_text()
            # Extract active projects from NOW section
            now_match = re.search(r'## NOW\s*\n(.+?)##', content, re.DOTALL)
            active_projects = []
            if now_match:
                for line in now_match.group(1).split('\n'):
                    if '|' in line and '**' in line:
                        project_match = re.search(r'\*\*(.+?)\*\*', line)
                        if project_match:
                            active_projects.append(project_match.group(1).strip())
            context["domains"][f"@{domain_name}"] = {
                "active_projects": active_projects,
                "raw": content
            }

    return context


# ============================================================================
# RULE-BASED ANALYSIS
# ============================================================================

def generate_summary(title: str, transcript: str, domain: str) -> str:
    """Generate a 2-3 sentence summary of the conversation."""
    # Get first few exchanges to understand the topic
    lines = transcript.split('\n')[:20]
    early_content = ' '.join(lines)

    # Extract what the conversation was about
    summary_parts = []

    # First sentence: what was discussed
    if title and title.strip():
        summary_parts.append(f"Conversation about {title.lower()}.")
    else:
        # Try to infer from content
        if "music" in early_content.lower() or "song" in early_content.lower():
            summary_parts.append("Conversation about music creation or lyrics.")
        elif "code" in early_content.lower() or "script" in early_content.lower():
            summary_parts.append("Technical discussion about code or automation.")
        elif "brand" in early_content.lower() or "positioning" in early_content.lower():
            summary_parts.append("Discussion about brand strategy or positioning.")
        else:
            summary_parts.append("General conversation on various topics.")

    # Second sentence: domain context
    domain_names = {
        "@loopwalker": "music and creative work",
        "@pulsekeeper": "heart coherence and ADHD",
        "@shadow-institute": "2E and dyslexia",
        "@unlimited-band": "music collaboration",
        "@brent": "brand and personal systems",
        "@gal": "connections and outreach",
        "@system": "systems and workflows"
    }
    domain_desc = domain_names.get(domain, "general topics")
    summary_parts.append(f"Related to {domain_desc}.")

    # Third sentence: key themes (if we can extract them)
    themes = []
    theme_keywords = {
        "brand strategy": ["brand", "positioning", "offer"],
        "music creation": ["song", "lyrics", "melody"],
        "technical implementation": ["code", "script", "function"],
        "workflow": ["workflow", "process", "system"],
        "2E awareness": ["2e", "dyslexia", "neurodivergent"]
    }

    for theme, keywords in theme_keywords.items():
        if any(kw in early_content.lower() for kw in keywords):
            themes.append(theme)
            if len(themes) >= 2:
                break

    if themes:
        summary_parts.append(f"Key themes: {', '.join(themes)}.")

    return ' '.join(summary_parts)


def extract_key_outputs(transcript: str) -> List[str]:
    """Extract key outputs from the conversation."""
    outputs = []

    # Look for decision markers
    decision_markers = [
        r"decided to",
        r"will",
        r"going to",
        r"plan to",
        r"final(?:ized|ized)?"
    ]

    lines = transcript.split('\n')
    for line in lines:
        line_lower = line.lower()
        for marker in decision_markers:
            if marker in line_lower and len(line) < 200:
                # Clean up the line
                cleaned = re.sub(r'\*\*(.+?):\*\*', '', line).strip()
                if len(cleaned) > 10 and len(cleaned) < 150:
                    outputs.append(f"- {cleaned[:100]}")
                    if len(outputs) >= 3:
                        break
        if len(outputs) >= 3:
            break

    # If no decisions found, extract key points from assistant responses
    if not outputs:
        for line in lines:
            if "**Assistant:**" in line or "**assistant**:" in line.lower():
                # Get the next few lines
                idx = lines.index(line)
                for next_line in lines[idx+1:idx+4]:
                    if next_line.strip() and not next_line.startswith("**"):
                        cleaned = next_line.strip()
                        if len(cleaned) > 20 and len(cleaned) < 150:
                            outputs.append(f"- {cleaned[:100]}")
                            if len(outputs) >= 3:
                                break
                if len(outputs) >= 3:
                    break

    return outputs[:3] if outputs else ["- [Key decisions or outputs from this conversation]"]


def sanitize_topic(text: str) -> str:
    """Convert text to a hyphenated topic name."""
    # Remove special chars, lowercase, hyphenate
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'\s+', '-', text.strip())
    # Limit to 4 words
    words = text.split('-')[:4]
    result = '-'.join(words)
    # Handle empty titles
    if not result or result == '-':
        return "untitled-conversation"
    return result


def detect_domain(content: str, title: str = "") -> Optional[str]:
    """Detect domain from content and title using keyword matching."""
    combined = f"{title} {content}".lower()

    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in combined)
        if score > 0:
            scores[domain] = score

    if scores:
        return max(scores, key=scores.get)

    # Return default domain from config
    default_domain = CONFIG["domains"].get("default", "system")
    return f"@{default_domain}" if not default_domain.startswith("@") else default_domain


def generate_tags(content: str, title: str, context: Dict) -> List[str]:
    """Generate tags from content and context."""
    tags = set()
    combined = f"{title} {content}".lower()

    # Add domain-related tags
    detected_domain = detect_domain(content, title)
    if detected_domain:
        tags.add(detected_domain.replace("@", ""))

    # Add sprint-related tags (if Human OS is enabled)
    if CONFIG["human_os"]["enabled"] and "flagship" in context["sprint"]:
        flagship = context["sprint"]["flagship"].lower()
        if "brand" in flagship:
            tags.add("brand")
        if "visual" in flagship:
            tags.add("visual-direction")

    # Add common topic tags
    topic_keywords = {
        "positioning": ["positioning", "brand strategy", "offer"],
        "music": ["song", "lyrics", "melody", "music", "audio"],
        "code": ["python", "javascript", "function", "script", "code"],
        "2e": ["2e", "dyslexia", "twice-exceptional", "neurodivergent"],
        "shadow-work": ["shadow", "integration", "shadow-work"],
        "website": ["website", "site", "landing page", "domain"]
    }

    for tag, keywords in topic_keywords.items():
        if any(kw in combined for kw in keywords):
            tags.add(tag)

    return sorted(list(tags))[:5]  # Max 5 tags


# ============================================================================
# CONVERSION FUNCTIONS
# ============================================================================

def parse_claude_conversation(chat: Dict, context: Dict) -> Dict:
    """Parse a Claude conversation from JSON."""
    # Extract date
    created_at = chat.get("created_at", "")
    try:
        if isinstance(created_at, str):
            date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        else:
            date = datetime.now()
    except:
        date = datetime.now()

    # Extract title and content
    title = chat.get("name", "Untitled")
    messages = chat.get("chat_messages", [])

    # Build transcript
    transcript_parts = []
    for msg in messages:
        sender = msg.get("sender", "unknown")
        text = msg.get("text", "")
        if text:
            transcript_parts.append(f"**{sender.title()}:** {text}")

    transcript = "\n\n".join(transcript_parts)

    # Generate metadata
    topic = sanitize_topic(title)
    domain = detect_domain(transcript, title)
    tags = generate_tags(transcript, title, context)

    return {
        "date": date,
        "title": title,
        "topic": topic,
        "domain": domain,
        "tags": tags,
        "ai": "claude",
        "transcript": transcript
    }


def parse_chatgpt_conversation(chat: Dict, context: Dict) -> Optional[Dict]:
    """Parse a ChatGPT conversation from JSON."""
    # ChatGPT format is complex - extract from mapping structure
    title = chat.get("title", "Untitled")
    create_time = chat.get("create_time", 0)

    try:
        date = datetime.fromtimestamp(create_time)
    except:
        return None

    # Extract messages from mapping
    mapping = chat.get("mapping", {})
    transcript_parts = []

    for node_id, node in mapping.items():
        message = node.get("message")
        if message:
            author = message.get("author", {})
            role = author.get("role", "unknown")
            content = message.get("content", {})

            if content.get("content_type") == "text":
                parts = content.get("parts", [])
                for part in parts:
                    if isinstance(part, str) and part.strip():
                        transcript_parts.append(f"**{role.title()}:** {part}")

    if not transcript_parts:
        return None

    transcript = "\n\n".join(transcript_parts)

    # Generate metadata
    topic = sanitize_topic(title)
    domain = detect_domain(transcript, title)
    tags = generate_tags(transcript, title, context)

    return {
        "date": date,
        "title": title,
        "topic": topic,
        "domain": domain,
        "tags": tags,
        "ai": "chatgpt",
        "transcript": transcript
    }


def create_archive_entry(data: Dict, use_claude_api: bool = False, api_key: str = None) -> Path:
    """Create a markdown file in the archive."""
    year = data["date"].year
    month = MONTH_NAMES[data["date"].month]
    day = data["date"].day

    # Create folder structure
    folder = ARCHIVE_ROOT / str(year) / month
    folder.mkdir(parents=True, exist_ok=True)

    # Generate filename
    filename = f"{year:04d}-{data['date'].month:02d}-{day:02d}-{data['topic']}.md"
    filepath = folder / filename

    # Handle duplicates
    counter = 1
    while filepath.exists():
        filename = f"{year:04d}-{data['date'].month:02d}-{day:02d}-{data['topic']}-{counter}.md"
        filepath = folder / filename
        counter += 1

    # Generate summary and key outputs
    if use_claude_api and api_key:
        summary = generate_summary_with_claude(data['title'], data['transcript'], data['domain'], api_key)
        key_outputs = extract_key_outputs_with_claude(data['transcript'], api_key)
    else:
        summary = generate_summary(data['title'], data['transcript'], data['domain'])
        key_outputs = extract_key_outputs(data['transcript'])
    key_outputs_text = '\n'.join(key_outputs)

    # Create markdown content
    content = f"""---
date: {data['date'].strftime('%Y-%m-%d')}
topic: {data['title']}
domains: ["{data['domain']}"]
tags: {json.dumps(data['tags'])}
ai: {data['ai']}
---

# {data['title']}

**Date:** {data['date'].strftime('%Y-%m-%d')}
**Source:** {data['ai'].title()}

## Summary
{summary}

## Key Outputs
{key_outputs_text}

## Transcript

{data['transcript']}
"""

    filepath.write_text(content)
    return filepath


def update_index(entry: Dict, filepath: Path):
    """Update INDEX.md with new entry."""
    index_path = ARCHIVE_ROOT / "INDEX.md"
    if not index_path.exists():
        return

    content = index_path.read_text()

    # Find the year section
    year = entry["date"].year
    month_name = MONTH_NAMES[entry["date"].month].split('-')[1]  # Get month name

    # Add entry (simplified - in production would parse and insert properly)
    new_entry = f"- **{entry['date'].strftime('%Y-%m-%d')}** — [{entry['title']}]({filepath.relative_to(ARCHIVE_ROOT)}) — {', '.join(entry['tags'])}\n"

    # For now, just append to a comment at top noting update needed
    # In production, would properly parse and insert
    pass


# ============================================================================
# MAIN IMPORT FUNCTION
# ============================================================================

def main():
    """Main import function."""
    import argparse

    parser = argparse.ArgumentParser(description="Import AI chat conversations to archive")
    parser.add_argument("--sample", action="store_true", help="Run in sample mode")
    parser.add_argument("--count", type=int, default=5, help="Number of conversations for sample mode")
    parser.add_argument("--source", choices=["claude", "chatgpt", "all"], default="all", help="Which source to import")
    parser.add_argument("--claude-api", action="store_true", help="Use Claude API for higher-quality summaries")
    parser.add_argument("--api-key", type=str, help="Anthropic API key (or set ANTHROPIC_API_KEY env var)")
    args = parser.parse_args()

    # Get API key
    api_key_env = CONFIG["anthropic"]["api_key_env"]
    api_key = args.api_key or os.environ.get(api_key_env)
    use_claude_api = args.claude_api

    if use_claude_api:
        if not api_key:
            print(f"Error: --claude-api requires {api_key_env} environment variable or --api-key parameter")
            sys.exit(1)
        if not ANTHROPIC_AVAILABLE:
            print("Error: anthropic package not installed. Run: pip install anthropic")
            sys.exit(1)
        print(f"Claude API enabled (using {CONFIG['anthropic']['model']} for summaries)")

    # Display configuration
    print(f"Archive location: {ARCHIVE_ROOT}")
    print(f"Human OS integration: {'Enabled' if CONFIG['human_os']['enabled'] else 'Disabled'}")

    if CONFIG["human_os"]["enabled"]:
        print("Loading context from Human OS...")
        context = load_context()
        print(f"  Flagship: {context['sprint'].get('flagship', 'N/A')}")
        print(f"  Domains loaded: {len(context['domains'])}")
    else:
        print("Skipping Human OS context (using fallback keyword detection)")
        context = {"sprint": {}, "domains": {}, "active_domains": [], "sprint_priorities": []}

    imported = 0
    errors = 0

    # Process Claude exports
    if args.source in ["claude", "all"]:
        claude_path = Path(CONFIG["import_sources"]["claude"]).expanduser()
        if claude_path.exists():
            print(f"\nProcessing Claude exports from {claude_path}...")

            try:
                with open(claude_path, 'r') as f:
                    claude_chats = json.load(f)

                chats_to_process = claude_chats[:args.count] if args.sample else claude_chats

                for i, chat in enumerate(chats_to_process):
                    try:
                        data = parse_claude_conversation(chat, context)
                        filepath = create_archive_entry(data, use_claude_api, api_key)
                        update_index(data, filepath)

                        if args.sample or i % 100 == 0:
                            print(f"  [{i+1}/{len(chats_to_process)}] {data['title'][:50]} -> {filepath.relative_to(ARCHIVE_ROOT)}")

                        imported += 1
                    except Exception as e:
                        errors += 1
                        if args.sample:
                            print(f"  Error processing chat {i}: {e}")

            except json.JSONDecodeError as e:
                print(f"  Error parsing Claude JSON: {e}")
        else:
            print(f"\nClaude export not found: {claude_path}")
            print(f"  (Check import_sources.claude in config/config.yaml)")

    # Process ChatGPT exports
    if args.source in ["chatgpt", "all"]:
        chatgpt_path = Path(CONFIG["import_sources"]["chatgpt"]).expanduser()
        if chatgpt_path.exists():
            print(f"\nProcessing ChatGPT exports from {chatgpt_path}...")

            try:
                with open(chatgpt_path, 'r') as f:
                    chatgpt_chats = json.load(f)

                chats_to_process = chatgpt_chats[:args.count] if args.sample else chatgpt_chats

                for i, chat in enumerate(chats_to_process):
                    try:
                        data = parse_chatgpt_conversation(chat, context)
                        if data:
                            filepath = create_archive_entry(data, use_claude_api, api_key)
                            update_index(data, filepath)

                            if args.sample or i % 100 == 0:
                                print(f"  [{i+1}/{len(chats_to_process)}] {data['title'][:50]} -> {filepath.relative_to(ARCHIVE_ROOT)}")

                            imported += 1
                    except Exception as e:
                        errors += 1
                        if args.sample:
                            print(f"  Error processing chat {i}: {e}")

            except json.JSONDecodeError as e:
                print(f"  Error parsing ChatGPT JSON: {e}")
        else:
            print(f"\nChatGPT export not found: {chatgpt_path}")
            print(f"  (Check import_sources.chatgpt in config/config.yaml)")

    print(f"\n{'='*60}")
    print(f"Import complete!")
    print(f"  Imported: {imported}")
    print(f"  Errors: {errors}")
    print(f"  Mode: {'Sample' if args.sample else 'Batch'}")
    print(f"{'='*60}")

    if args.sample:
        print("\nPlease review the imported files and verify:")
        print("  1. File naming makes sense")
        print("  2. Topic extraction is accurate")
        print("  3. Domain detection is correct")
        print("  4. Tags are relevant")
        print("\nIf satisfied, run without --sample to import all conversations.")


if __name__ == "__main__":
    main()
