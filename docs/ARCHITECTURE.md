# AI Chat Archive Architecture

## System Overview

The AI Chat Archive is a Python-based system for importing, organizing, and searching AI conversations from Claude and ChatGPT.

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Chat Archive System                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────┐   │
│  │   Claude    │    │   ChatGPT    │    │  Human OS   │   │
│  │   Exports   │    │   Exports    │    │ (Optional)  │   │
│  └──────┬──────┘    └──────┬───────┘    └──────┬──────┘   │
│         │                  │                    │           │
│         └──────────────────┴────────────────────┘           │
│                           │                                 │
│                    ┌──────▼──────┐                          │
│                    │ import-chats│                          │
│                    │    .py      │                          │
│                    └──────┬──────┘                          │
│                           │                                 │
│         ┌─────────────────┼─────────────────┐               │
│         │                 │                 │               │
│    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐          │
│    │  Parse  │      │ Detect  │      │ Generate│          │
│    │   JSON  │      │ Domain  │      │  Tags   │          │
│    └────┬────┘      └────┬────┘      └────┬────┘          │
│         │                │                │                 │
│         └────────────────┴────────────────┘                 │
│                           │                                 │
│                    ┌──────▼──────┐                          │
│                    │ Create      │                          │
│                    │ Markdown    │                          │
│                    └──────┬──────┘                          │
│                           │                                 │
│                    ┌──────▼──────┐                          │
│                    │   Archive   │                          │
│                    │  YYYY/MM/   │                          │
│                    └─────────────┘                          │
│                                                           │
├─────────────────────────────────────────────────────────────┤
│  Configuration: config.yaml | Environment Variables         │
│  Skills: /archive | /archive-query                         │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Import Script (`import-chats.py`)

**Purpose:** Convert raw JSON exports into organized markdown files.

**Key Functions:**
- `load_config()` - Load configuration with priority cascade
- `parse_claude_conversation()` - Parse Claude JSON format
- `parse_chatgpt_conversation()` - Parse ChatGPT JSON format
- `detect_domain()` - Auto-detect domain from content
- `generate_tags()` - Extract relevant tags
- `create_archive_entry()` - Write markdown file

**Configuration Priority:**
1. Environment variables
2. `config/config.yaml`
3. Hardcoded defaults

### 2. Configuration System

**Location:** `config/config.yaml`

**Sections:**
- `archive` - Output location
- `import_sources` - Input file locations
- `human_os` - Optional Human OS integration
- `domains` - Domain keyword mappings
- `anthropic` - Claude API settings

### 3. Domain Detection

**Method:** Keyword matching with scoring

**Algorithm:**
```python
for domain, keywords in DOMAIN_KEYWORDS.items():
    score = sum(1 for kw in keywords if kw.lower() in content)
    if score > 0:
        scores[domain] = score

return max(scores, key=scores.get) if scores else default_domain
```

**Fallback:** Uses default domain from config if no match.

### 4. Tag Generation

**Sources:**
1. Domain name (from domain detection)
2. Sprint priorities (from Human OS, if enabled)
3. Topic keywords (predefined mappings)

**Maximum:** 5 tags per conversation

### 5. Claude API Integration (Optional)

**Purpose:** Generate higher-quality summaries and key outputs

**Model:** Claude 3 Haiku (configurable)

**Functions:**
- `generate_summary_with_claude()` - 2-3 sentence summaries
- `extract_key_outputs_with_claude()` - Bullet point extraction

**Fallback:** Rule-based generation if API unavailable

## File Format

### Markdown Structure

```markdown
---
date: 2026-01-16
topic: Loopwalker Positioning
domains: ["loopwalker"]
tags: ["positioning", "brand", "offer", "loopwalker"]
ai: claude
---

# Loopwalker Positioning

**Date:** 2026-01-16
**Source:** Claude

## Summary
[2-3 sentence overview of conversation]

## Key Outputs
- Decision 1
- Decision 2
- Decision 3

## Transcript
[Full conversation content]
```

### Directory Structure

```
archive/
├── INDEX.md
├── 2026/
│   ├── 01-January/
│   │   ├── 2026-01-16-topic-1.md
│   │   └── 2026-01-17-topic-2.md
│   └── 02-February/
└── 2027/
```

## Claude Code Skills

### /archive

**Purpose:** Automatically archive current conversation

**Usage:** `/archive [topic] [domain] [tags]`

**Actions:**
1. Capture current conversation
2. Generate summary and key outputs
3. Create markdown file with frontmatter
4. Update INDEX.md
5. Return file path

### /archive-query

**Purpose:** Search archived conversations

**Usage:** `/archive-query [query]`

**Query Types:**
- Domain: `@loopwalker`, `@brent`, etc.
- Time: "December", "last week"
- Topic: "positioning", "music"
- Complex: "@loopwalker positioning last month"

## Human OS Integration (Optional)

### What It Reads

1. **Sprint.md** - Current sprint flagship
2. **@domain-INDEX.md** - Active projects per domain

### How It Helps

- Adds sprint-related tags (e.g., "brand" if flagship is brand-focused)
- Provides context for domain detection
- Enriches tag generation

### Disabling

Set `human_os.enabled: false` in config.yaml

## Error Handling

### Import Failures

**Strategy:** Continue processing, log errors, report at end

```python
for chat in chats:
    try:
        data = parse(chat, context)
        create_entry(data)
        imported += 1
    except Exception as e:
        errors += 1
        if args.sample:
            print(f"Error: {e}")
```

### Missing Files

**Behavior:** Skip with warning, don't fail

```
Claude export not found: ~/path/to/conversations.json
  (Check import_sources.claude in config/config.yaml)
```

### Invalid JSON

**Behavior:** Catch `JSONDecodeError`, report, continue

## Performance

### Batch Processing

**Progress Reporting:** Every 100 files (or all in sample mode)

```python
if args.sample or i % 100 == 0:
    print(f"[{i}/{total}] {title[:50]} -> {filepath}")
```

### Large Exports

**Transcript Preview:** Limited to 8000 chars for Claude API

**Reason:** Avoid token limits, reduce API costs

## Extensibility

### Adding Custom Domains

Edit `config/config.yaml`:

```yaml
domains:
  custom:
    "@mydomain":
      - keyword1
      - keyword2
      - keyword3
```

### Adding Custom Tag Keywords

Edit `generate_tags()` function in `import-chats.py`

### Changing Output Format

Modify `create_archive_entry()` function

## Testing

### Unit Tests

**Location:** `tests/test_import.py`

**Coverage:**
- Config loading
- Topic sanitization
- Domain detection
- Tag generation

### Fixtures

**Location:** `tests/fixtures/`

- `sample-claude-export.json`
- `sample-chatgpt-export.json`
- `expected-output.md`

### CI/CD

**GitHub Actions:** `.github/workflows/test-import.yml`

**Matrix:** Python 3.8-3.11

---

*Last updated: 2026-02-10*
