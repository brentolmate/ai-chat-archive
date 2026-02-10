# Human OS Integration Guide

## What is Human OS?

Human OS is a personal knowledge and build system that uses:
- Domain-based organization (@loopwalker, @brent, @gal, etc.)
- Sprint planning with flagship goals
- INDEX files for tracking NOW/NEXT/LATER work

## Why Integrate?

When enabled, the AI Chat Archive reads Human OS context to:
1. **Add sprint-related tags** - If flagship is "brand system", tag conversations as "brand"
2. **Inform domain detection** - Active projects in @loopwalker increase loopwalker domain likelihood
3. **Enrich metadata** - Connect conversations to active work

## How It Works

```
Human OS/
├── SYSTEM/00-Index/Sprint.md          ← Reads flagship goal
├── @loopwalker-INDEX.md               ← Reads active projects
├── @brent-INDEX.md
└── @gal-INDEX.md
```

### Data Read

**From Sprint.md:**
```markdown
## Flagship: Brand System for Loopwalker
```
→ Adds "brand" tag to conversations

**From @domain-INDEX.md:**
```markdown
## NOW
| Project | Stage | Focus |
|---------|-------|-------|
| Positioning Framework | 2 | Core Assets |
```
→ Increases domain detection confidence

## Configuration

### Enable Human OS

**Option 1: Setup Wizard**
```bash
python3 bin/setup-config.py
# Answer "Yes" to "Enable Human OS integration?"
```

**Option 2: Manual Config**

Edit `config/config.yaml`:

```yaml
human_os:
  enabled: true
  path: ~/Human  # or your actual path
  domains:
    - loopwalker
    - brent
    - gal
    - pulsekeeper
    - shadow-institute
    - unlimited-band
```

### Disable Human OS

```yaml
human_os:
  enabled: false
```

The archive will use keyword-based detection instead (still works well).

## Without Human OS

### What You Lose

- Sprint-based tags
- Active project context

### What Still Works

- Domain detection (via keywords)
- Tag generation (via topic keywords)
- All core functionality

### Example

**Without Human OS:**
```yaml
# Domain detected via keywords
domains: ["loopwalker"]
tags: ["loopwalker", "music", "song"]
```

**With Human OS (flagship: brand work):**
```yaml
# Same domain detection
domains: ["loopwalker"]
# Enriched tags from sprint context
tags: ["loopwalker", "music", "brand", "positioning"]
```

## Troubleshooting

### Path Not Found

**Error:** `Human OS path not found`

**Solution:**
1. Check path in `config/config.yaml`
2. Use absolute path or `~` for home directory
3. Verify path exists: `ls ~/Human`

### INDEX Files Not Loading

**Error:** `No domains loaded`

**Solution:**
1. Verify `human_os.domains` list matches your actual domains
2. Check INDEX files exist: `ls ~/Human/@*-INDEX.md`
3. Ensure INDEX files have proper structure

### Sprint.md Not Found

**Error:** `Sprint.md not found at path`

**Solution:**
1. Check if you use sprint planning
2. If not, the system still works without it
3. Path should be: `~/Human/SYSTEM/00-Index/Sprint.md`

## Custom Domain Setup

If you have different domains than the defaults:

```yaml
human_os:
  enabled: true
  path: ~/KnowledgeBase  # your custom path
  domains:
    - writing
    - development
    - fitness
    - marketing
```

And create corresponding INDEX files:
```
~/KnowledgeBase/
├── @writing-INDEX.md
├── @development-INDEX.md
├── @fitness-INDEX.md
└── @marketing-INDEX.md
```

## Minimal Human OS Setup

If you want to use Human OS integration but don't have a full system:

### 1. Create Basic Structure

```bash
mkdir -p ~/Human/SYSTEM/00-Index
```

### 2. Create Sprint.md

```bash
cat > ~/Human/SYSTEM/00-Index/Sprint.md << 'EOF'
# Sprint

## Flagship: Your Main Goal This Sprint

## Focus Areas
- Area 1
- Area 2
EOF
```

### 3. Create One Domain INDEX

```bash
cat > ~/Human/@mydomain-INDEX.md << 'EOF'
# My Domain Index

## NOW
| Project | Stage | Focus |
|---------|-------|-------|
| Project A | 1 | Foundation |

## NEXT
- Project B

## LATER
- Future idea
EOF
```

### 4. Update Config

```yaml
human_os:
  enabled: true
  path: ~/Human
  domains:
    - mydomain
```

## Best Practices

1. **Keep INDEX files updated** - Archive reads from NOW section
2. **Use consistent flagship** - Helps tag conversations correctly
3. **Match domains in config** - Only list domains you have INDEX files for
4. **Test without first** - Verify basic import works, then enable Human OS

---

**Need help?** See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) or [open an issue](https://github.com/yourusername/ai-chat-archive/issues)
