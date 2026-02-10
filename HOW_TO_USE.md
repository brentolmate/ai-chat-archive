# AI Chat Archive - User Guide

> **Transform AI chat exports into a searchable, organized knowledge base**

This guide explains how to use the AI Chat Archive system and which AI platforms it supports.

---

## 🎯 What This Does

The AI Chat Archive transforms raw AI conversation exports into:

- **Organized markdown files** — Structured by year/month for easy browsing
- **Auto-tagged conversations** — Domains and topics detected automatically
- **Searchable knowledge base** — Find past conversations by keyword, domain, or time
- **Portable format** — Plain markdown files work anywhere

### Before & After

**Before:** Raw JSON exports buried in download folders
```json
[
  {"name": "Conversation", "chat_messages": [...]}
]
```

**After:** Organized, tagged, searchable archive
```markdown
---
date: 2026-01-16
topic: Music Production Workflow
domains: ["loopwalker"]
tags: ["music", "production", "workflow"]
---

# Music Production Workflow

## Summary
Conversation about creating a systematic workflow...

## Key Outputs
- 5-stage workflow defined
- Quality checkpoints established
```

---

## 📥 Supported Export Formats

### ✅ Claude (claude.ai)

**How to Export:**
1. Go to [claude.ai](https://claude.ai)
2. Click **Settings** (gear icon)
3. Select **Account**
4. Scroll to **Data** section
5. Click **"Request data export"**
6. Wait for email (may take 24-48 hours)
7. Download ZIP file
8. Extract and find `conversations.json`

**File Format:** JSON
```json
[
  {
    "name": "Conversation title",
    "created_at": "2026-01-16T10:00:00Z",
    "chat_messages": [
      {"sender": "Human", "text": "..."},
      {"sender": "Assistant", "text": "..."}
    ]
  }
]
```

**Where to Place It:**
```
~/RAW-AI-CHAT-IMPORT/claude export/conversations.json
```

---

### ✅ ChatGPT (chatgpt.com)

**How to Export:**
1. Go to [chatgpt.com](https://chatgpt.com)
2. Click **Settings** (gear icon)
3. Select **Data Controls**
4. Click **"Export data"**
5. Confirm export
6. Wait for email
7. Download ZIP file
8. Extract and find `conversations.json`

**File Format:** JSON
```json
[
  {
    "title": "Conversation title",
    "create_time": 1642357200.0,
    "mapping": {
      "node1": {
        "message": {
          "author": {"role": "user"},
          "content": {
            "content_type": "text",
            "parts": ["message text"]
          }
        }
      }
    }
  }
]
```

**Where to Place It:**
```
~/RAW-AI-CHAT-IMPORT/CHAT GPT Archive/conversations.json
```

---

## ❌ Not Currently Supported

| Platform | Status | Notes |
|----------|--------|-------|
| **Perplexity** | ⚠️ Not supported | Different export format |
| **Copilot** | ⚠️ Not supported | No export feature |
| **Gemini** | ⚠️ Not supported | Different JSON structure |
| **Claude Code** | ⚠️ Partial | Manual export via skills |

**Want support for another platform?** [Open an issue](https://github.com/brentolmate/ai-chat-archive/issues) with a sample export format.

---

## 🚀 How to Use (Step-by-Step)

### Step 1: Get the Archive

**Option A: Use Template (Recommended)**
1. Go to https://github.com/brentolmate/ai-chat-archive
2. Click green **"Use this template"** button
3. Choose your GitHub account
4. Clone your new repository

**Option B: Direct Download**
```bash
git clone https://github.com/brentolmate/ai-chat-archive.git
cd ai-chat-archive
```

### Step 2: Run Setup Wizard

```bash
python3 bin/setup-config.py
```

The wizard will ask:
- **Archive location** - Where to store conversations (default: `~/AI-CHAT-ARCHIVE`)
- **Import sources** - Where your export files are (default: `~/RAW-AI-CHAT-IMPORT`)
- **Human OS** - Enable integration? (optional, say no if you don't use it)

This creates `config/config.yaml` with your settings.

### Step 3: Prepare Your Exports

#### For Claude:
1. Export from claude.ai (see above)
2. Create folder: `mkdir -p ~/RAW-AI-CHAT-IMPORT/"claude export"`
3. Place file: `conversations.json` in that folder

#### For ChatGPT:
1. Export from chatgpt.com (see above)
2. Create folder: `mkdir -p ~/RAW-AI-CHAT-IMPORT/"CHAT GPT Archive"`
3. Place file: `conversations.json` in that folder

**Both platforms?** Place both exports in their respective folders.

### Step 4: Test Import

Always test with a small sample first:

```bash
python3 bin/import-chats.py --sample --count 5
```

**Expected Output:**
```
Archive location: /Users/you/AI-CHAT-ARCHIVE
Human OS integration: Disabled

Processing Claude exports...
  [1/5] Music Production Workflow -> 2026/01-January/2026-01-16-music-production.md
  [2/5] Brand Positioning -> 2026/01-January/2026-01-16-brand-positioning.md
  ...

============================================================
Import complete!
  Imported: 5
  Errors: 0
  Mode: Sample
============================================================
```

### Step 5: Review Results

Check that the imported files look correct:

```bash
# View first imported file
find ~/AI-CHAT-ARCHIVE/ -name "*.md" -type f | head -1 | xargs cat
```

Verify:
- ✅ File naming makes sense
- ✅ Topic is accurate
- ✅ Domain detection is correct
- ✅ Tags are relevant

### Step 6: Full Import

Once satisfied with the sample:

```bash
# Import everything from both platforms
python3 bin/import-chats.py --source all

# Or import one platform at a time
python3 bin/import-chats.py --source claude
python3 bin/import-chats.py --source chatgpt
```

This may take a while for large archives. Progress is shown every 100 conversations.

### Step 7: (Optional) Install Claude Code Skills

If you use [Claude Code](https://code.anthropic.com):

```bash
cd ai-chat-archive
./bin/install-skills.sh
```

Now you can:
- **Archive current session:** `/archive topic domain tags`
- **Search archives:** `/archive-query @domain keyword`

---

## 📁 What You Get

### Archive Structure

```
~/AI-CHAT-ARCHIVE/
├── INDEX.md              # Master index
├── 2024/
│   ├── 06-June/
│   │   └── 2024-06-15-topic.md
│   └── 07-July/
├── 2025/
└── 2026/
    └── 01-January/
        └── 2026-01-16-music-production.md
```

### File Format

Each archived conversation includes:

**Frontmatter** (metadata):
```yaml
---
date: 2026-01-16
topic: Music Production Workflow
domains: ["loopwalker"]
tags: ["music", "production", "workflow"]
ai: claude
---
```

**Content:**
- **Summary** - 2-3 sentence overview
- **Key Outputs** - Decisions and insights
- **Transcript** - Full conversation

---

## 🔍 Searching Your Archive

### By Keyword
```bash
grep -r "positioning" ~/AI-CHAT-ARCHIVE/
```

### By Domain
```bash
grep -r "domains.*loopwalker" ~/AI-CHAT-ARCHIVE/
```

### By Date
```bash
# All conversations from January 2026
ls ~/AI-CHAT-ARCHIVE/2026/01-January/
```

### By Tag
```bash
grep -r "tags.*brand" ~/AI-CHAT-ARCHIVE/
```

### With Claude Code Skills
```bash
# If you installed the skills
/archive-query @loopwalker positioning
/archive-query "music production"
/archive-query December brand strategy
```

---

## ⚙️ Customization

### Add Your Own Domains

Edit `config/config.yaml`:

```yaml
domains:
  custom:
    "@writing":
      - blog
      - article
      - essay
      - copy
    "@development":
      - python
      - javascript
      - api
      - database
```

### Change Archive Location

```yaml
archive:
  path: ~/my-custom-archive
```

### Disable Human OS

If you don't use Human OS (most users):

```yaml
human_os:
  enabled: false
```

The archive will use keyword-based detection (still works well!).

---

## 🧪 Testing Your Setup

### Verify Configuration

```bash
# Check config is valid
python3 -c "import yaml; yaml.safe_load(open('config/config.yaml'))"
```

### Verify Exports

```bash
# Claude export
python3 -c "import json; json.load(open('~/RAW-AI-CHAT-IMPORT/claude export/conversations.json'))"

# ChatGPT export
python3 -c "import json; json.load(open('~/RAW-AI-CHAT-IMPORT/CHAT GPT Archive/conversations.json'))"
```

### Test Import

```bash
# Import 1 conversation
python3 bin/import-chats.py --sample --count 1

# Check output
ls ~/AI-CHAT-ARCHIVE/
```

---

## 📊 What Gets Extracted

### From Conversations

| Field | Source | Example |
|-------|--------|---------|
| **Date** | Export timestamp | `2026-01-16` |
| **Title** | Export name/title | `"Music Production Workflow"` |
| **Domain** | Auto-detected from content | `@loopwalker` |
| **Tags** | Keywords + domain | `["music", "production", "loopwalker"]` |
| **Summary** | Generated from content | 2-3 sentences |
| **Key Outputs** | Decisions extracted | Bullet points |
| **Transcript** | Full conversation | All messages |

### Domain Detection

The system detects domains by matching keywords in conversation content:

| Domain | Keywords |
|--------|----------|
| `@loopwalker` | music, song, lyrics, melody, hip-hop, trap |
| `@brent` | brand, positioning, website, founder |
| `@gal` | connection, outreach, networking, instagram |
| `@system` | workflow, automation, process, system |

**Customize domains** in `config/config.yaml`

---

## 🐛 Troubleshooting

### "conversations.json not found"

**Problem:** Can't find your export files

**Solution:**
```bash
# Check file exists
ls ~/RAW-AI-CHAT-IMPORT/"claude export"/conversations.json

# Or with custom path
ls /path/to/your/export.json
```

Update `config/config.yaml` if using custom path.

### "JSON decode error"

**Problem:** Export file is corrupted or wrong format

**Solution:**
```bash
# Validate JSON
python3 -c "import json; json.load(open('path/to/conversations.json'))"
```

Re-export from source if validation fails.

### "No valid conversations found"

**Problem:** JSON structure doesn't match expected format

**Solution:**
- Ensure you exported "conversations" not "account data"
- Check JSON has correct structure (see [Supported Export Formats](#-supported-export-formats))
- [Open an issue](https://github.com/brentolmate/ai-chat-archive/issues) with sample

### Domain detection wrong?

**Solution:** Add custom keywords to `config/config.yaml`:

```yaml
domains:
  custom:
    "@mydomain":
      - specific-keyword-1
      - specific-keyword-2
```

See [docs/CUSTOM_DOMAINS.md](https://github.com/brentolmate/ai-chat-archive/blob/main/docs/CUSTOM_DOMAINS.md) for details.

### More Help?

See [TROUBLESHOOTING.md](https://github.com/brentolmate/ai-chat-archive/blob/main/TROUBLESHOOTING.md) for comprehensive troubleshooting.

---

## 📚 Advanced Usage

### Environment Variables

Override config without editing files:

```bash
# Custom archive location
export ARCHIVE_PATH="~/My-Archive"

# Custom import location
export IMPORT_ROOT="~/My-Exports"

# Run import
python3 bin/import-chats.py --source all
```

### Claude API for Better Summaries

Use Claude API for higher-quality summaries:

```bash
# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Import with API
python3 bin/import-chats.py --claude-api --source all
```

Requires: `pip install anthropic`

### Schedule Automatic Imports

**macOS/Linux (cron):**
```bash
# Edit crontab
crontab -e

# Add weekly import (Sundays at 2am)
0 2 * * 0 cd ~/ai-chat-archive && python3 bin/import-chats.py --source all
```

---

## 🎓 Examples

### Example 1: Music Producer

**Exports:** Claude conversations about music production

**Setup:**
```yaml
domains:
  custom:
    "@music":
      - beat
      - production
      - mixing
      - mastering
      - daw
```

**Result:** Conversations auto-tagged with music-related domains

### Example 2: Developer

**Exports:** ChatGPT coding conversations

**Setup:**
```yaml
domains:
  custom:
    "@coding":
      - python
      - javascript
      - api
      - database
      - bug
```

**Result:** Easy to find solutions to past coding problems

### Example 3: Content Creator

**Exports:** Both Claude and ChatGPT for content strategy

**Setup:**
```yaml
domains:
  custom:
    "@content":
      - blog
      - video
      - script
      - seo
```

**Result:** Unified archive across platforms, searchable by topic

---

## 🤝 Contributing

Found a bug or have a feature request?

- **Bug reports:** [Open an issue](https://github.com/brentolmate/ai-chat-archive/issues/new?template=bug_report.md)
- **Features:** [Open an issue](https://github.com/brentolmate/ai-chat-archive/issues/new?template=feature_request.md)
- **Questions:** [Start a discussion](https://github.com/brentolmate/ai-chat-archive/discussions)

Want to contribute code? See [CONTRIBUTING.md](https://github.com/brentolmate/ai-chat-archive/blob/main/CONTRIBUTING.md)

---

## 📄 License

MIT License - Free to use, modify, and distribute

---

**Last updated:** 2026-02-10
**Version:** 1.0.0
**Repository:** https://github.com/brentolmate/ai-chat-archive

---

## 🎉 You're Ready!

1. ✅ Export from Claude or ChatGPT
2. ✅ Run `python3 bin/setup-config.py`
3. ✅ Place exports in import folder
4. ✅ Run `python3 bin/import-chats.py --sample`
5. ✅ Search your organized archive!

**Need help?** [Open an issue](https://github.com/brentolmate/ai-chat-archive/issues)
