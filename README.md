# AI Chat Archive

[![Use this template](https://img.shields.io/badge/Use-this-template-success?style=for-the-badge&logo=github)](https://github.com/brentolmate/ai-chat-archive/generate)

> Transform AI chat exports into a searchable, organized knowledge base. Zero-config setup.

---

## 🎯 What This Does

Transform raw AI conversation exports into:
- **Organized markdown files** — Structured by year/month
- **Auto-tagged conversations** — Domains and topics detected automatically
- **Searchable knowledge base** — Find past conversations by keyword, domain, or time
- **Portable format** — Plain markdown files work anywhere

### Before & After

**Before:** Raw JSON exports buried in download folders
```json
[{"name": "Conversation", "chat_messages": [...]}]
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
2. Click **Settings** → **Account** → **Data**
3. Click **"Request data export"**
4. Wait for email (24-48 hours)
5. Download ZIP, extract `conversations.json`

**Where to Place:**
```bash
~/RAW-AI-CHAT-IMPORT/claude export/conversations.json
```

### ✅ ChatGPT (chatgpt.com)

**How to Export:**
1. Go to [chatgpt.com](https://chatgpt.com)
2. Click **Settings** → **Data Controls** → **Export data**
3. Wait for email
4. Download ZIP, extract `conversations.json`

**Where to Place:**
```bash
~/RAW-AI-CHAT-IMPORT/CHAT GPT Archive/conversations.json
```

### ❌ Not Currently Supported

| Platform | Status |
|----------|--------|
| Perplexity | ⚠️ Different export format |
| Copilot | ⚠️ No export feature |
| Gemini | ⚠️ Different JSON structure |

[Request support](https://github.com/brentolmate/ai-chat-archive/issues) for other platforms.

---

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Get the archive
git clone https://github.com/brentolmate/ai-chat-archive.git
cd ai-chat-archive

# 2. Run setup wizard
python3 bin/setup-config.py

# 3. Place your exports
#    Claude: ~/RAW-AI-CHAT-IMPORT/claude export/conversations.json
#    ChatGPT: ~/RAW-AI-CHAT-IMPORT/CHAT GPT Archive/conversations.json

# 4. Test with sample
python3 bin/import-chats.py --sample --count 5

# 5. If satisfied, import all
python3 bin/import-chats.py --source all
```

**That's it!** Your conversations are now archived at `~/AI-CHAT-ARCHIVE/`.

---

## 📋 Requirements

- **Python 3.7+** - [Download](https://python.org)
- **pip** - Python package manager (included with Python)

**Optional (for better features):**
```bash
pip install pyyaml      # For YAML config
pip install anthropic   # For Claude API summaries
pip install pytest      # For running tests
```

---

## 📖 How to Use

### Step 1: Export Your Conversations

**From Claude:**
1. Login to [claude.ai](https://claude.ai)
2. Settings → Account → Data → Request export
3. Download `conversations.json` from email

**From ChatGPT:**
1. Login to [chatgpt.com](https://chatgpt.com)
2. Settings → Data Controls → Export data
3. Download `conversations.json` from email

### Step 2: Run Setup Wizard

```bash
python3 bin/setup-config.py
```

The wizard asks:
- Archive location (default: `~/AI-CHAT-ARCHIVE`)
- Import sources location (default: `~/RAW-AI-CHAT-IMPORT`)
- Human OS integration (optional, say no if not using it)

Creates `config/config.yaml` with your settings.

### Step 3: Place Export Files

```bash
# Create folders
mkdir -p ~/RAW-AI-CHAT-IMPORT/"claude export"
mkdir -p ~/RAW-AI-CHAT-IMPORT/"CHAT GPT Archive"

# Copy your exports
cp ~/Downloads/conversations.json ~/RAW-AI-CHAT-IMPORT/"claude export"/
```

### Step 4: Test Import

```bash
python3 bin/import-chats.py --sample --count 5
```

**Expected Output:**
```
Archive location: /Users/you/AI-CHAT-ARCHIVE

Processing Claude exports...
  [1/5] Music Production -> 2026/01-January/2026-01-16-music-production.md
  [2/5] Brand Strategy -> 2026/01-January/2026-01-16-brand-strategy.md

============================================================
Import complete!
  Imported: 5
  Errors: 0
============================================================
```

### Step 5: Review & Full Import

```bash
# Review results
cat ~/AI-CHAT-ARCHIVE/2026/01-January/2026-01-16-music-production.md

# Import everything
python3 bin/import-chats.py --source all
```

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

### By Tag
```bash
grep -r "tags.*brand" ~/AI-CHAT-ARCHIVE/
```

### With Claude Code Skills

If using [Claude Code](https://code.anthropic.com):

```bash
# Install skills
./bin/install-skills.sh

# Archive current session
/archive topic domain tags

# Search archives
/archive-query @domain keyword
```

---

## ⚙️ Configuration

Edit `config/config.yaml` (created by setup wizard):

```yaml
archive:
  path: ~/AI-CHAT-ARCHIVE          # Where to store

import_sources:
  claude: ~/RAW-AI-CHAT-IMPORT/claude export/conversations.json
  chatgpt: ~/RAW-AI-CHAT-IMPORT/CHAT GPT Archive/conversations.json

human_os:
  enabled: false                    # Optional integration

domains:
  default: system
  custom:
    "@mydomain":
      - keyword1
      - keyword2
```

See [CONFIGURATION.md](https://github.com/brentolmate/ai-chat-archive/blob/main/CONFIGURATION.md) for all options.

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

```markdown
---
date: 2026-01-16
topic: Music Production Workflow
domains: ["loopwalker"]
tags: ["music", "production", "workflow"]
ai: claude
---

# Music Production Workflow

**Date:** 2026-01-16
**Source:** Claude

## Summary
[2-3 sentence overview]

## Key Outputs
- Decision 1
- Decision 2

## Transcript
[Full conversation]
```

### What Gets Extracted

| Field | Source | Example |
|-------|--------|---------|
| **Date** | Export timestamp | `2026-01-16` |
| **Title** | Export name | `"Music Production Workflow"` |
| **Domain** | Auto-detected | `@loopwalker` |
| **Tags** | Keywords + domain | `["music", "production"]` |
| **Summary** | Generated | 2-3 sentences |
| **Key Outputs** | Extracted | Bullet points |
| **Transcript** | Full export | All messages |

---

## 🎨 Customization

### Add Custom Domains

Edit `config/config.yaml`:

```yaml
domains:
  custom:
    "@writing":
      - blog
      - article
      - essay
    "@development":
      - python
      - javascript
      - api
```

See [docs/CUSTOM_DOMAINS.md](https://github.com/brentolmate/ai-chat-archive/blob/main/docs/CUSTOM_DOMAINS.md)

### Change Archive Location

```yaml
archive:
  path: ~/my-custom-archive
```

### Use Environment Variables

```bash
export ARCHIVE_PATH="~/My-Archive"
python3 bin/import-chats.py --source all
```

---

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test specific function
pytest tests/test_import.py::test_sanitize_topic

# With coverage
pytest --cov=bin tests/
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [HOW_TO_USE.md](https://github.com/brentolmate/ai-chat-archive/blob/main/HOW_TO_USE.md) | Complete user guide |
| [QUICKSTART.md](https://github.com/brentolmate/ai-chat-archive/blob/main/QUICKSTART.md) | 5-minute setup |
| [CONFIGURATION.md](https://github.com/brentolmate/ai-chat-archive/blob/main/CONFIGURATION.md) | All config options |
| [IMPORT.md](https://github.com/brentolmate/ai-chat-archive/blob/main/IMPORT.md) | Export instructions |
| [TROUBLESHOOTING.md](https://github.com/brentolmate/ai-chat-archive/blob/main/TROUBLESHOOTING.md) | Common issues |
| [docs/CUSTOM_DOMAINS.md](https://github.com/brentolmate/ai-chat-archive/blob/main/docs/CUSTOM_DOMAINS.md) | Domain setup |
| [docs/ARCHITECTURE.md](https://github.com/brentolmate/ai-chat-archive/blob/main/docs/ARCHITECTURE.md) | System architecture |

---

## 🐛 Troubleshooting

### "conversations.json not found"
```bash
# Check file exists
ls ~/RAW-AI-CHAT-IMPORT/"claude export"/conversations.json
```

### "JSON decode error"
```bash
# Validate JSON
python3 -c "import json; json.load(open('path/to/conversations.json'))"
```

### More Help?
See [TROUBLESHOOTING.md](https://github.com/brentolmate/ai-chat-archive/blob/main/TROUBLESHOOTING.md)

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](https://github.com/brentolmate/ai-chat-archive/blob/main/CONTRIBUTING.md)

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](https://github.com/brentolmate/ai-chat-archive/blob/main/LICENSE)

---

## 🙏 Acknowledgments

- Designed for personal knowledge management
- Inspired by Human OS and Final Signal Path architecture
- Built to work with Claude Code

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/brentolmate/ai-chat-archive/issues)
- **Discussions:** [GitHub Discussions](https://github.com/brentolmate/ai-chat-archive/discussions)
- **Documentation:** See full list above

---

[![Use this template](https://img.shields.io/badge/Use-this-template-success?style=for-the-badge&logo=github)](https://github.com/brentolmate/ai-chat-archive/generate)

**Made with ❤️ for personal knowledge management**
