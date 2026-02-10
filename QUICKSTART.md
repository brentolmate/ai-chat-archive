# Quick Start Guide

Get your AI Chat Archive up and running in 5 minutes.

## Prerequisites

- Python 3.7+ installed
- AI chat exports from Claude or ChatGPT (optional for setup)

## Step 1: Get the Archive

**Option A: Clone from GitHub**
```bash
git clone https://github.com/yourusername/ai-chat-archive.git
cd ai-chat-archive
```

**Option B: Download ZIP**
1. Download from GitHub
2. Extract to folder
3. Open terminal in that folder

## Step 2: Run Setup Wizard

```bash
python3 bin/setup-config.py
```

The wizard will ask:
1. **Archive location** - Where to store conversations (default: `~/AI-CHAT-ARCHIVE`)
2. **Import sources** - Where your export files are (default: `~/RAW-AI-CHAT-IMPORT`)
3. **Human OS** - Enable integration? (default: no)

This creates `config/config.yaml` with your settings.

## Step 3: Prepare Your Exports

### Claude Export

1. Go to [claude.ai](https://claude.ai)
2. Click **Settings** → **Export data**
3. Download conversations as JSON
4. Place at: `~/RAW-AI-CHAT-IMPORT/claude export/conversations.json`

### ChatGPT Export

1. Go to [chatgpt.com](https://chatgpt.com)
2. Click **Settings** → **Data controls** → **Export**
3. Download conversations
4. Place at: `~/RAW-AI-CHAT-IMPORT/CHAT GPT Archive/conversations.json`

**Don't have exports yet?** Skip to Step 4 and test with sample data.

## Step 4: Test Import

Run a sample import to verify everything works:

```bash
cd ~/ai-chat-archive  # or wherever you cloned it
python3 bin/import-chats.py --sample --count 5
```

This will:
- Import 5 conversations
- Create archive folders
- Generate markdown files
- Show you the results

### Expected Output

```
Archive location: /Users/you/AI-CHAT-ARCHIVE
Human OS integration: Disabled

Processing Claude exports from ~/RAW-AI-CHAT-IMPORT/claude export/conversations.json...
  [1/5] Conversation about music -> 2026/01-January/2026-01-16-music.md
  [2/5] Brand strategy discussion -> 2026/01-January/2026-01-16-brand-strategy.md
  ...

============================================================
Import complete!
  Imported: 5
  Errors: 0
  Mode: Sample
============================================================
```

## Step 5: Review Results

Check the imported files:

```bash
# List archive contents
ls -R ~/AI-CHAT-ARCHIVE/

# View a file
cat ~/AI-CHAT-ARCHIVE/2026/01-January/2026-01-16-music.md
```

Verify:
- ✅ File naming makes sense
- ✅ Topic extraction is accurate
- ✅ Domain detection is correct
- ✅ Tags are relevant

## Step 6: Full Import

If sample looks good, import everything:

```bash
python3 bin/import-chats.py --source all
```

This may take a while for large archives. Progress is shown every 100 conversations.

## Step 7: Install Claude Code Skills (Optional)

If you use Claude Code, install the skills:

```bash
cd ~/ai-chat-archive
./bin/install-skills.sh
```

Now you can:
- Archive current session: `/archive topic domain tags`
- Search archives: `/archive-query @domain keyword`

## Troubleshooting

### "Module not found" Error

```bash
# Install pyyaml
pip install pyyaml
```

### "Path not found" Error

Check your `config/config.yaml` paths are correct:
```yaml
archive:
  path: ~/AI-CHAT-ARCHIVE  # Use ~ for home directory

import_sources:
  claude: ~/RAW-AI-CHAT-IMPORT/claude export/conversations.json
```

### "No conversations found"

Verify your export files exist:
```bash
# Claude
ls ~/RAW-AI-CHAT-IMPORT/claude\ export/conversations.json

# ChatGPT
ls ~/RAW-AI-CHAT-IMPORT/CHAT\ GPT\ Archive/conversations.json
```

## Next Steps

1. **Customize domains** - Edit `config/config.yaml` to add your domains
2. **Enable Human OS** - If you use it, set `human_os.enabled: true`
3. **Set up automation** - Run imports on schedule
4. **Explore docs** - See full documentation list in README.md

## Environment Variables (Optional)

Override config without editing files:

```bash
# Custom archive location
export ARCHIVE_PATH="~/My-Archive"

# Custom import location
export IMPORT_ROOT="~/My-Imports"

# Disable Human OS
export HUMAN_OS_ENABLED="false"

# Then run import
python3 bin/import-chats.py --source all
```

## Quick Reference

| Task | Command |
|------|---------|
| **Setup** | `python3 bin/setup-config.py` |
| **Test import** | `python3 bin/import-chats.py --sample` |
| **Full import** | `python3 bin/import-chats.py --source all` |
| **Claude only** | `python3 bin/import-chats.py --source claude` |
| **ChatGPT only** | `python3 bin/import-chats.py --source chatgpt` |
| **Install skills** | `./bin/install-skills.sh` |
| **View help** | `python3 bin/import-chats.py --help` |

---

**Need more help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or [open an issue](https://github.com/yourusername/ai-chat-archive/issues)
