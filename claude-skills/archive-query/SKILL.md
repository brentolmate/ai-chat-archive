---
name: archive-query
description: Search AI-CHAT-ARCHIVE using RAG retrieval. Queries support domain (@loopwalker, @brent, etc.), time ranges ("December", "last week"), keywords ("rap songs"), and tags.
invocation: user
allowed-tools: Read, Glob, Grep
---

# Archive Query Skill

Search the AI Chat Archive using intelligent retrieval.

**Triggers:** "search archive", "archive query", "what did we work on", "find in archive"

---

## How It Works

**IMPORTANT:** This skill searches ONLY your archive directory (as configured in config.yaml), not the entire system. When asked for "examples" or "patterns" from your work, always scope to the archive directory.

The archive location is read from `config/config.yaml`:

```yaml
archive:
  path: ~/AI-CHAT-ARCHIVE  # or your custom path
```

### Query Types

1. **Domain queries** (`@loopwalker`, `@brent`, etc.) → Filter by domain frontmatter
2. **Time queries** ("last week", "December", "2025-12-01") → Filter by date
3. **Topic queries** ("rap songs", "brand", "skills") → Search by keywords
4. **Pattern/example queries** ("2E prompt examples", "positioning patterns") → Full-text search
5. **Complex queries** → Combine multiple filters

---

## Quick Reference

| Query | Search Method |
|-------|---------------|
| "What rap songs?" | Grep topics/tags |
| "@loopwalker December" | Grep domains + date |
| "Decisions about brand" | Grep keywords |
| "What did I work on last week?" | Grep with date filter |

---

## Usage Examples

### Search by Domain
```bash
/archive-query @loopwalker songs
# Searches all loopwalker conversations for "songs"
```

### Search by Time
```bash
/archive-query December positioning
# Searches December conversations for "positioning"
```

### Search by Topic
```bash
/archive-query "rap flow" "trap beats"
# Searches for conversations about rap flow and trap beats
```

### Complex Query
```bash
/archive-query @loopwalker December positioning brand
# Searches loopwalker domain, December, for positioning/brand topics
```

---

## Search Techniques

The skill uses multiple search strategies:

### 1. Frontmatter Search
Searches YAML frontmatter for structured data:
```bash
grep -r "domains.*loopwalker" ~/AI-CHAT-ARCHIVE/
grep -r "tags.*positioning" ~/AI-CHAT-ARCHIVE/
```

### 2. Content Search
Searches full transcript content:
```bash
grep -r "shadow integration" ~/AI-CHAT-ARCHIVE/
```

### 3. Date-Based Search
Filters by date in frontmatter:
```bash
grep -r "date: 2026-01" ~/AI-CHAT-ARCHIVE/
```

### 4. Combined Search
Uses Grep with complex patterns:
```bash
grep -r "domains.*loopwalker" ~/AI-CHAT-ARCHIVE/ | grep "2026-01"
```

---

## Archive Stats

Get stats by reading INDEX.md or running:

```bash
# Total conversations
find ~/AI-CHAT-ARCHIVE/ -name "*.md" -type f | wc -l

# By domain
grep -r "domains.*loopwalker" ~/AI-CHAT-ARCHIVE/ | wc -l

# Date range
ls -R ~/AI-CHAT-ARCHIVE/2026/
```

---

## Tips for Better Queries

1. **Use domain filters** - `@loopwalker` instead of "loopwalker"
2. **Quote phrases** - `"brand positioning"` instead of `brand positioning`
3. **Specify time** - Add month/year to narrow results
4. **Use tags** - Search tags field for common topics
5. **Start broad** - Begin with general term, then refine

---

## Related Skills

- `/archive` — Save current conversation to archive
- `/build` — Log work to build log
- `/idea` — Route ideas through Final Signal Path

---

## Archive System Docs

Full documentation: `AI-CHAT-ARCHIVE/README.md`
Configuration: `AI-CHAT-ARCHIVE/CONFIGURATION.md`
