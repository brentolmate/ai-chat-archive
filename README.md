# AI Chat Archive

[![Use this template](https://img.shields.io/badge/Use-this-template-success?style=for-the-badge&logo=github)](https://github.com/yourusername/ai-chat-archive/generate)

> A zero-config system for archiving, organizing, and searching AI conversations from Claude and ChatGPT.

## ✨ Features

- **Zero-config setup** — Works out of the box with sensible defaults
- **Intelligent tagging** — Auto-detects domains and generates relevant tags
- **Human OS integration** (optional) — Reads Sprint.md and domain INDEX files for context
- **Claude Code skills** — `/archive` and `/archive-query` for seamless workflow
- **Dual import modes** — JSON bulk import or manual single-file archiving
- **Flexible configuration** — YAML config with environment variable override
- **Platform-agnostic** — Works on macOS, Linux, Windows (WSL)

## 🚀 Quick Start

```bash
# 1. Clone or download this template
git clone https://github.com/yourusername/ai-chat-archive.git
cd ai-chat-archive

# 2. Run setup wizard
python3 bin/setup-config.py

# 3. Place your AI exports
#    Claude: ~/RAW-AI-CHAT-IMPORT/claude export/conversations.json
#    ChatGPT: ~/RAW-AI-CHAT-IMPORT/CHAT GPT Archive/conversations.json

# 4. Test with sample import
python3 bin/import-chats.py --sample --count 5

# 5. If satisfied, import all
python3 bin/import-chats.py --source all
```

**That's it!** Your conversations are now archived at `~/AI-CHAT-ARCHIVE/`.

For detailed setup, see [QUICKSTART.md](QUICKSTART.md).

## 📋 Requirements

- Python 3.7 or higher
- pip (Python package manager)

**Optional dependencies:**
- `pyyaml` — For YAML configuration files
- `anthropic` — For Claude API summaries (better quality)
- `pytest` — For running tests

Install optional dependencies:
```bash
pip install pyyaml anthropic pytest
```

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup guide |
| [CONFIGURATION.md](CONFIGURATION.md) | All configuration options |
| [IMPORT.md](IMPORT.md) | Detailed import guide with export instructions |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and solutions |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture |
| [docs/HUMAN_OS_INTEGRATION.md](docs/HUMAN_OS_INTEGRATION.md) | Human OS setup guide |
| [docs/CUSTOM_DOMAINS.md](docs/CUSTOM_DOMAINS.md) | Creating custom domains |

## 🎯 Use Cases

### Daily Work Archive

Archive valuable conversations as you work:

```bash
# After an important session
/archive loopwalker-positioning loopwalker positioning,brand,offer
```

### Bulk Historical Import

Import thousands of past conversations:

```bash
# Import all Claude and ChatGPT exports
python3 bin/import-chats.py --source all

# Or import one platform at a time
python3 bin/import-chats.py --source claude
python3 bin/import-chats.py --source chatgpt
```

### Search Archived Conversations

Find past work quickly:

```bash
# Search by domain
/archive-query @loopwalker positioning

# Search by topic
/archive-query "rap songs"

# Search by time
/archive-query December brand strategy
```

## 🔧 Configuration

Configure via `config/config.yaml` (created by setup wizard):

```yaml
archive:
  path: ~/AI-CHAT-ARCHIVE

import_sources:
  claude: ~/RAW-AI-CHAT-IMPORT/claude export/conversations.json
  chatgpt: ~/RAW-AI-CHAT-IMPORT/CHAT GPT Archive/conversations.json

human_os:
  enabled: true  # Optional integration
  path: ~/Human

domains:
  default: system
  custom:
    # Your domain keywords here
```

See [CONFIGURATION.md](CONFIGURATION.md) for all options.

## 📁 Archive Structure

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
        └── 2026-01-16-loopwalker-positioning.md
```

Each file includes:
- **Frontmatter** — date, topic, domains, tags, ai source
- **Summary** — 2-3 sentence overview
- **Key Outputs** — Decisions and insights
- **Transcript** — Full conversation

## 🎨 Customization

### Add Custom Domains

Edit `config/config.yaml`:

```yaml
domains:
  custom:
    "@mydomain":
      - keyword1
      - keyword2
      - keyword3
```

See [docs/CUSTOM_DOMAINS.md](docs/CUSTOM_DOMAINS.md) for details.

### Disable Human OS

If you don't use Human OS:

```yaml
human_os:
  enabled: false
```

The archive will use keyword-based detection (still works well).

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run specific test
pytest tests/test_import.py::test_sanitize_topic

# Run with coverage
pytest --cov=bin tests/
```

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Quick start:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Designed for personal knowledge management
- Inspired by Human OS and Final Signal Path architecture
- Built to work with Claude Code

## 📞 Support

- **Documentation:** See [QUICKSTART.md](QUICKSTART.md) and [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Issues:** [GitHub Issues](https://github.com/yourusername/ai-chat-archive/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/ai-chat-archive/discussions)

## 🗺️ Roadmap

- [ ] Web interface for browsing archives
- [ ] Vector search integration (RAG)
- [ ] Duplicate detection
- [ ] Automatic index updates
- [ ] Export to other formats (PDF, HTML)
- [ ] Tag management UI

---

**Made with ❤️ for personal knowledge management**

[![Template](https://img.shields.io/badge/Use-this-template-success?style=for-the-badge&logo=github)](https://github.com/yourusername/ai-chat-archive/generate)
