# Configuration Guide

Complete reference for configuring your AI Chat Archive.

## Configuration File

**Location:** `config/config.yaml` (created by setup wizard)

**Priority:**
1. Environment variables (highest)
2. `config/config.yaml`
3. Hardcoded defaults (lowest)

## Full Configuration Example

```yaml
# Archive location
archive:
  path: ~/AI-CHAT-ARCHIVE

# Import source locations
import_sources:
  claude: ~/RAW-AI-CHAT-IMPORT/claude export/conversations.json
  chatgpt: ~/RAW-AI-CHAT-IMPORT/CHAT GPT Archive/conversations.json

# Human OS integration (optional)
human_os:
  enabled: true
  path: ~/Human
  domains:
    - loopwalker
    - brent
    - gal
    - pulsekeeper
    - shadow-institute
    - unlimited-band

# Domain keyword mapping
domains:
  default: system
  custom:
    "@loopwalker":
      - music
      - song
      - loopwalker
      - shadow work
    "@brent":
      - brand
      - positioning
      - website

# Claude API settings (optional)
anthropic:
  api_key_env: ANTHROPIC_API_KEY
  model: claude-3-haiku-20240307
  max_tokens_summary: 200
  max_tokens_outputs: 300
```

## Configuration Sections

### Archive

Controls where conversations are stored.

```yaml
archive:
  path: ~/AI-CHAT-ARCHIVE
```

**Options:**
- `path` - Absolute path or `~` for home directory

**Environment variable:** `ARCHIVE_PATH`

### Import Sources

Locations of your AI chat export files.

```yaml
import_sources:
  claude: ~/RAW-AI-CHAT-IMPORT/claude export/conversations.json
  chatgpt: ~/RAW-AI-CHAT-IMPORT/CHAT GPT Archive/conversations.json
```

**Options:**
- `claude` - Path to Claude conversations.json
- `chatgpt` - Path to ChatGPT conversations.json

**Environment variable:** `IMPORT_ROOT` (sets parent directory)

### Human OS

Optional integration with Human OS for enhanced tagging.

```yaml
human_os:
  enabled: true
  path: ~/Human
  domains:
    - loopwalker
    - brent
    - gal
```

**Options:**
- `enabled` - `true` or `false`
- `path` - Path to Human OS root
- `domains` - List of domains to load

**Environment variables:**
- `HUMAN_OS_ROOT` - Override path
- `HUMAN_OS_ENABLED` - Override enabled state ("true"/"false")

**What it does:**
- Reads `SYSTEM/00-Index/Sprint.md` for flagship goal
- Reads `@domain-INDEX.md` files for active projects
- Adds sprint-related tags automatically

### Domains

Defines domain keywords for auto-detection.

```yaml
domains:
  default: system
  custom:
    "@loopwalker":
      - music
      - song
      - audio
```

**Options:**
- `default` - Fallback domain when no match found
- `custom` - Map of domain names to keyword lists

**How it works:**
1. Counts keyword matches in conversation
2. Assigns domain with highest score
3. Uses default if no matches

### Anthropic

Optional Claude API integration for better summaries.

```yaml
anthropic:
  api_key_env: ANTHROPIC_API_KEY
  model: claude-3-haiku-20240307
  max_tokens_summary: 200
  max_tokens_outputs: 300
```

**Options:**
- `api_key_env` - Environment variable name for API key
- `model` - Claude model to use
- `max_tokens_summary` - Max tokens for summaries
- `max_tokens_outputs` - Max tokens for key outputs

**Environment variable:** `ANTHROPIC_API_KEY` (or custom name from config)

**Usage:**
```bash
export ANTHROPIC_API_KEY="your-key-here"
python3 bin/import-chats.py --claude-api
```

## Environment Variables

Override configuration without editing files:

```bash
# Archive location
export ARCHIVE_PATH="~/My-Archive"

# Import sources
export IMPORT_ROOT="~/My-Imports"

# Human OS
export HUMAN_OS_ROOT="~/KnowledgeBase"
export HUMAN_OS_ENABLED="true"

# Claude API
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Path Expansion

The system supports these path formats:

```yaml
# Tilde expansion (recommended)
archive:
  path: ~/AI-CHAT-ARCHIVE

# Absolute paths
archive:
  path: /Users/username/AI-CHAT-ARCHIVE

# Relative paths (from project root)
archive:
  path: ./archive
```

**Tilde (`~`) is recommended** for portability across systems.

## Validation

Test your configuration:

```bash
# Check if config is valid
python3 -c "import yaml; yaml.safe_load(open('config/config.yaml'))"

# Test import with dry run
python3 bin/import-chats.py --sample --count 1
```

## Common Patterns

### Portable Configuration

Use tilde paths for cross-system compatibility:

```yaml
archive:
  path: ~/AI-CHAT-ARCHIVE

import_sources:
  claude: ~/Imports/claude.json
  chatgpt: ~/Imports/chatgpt.json
```

### Multi-User Setup

Use environment variables for per-user configuration:

```yaml
# config.yaml (shared)
archive:
  path: ~/AI-CHAT-ARCHIVE

# User 1
export ARCHIVE_PATH="~/user1-archive"

# User 2
export ARCHIVE_PATH="~/user2-archive"
```

### Development vs Production

Use different configs:

```bash
# Development
cp config/config.yaml.example config/config.dev.yaml
export ARCHIVE_PATH="~/dev-archive"

# Production
cp config/config.yaml.example config/config.prod.yaml
export ARCHIVE_PATH="~/archive"
```

## Troubleshooting

### Config Not Loading

**Symptom:** Default values being used

**Check:**
```bash
# Verify file exists
ls config/config.yaml

# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('config/config.yaml'))"
```

### Paths Not Expanding

**Symptom:** `~` in path not expanded

**Solution:** Use environment variables instead:
```bash
export ARCHIVE_PATH="$HOME/AI-CHAT-ARCHIVE"
```

### Human OS Not Working

**Symptom:** "No domains loaded" message

**Check:**
1. `human_os.enabled: true` in config
2. `human_os.path` points to valid Human OS
3. `human_os.domains` matches your actual domains
4. INDEX files exist: `@domain-INDEX.md`

---

**Need help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or [open an issue](https://github.com/yourusername/ai-chat-archive/issues)
