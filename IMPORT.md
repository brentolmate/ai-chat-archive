# Import Guide

Complete guide to exporting and importing AI conversations.

## Overview

The AI Chat Archive supports importing from:
- **Claude** (claude.ai) — JSON export format
- **ChatGPT** (chatgpt.com) — JSON export format

## Exporting from Claude

### Step 1: Request Export

1. Go to [claude.ai](https://claude.ai)
2. Click **Settings** (gear icon)
3. Select **Account**
4. Scroll to **Data**
5. Click **Request data export**

### Step 2: Download Export

1. Wait for email notification (may take 24-48 hours)
2. Click download link in email
3. Extract ZIP file

### Step 3: Locate Conversations

The ZIP contains a folder structure. Find:

```
claude-export/
└── conversations.json  # This is what you need
```

### Step 4: Place in Import Location

```bash
# Create import directory (if using default)
mkdir -p ~/RAW-AI-CHAT-IMPORT/"claude export"

# Move conversations.json
mv ~/Downloads/claude-export/conversations.json \
   ~/RAW-AI-CHAT-IMPORT/"claude export"/
```

**Note:** The folder name `"claude export"` has a space. Keep it exactly as shown.

### Step 5: Verify

```bash
# Check file exists
ls ~/RAW-AI-CHAT-IMPORT/"claude export"/conversations.json

# Check it's valid JSON
python3 -c "import json; json.load(open('~/RAW-AI-CHAT-IMPORT/claude export/conversations.json'))"
```

## Exporting from ChatGPT

### Step 1: Request Export

1. Go to [chatgpt.com](https://chatgpt.com)
2. Click **Settings** (gear icon)
3. Select **Data Controls**
4. Scroll to **Export data**
5. Click **Confirm export**

### Step 2: Download Export

1. Wait for email notification
2. Click download link
3. Extract ZIP file

### Step 3: Locate Conversations

The ZIP contains:

```
chatgpt-export/
└── conversations.json  # This is what you need
```

### Step 4: Place in Import Location

```bash
# Create import directory (if using default)
mkdir -p ~/RAW-AI-CHAT-IMPORT/"CHAT GPT Archive"

# Move conversations.json
mv ~/Downloads/chatgpt-export/conversations.json \
   ~/RAW-AI-CHAT-IMPORT/"CHAT GPT Archive"/
```

**Note:** The folder name `"CHAT GPT Archive"` has spaces. Keep it exactly as shown.

### Step 5: Verify

```bash
# Check file exists
ls ~/RAW-AI-CHAT-IMPORT/"CHAT GPT Archive"/conversations.json

# Check it's valid JSON
python3 -c "import json; json.load(open('~/RAW-AI-CHAT-IMPORT/CHAT GPT Archive/conversations.json'))"
```

## Import Options

### Test Import (Recommended First)

Always test with a small sample first:

```bash
python3 bin/import-chats.py --sample --count 5
```

This imports 5 conversations so you can verify:
- File naming makes sense
- Topic extraction is accurate
- Domain detection is correct
- Tags are relevant

### Import All Conversations

Once satisfied with test results:

```bash
python3 bin/import-chats.py --source all
```

### Import Single Platform

Import only Claude or only ChatGPT:

```bash
# Claude only
python3 bin/import-chats.py --source claude

# ChatGPT only
python3 bin/import-chats.py --source chatgpt
```

### Import with Claude API

Use Claude API for higher-quality summaries:

```bash
# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Import with API
python3 bin/import-chats.py --claude-api --source all
```

**Note:** Requires `pip install anthropic`

## Command Reference

```
usage: import-chats.py [-h] [--sample] [--count N] [--source {claude,chatgpt,all}]
                       [--claude-api] [--api-key KEY]

options:
  -h, --help            Show help message
  --sample              Run in sample mode (test first N conversations)
  --count N             Number of conversations for sample mode (default: 5)
  --source {claude,chatgpt,all}
                        Which source to import (default: all)
  --claude-api          Use Claude API for higher-quality summaries
  --api-key KEY         Anthropic API key (or set ANTHROPIC_API_KEY env var)
```

## Understanding Import Output

### Successful Import

```
Archive location: /Users/you/AI-CHAT-ARCHIVE
Human OS integration: Enabled

Loading context from Human OS...
  Flagship: Brand System for Loopwalker
  Domains loaded: 6

Processing Claude exports from ~/RAW-AI-CHAT-IMPORT/claude export/conversations.json...
  [1/850] Music production workflow -> 2026/01-January/2026-01-16-music-production.md
  [2/850] Shadow integration lyrics -> 2026/01-January/2026-01-16-shadow-integration-lyrics.md
  ...

Processing ChatGPT exports from ~/RAW-AI-CHAT-IMPORT/CHAT GPT Archive/conversations.json...
  [851/1200] Website positioning -> 2026/01-January/2026-01-16-website-positioning.md
  ...

============================================================
Import complete!
  Imported: 1200
  Errors: 0
  Mode: Batch
============================================================
```

### Import with Errors

```
Processing Claude exports...
  [1/5] Valid chat -> 2026/01-January/2026-01-16-valid.md
  Error processing chat 1: Missing 'created_at' field
  Error processing chat 2: Invalid date format
  [4/5] Another valid chat -> 2026/01-January/2026-01-16-another-valid.md

============================================================
Import complete!
  Imported: 3
  Errors: 2
  Mode: Sample
============================================================
```

Errors are expected with incomplete/malformed conversations. The import continues processing valid conversations.

## Post-Import Verification

### Check Archive Structure

```bash
# List archive contents
ls -R ~/AI-CHAT-ARCHIVE/

# Expected output:
# ~/AI-CHAT-ARCHIVE/
# ├── 2024/
# │   └── 06-June/
# ├── 2025/
# └── 2026/
#     └── 01-January/
```

### View Sample File

```bash
# View first imported file
find ~/AI-CHAT-ARCHIVE/ -name "*.md" -type f | head -1 | xargs cat
```

Expected format:

```markdown
---
date: 2026-01-16
topic: Music Production Workflow
domains: ["loopwalker"]
tags: ["loopwalker", "music", "production"]
ai: claude
---

# Music Production Workflow

**Date:** 2026-01-16
**Source:** Claude

## Summary
Conversation about music production workflow. Related to music and creative work. Key themes: workflow, audio.

## Key Outputs
- Defined 3-stage production process
- Created template for new tracks
- Established quality checklist

## Transcript
**Human:** Let's work on a music production workflow...
**Assistant:** Here's a systematic approach...
```

### Check Stats

```bash
# Total conversations
find ~/AI-CHAT-ARCHIVE/ -name "*.md" -type f | wc -l

# By year
find ~/AI-CHAT-ARCHIVE/2024/ -name "*.md" | wc -l
find ~/AI-CHAT-ARCHIVE/2025/ -name "*.md" | wc -l
find ~/AI-CHAT-ARCHIVE/2026/ -name "*.md" | wc -l

# By domain
grep -r "domains.*loopwalker" ~/AI-CHAT-ARCHIVE/ | wc -l
grep -r "domains.*brent" ~/AI-CHAT-ARCHIVE/ | wc -l
```

## Custom Import Paths

If your exports are in non-default locations:

### Option 1: Edit config.yaml

```yaml
import_sources:
  claude: ~/Downloads/my-claude-export.json
  chatgpt: ~/Documents/chatgpt/conversations.json
```

### Option 2: Use Environment Variables

```bash
export IMPORT_ROOT="~/My-Exports"
python3 bin/import-chats.py --source all
```

## Re-Importing

Running import again will:
- **Skip duplicates** - Based on date + topic + content
- **Add new conversations** - Since last import
- **Not modify existing** - Files are never overwritten

If you want to re-import everything:
1. Delete/archive existing archive
2. Run import again

```bash
# Backup existing archive
mv ~/AI-CHAT-ARCHIVE ~/AI-CHAT-ARCHIVE.backup

# Re-import
python3 bin/import-chats.py --source all
```

## Troubleshooting

### "conversations.json not found"

**Check paths in config:**
```bash
# View config
cat config/config.yaml | grep import_sources

# Verify file exists
ls ~/RAW-AI-CHAT-IMPORT/"claude export"/conversations.json
```

### "JSON decode error"

**Validate JSON:**
```bash
python3 -c "import json; json.load(open('path/to/conversations.json'))"
```

If error, export might be corrupted. Request new export.

### "No valid conversations found"

Check that conversations.json has the expected structure:

**Claude format:**
```json
[
  {
    "name": "Conversation title",
    "created_at": "2026-01-16T10:00:00Z",
    "chat_messages": [...]
  }
]
```

**ChatGPT format:**
```json
[
  {
    "title": "Conversation title",
    "create_time": 1642357200.0,
    "mapping": {...}
  }
]
```

### Domain detection seems wrong

**Check domain keywords in config:**

```yaml
domains:
  custom:
    "@loopwalker":
      - music  # Add more specific keywords
      - song
      - hip-hop
      - trap
```

See [docs/CUSTOM_DOMAINS.md](docs/CUSTOM_DOMAINS.md) for details.

---

**Need help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or [open an issue](https://github.com/yourusername/ai-chat-archive/issues)
