# Troubleshooting Guide

Common issues and solutions for the AI Chat Archive.

## Quick Diagnostics

Run this to check your setup:

```bash
# Check Python version
python3 --version  # Should be 3.7+

# Check dependencies
python3 -c "import yaml, anthropic"  # Should not error

# Check config
python3 -c "import yaml; yaml.safe_load(open('config/config.yaml'))"

# Check paths
ls ~/AI-CHAT-ARCHIVE/
ls ~/RAW-AI-CHAT-IMPORT/
```

## Installation Issues

### "python3: command not found"

**Problem:** Python not installed or not in PATH

**Solution:**

**macOS:**
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3
```

**Windows:**
- Download from [python.org](https://python.org)
- Or use WSL (recommended)

### "ModuleNotFoundError: No module named 'yaml'"

**Problem:** PyYAML not installed

**Solution:**
```bash
pip install pyyaml
```

### Setup wizard fails

**Problem:** `setup-config.py` errors

**Solutions:**

1. **Install pyyaml:**
```bash
pip install pyyaml
```

2. **Run with Python explicitly:**
```bash
python3 bin/setup-config.py
```

3. **Check file permissions:**
```bash
chmod +x bin/setup-config.py
```

## Configuration Issues

### Config file not being read

**Symptoms:** Default paths being used, custom settings ignored

**Solutions:**

1. **Verify file exists:**
```bash
ls config/config.yaml
```

2. **Check YAML syntax:**
```bash
python3 -c "import yaml; yaml.safe_load(open('config/config.yaml'))"
```

3. **Check for typos:**
- Indentation should be spaces (not tabs)
- Colons after keys
- Quotes around string values

4. **Environment variables overriding config:**
```bash
# Check if these are set
echo $ARCHIVE_PATH
echo $IMPORT_ROOT
```

### Path not found errors

**Symptoms:** `Path not found: ~/AI-CHAT-ARCHIVE`

**Solutions:**

1. **Use absolute paths:**
```yaml
archive:
  path: /Users/username/AI-CHAT-ARCHIVE
```

2. **Create directory:**
```bash
mkdir -p ~/AI-CHAT-ARCHIVE
```

3. **Use environment variables:**
```bash
export ARCHIVE_PATH="$HOME/AI-CHAT-ARCHIVE"
```

### Human OS integration not working

**Symptoms:** "Human OS path not found" or "No domains loaded"

**Solutions:**

1. **Check Human OS path:**
```bash
ls ~/Human/SYSTEM/00-Index/Sprint.md
```

2. **Verify config:**
```yaml
human_os:
  enabled: true
  path: ~/Human
  domains:
    - loopwalker  # Must match actual domains
```

3. **Check INDEX files exist:**
```bash
ls ~/Human/@*-INDEX.md
```

4. **Disable if not using:**
```yaml
human_os:
  enabled: false
```

## Import Issues

### "conversations.json not found"

**Problem:** Import script can't find export files

**Solutions:**

1. **Check file location:**
```bash
# Claude
ls ~/RAW-AI-CHAT-IMPORT/"claude export"/conversations.json

# ChatGPT
ls ~/RAW-AI-CHAT-IMPORT/"CHAT GPT Archive"/conversations.json
```

2. **Update config if different location:**
```yaml
import_sources:
  claude: ~/Downloads/conversations.json
```

3. **Create import directory:**
```bash
mkdir -p ~/RAW-AI-CHAT-IMPORT/"claude export"
mkdir -p ~/RAW-AI-CHAT-IMPORT/"CHAT GPT Archive"
```

### JSON decode errors

**Problem:** `JSONDecodeError: Expecting value`

**Solutions:**

1. **Validate JSON:**
```bash
python3 -c "import json; json.load(open('path/to/conversations.json'))"
```

2. **Check file size:**
```bash
ls -lh ~/RAW-AI-CHAT-IMPORT/"claude export"/conversations.json
# Should be > 0 bytes
```

3. **Re-export from source:**
- Request new export from claude.ai or chatgpt.com
- Previous export might be corrupted

### "No valid conversations found"

**Problem:** JSON structure doesn't match expected format

**Solutions:**

1. **Check JSON structure:**
```bash
# Claude format
cat conversations.json | python3 -m json.tool | head -20

# Should look like:
# [
#   {
#     "name": "...",
#     "created_at": "...",
#     "chat_messages": [...]
#   }
# ]
```

2. **Export might be different format:**
- Make sure you exported "conversations" not "account data"
- Re-export with correct option

### Domain detection wrong

**Problem:** Conversations tagged with wrong domain

**Solutions:**

1. **Check domain keywords:**
```bash
cat config/config.yaml | grep -A 10 "domains:"
```

2. **Add more specific keywords:**
```yaml
domains:
  custom:
    "@loopwalker":
      - hip-hop     # More specific than "music"
      - trap beat
      - shadow work
```

3. **Adjust default domain:**
```yaml
domains:
  default: loopwalker  # Change from "system"
```

See [docs/CUSTOM_DOMAINS.md](docs/CUSTOM_DOMAINS.md) for details.

## Claude API Issues

### "anthropic package not installed"

**Solution:**
```bash
pip install anthropic
```

### "Invalid API key"

**Problem:** API key not set or invalid

**Solutions:**

1. **Set environment variable:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

2. **Or use --api-key flag:**
```bash
python3 bin/import-chats.py --claude-api --api-key "sk-ant-..."
```

3. **Verify key:**
```bash
echo $ANTHROPIC_API_KEY
```

### API quota exceeded

**Problem:** Too many API calls

**Solutions:**

1. **Use rule-based summaries (default):**
```bash
python3 bin/import-chats.py --source all  # No --claude-api flag
```

2. **Reduce API usage:**
- Import without `--claude-api` flag
- Use API only for important imports

## Claude Code Skills Issues

### Skills not found

**Problem:** `/archive` command not recognized

**Solutions:**

1. **Install skills:**
```bash
cd ~/ai-chat-archive
./bin/install-skills.sh
```

2. **Check installation:**
```bash
ls ~/.claude/skills/archive
ls ~/.claude/skills/archive-query
```

3. **Restart Claude Code** after installation

### Symlink errors

**Problem:** `symbolic link not allowed`

**Solutions:**

1. **Check if skills already exist:**
```bash
ls ~/.claude/skills/
```

2. **Remove existing:**
```bash
rm ~/.claude/skills/archive
rm ~/.claude/skills/archive-query
```

3. **Run installer again:**
```bash
./bin/install-skills.sh
```

## Performance Issues

### Import is slow

**Problem:** Large imports taking too long

**Solutions:**

1. **Use sample mode first:**
```bash
python3 bin/import-chats.py --sample --count 10
```

2. **Import one platform at a time:**
```bash
python3 bin/import-chats.py --source claude
```

3. **Disable Claude API:**
```bash
# Without API (faster)
python3 bin/import-chats.py --source all

# With API (slower but better quality)
python3 bin/import-chats.py --claude-api --source all
```

### Memory errors

**Problem:** Script crashes with out of memory

**Solutions:**

1. **Import in batches:**
```bash
# Import 100 at a time
head -n 100 conversations.json > conversations-batch.json
python3 bin/import-chats.py --source claude
```

2. **Use sample mode:**
```bash
python3 bin/import-chats.py --sample --count 50
```

## Getting Help

If none of these solutions work:

### Check Documentation

- [QUICKSTART.md](QUICKSTART.md) - Basic setup
- [CONFIGURATION.md](CONFIGURATION.md) - Configuration options
- [IMPORT.md](IMPORT.md) - Import guide

### Debug Mode

Run with verbose output:

```bash
# Check what paths are being used
python3 -c "
from bin.import-chats import load_config
config = load_config()
print('Archive:', config['archive']['path'])
print('Claude:', config['import_sources']['claude'])
print('ChatGPT:', config['import_sources']['chatgpt'])
"
```

### Open an Issue

1. Run diagnostics (above)
2. Copy error message
3. Include your config (remove sensitive paths)
4. [Open an issue](https://github.com/yourusername/ai-chat-archive/issues) with:
   - What you were trying to do
   - What happened (error message)
   - Expected behavior
   - Your OS and Python version

---

**Still stuck?** Join the [GitHub Discussions](https://github.com/yourusername/ai-chat-archive/discussions) for community help.
