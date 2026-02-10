# Custom Domain Configuration

## Understanding Domains

Domains are categories for organizing your AI conversations. Each domain has:
- **Name** - e.g., `loopwalker`, `brent`, `gal`
- **Keywords** - Words that trigger domain detection
- **@-prefix** - Used in tags and file organization

## Default Domains

The archive comes with these predefined domains:

| Domain | Keywords |
|--------|----------|
| `@loopwalker` | music, song, loopwalker, shadow work, frequency, audio, lyrics, melody |
| `@pulsekeeper` | heart, coherence, adhd, 2e, frequency, nervous system, regulation |
| `@shadow-institute` | dyslexia, twice-exceptional, 2e, gifted, neurodivergent, learning difference |
| `@unlimited-band` | band, collaboration, music group, bandmate |
| `@brent` | hyperfocus, dyslexia, pattern recognition, brand, positioning, website |
| `@gal` | connection, outreach, networking, crm, warm, dm, comment |
| `@system` | sprint, workflow, process, system, automation, skill |

## Creating Custom Domains

### Step 1: Define Your Domain

Choose a name and relevant keywords.

**Example: Writing Domain**
```yaml
"@writing":
  - blog
  - article
  - essay
  - copy
  - content writing
  - editing
```

### Step 2: Add to Configuration

**Option A: Edit config.yaml directly**

```yaml
domains:
  default: system
  custom:
    "@writing":
      - blog
      - article
      - essay
      - copy
      - content writing
      - editing
```

**Option B: Edit config.yaml.example (for templates)**

Add your custom domain so others can use it as a starting point.

### Step 3: Test Domain Detection

Create a test conversation with your keywords and run:

```bash
./import-chats.py --sample --count 1
```

Check the output file:
```yaml
---
domains: ["writing"]  # Should match your domain
tags: ["writing", "blog"]  # Should include domain tag
---
```

## Domain Keyword Strategy

### Keyword Selection Tips

1. **Be specific** - "music" is too broad, "hip-hop production" is better
2. **Use variations** - include singular/plural, abbreviations
3. **Avoid overlap** - don't use "brand" for both @brent and @gal
4. **Test real content** - use words from your actual conversations

### Example: Music Production Domain

**Too broad:**
```yaml
"@music":
  - music
  - audio
```

**Better:**
```yaml
"@music-production":
  - beat
  - production
  - mixing
  - mastering
  - daw
  - ableton
  - logic pro
  - fl studio
```

## Managing Domain Conflicts

### Problem: Overlapping Keywords

```yaml
"@brent":
  - brand

"@gal":
  - brand
```

**Solution: Be more specific**

```yaml
"@brent":
  - brand strategy
  - personal brand
  - positioning

"@gal":
  - brand outreach
  - connection
  - networking
```

### Problem: False Positives

**Issue:** Conversations about "system" keep getting tagged as `@system`

**Solution:**
1. Add context keywords to `@system`
2. Remove generic terms
3. Create more specific domains

```yaml
# Before
"@system":
  - system
  - automation

# After
"@system":
  - sprint planning
  - workflow automation
  - build system
  - devops
```

## Domain Hierarchies

You can create sub-domains using naming conventions:

```yaml
# Top-level domain
"@writing":
  - blog
  - article
  - essay

# Sub-domain (specific type)
"@writing-fiction":
  - novel
  - short story
  - fiction
  - character

# Sub-domain (specific type)
"@writing-technical":
  - documentation
  - technical writing
  - api docs
  - tutorial
```

## Removing Default Domains

If you don't use certain domains, you can remove them:

```yaml
domains:
  default: system
  custom:
    # Keep only what you use
    "@writing":
      - blog
      - article
    "@coding":
      - python
      - javascript
    # Remove @loopwalker, @brent, etc.
```

## Dynamic Domain Loading (Human OS)

If you use Human OS integration, domains are loaded from your INDEX files:

```yaml
human_os:
  enabled: true
  domains:
    - loopwalker
    - brent
    - gal
    # Only load domains you have INDEX files for
```

The domain keywords in `config.yaml` are still used for detection.

## Testing Domain Changes

### 1. Test with Sample Content

Create `test-conversation.json`:
```json
[
  {
    "name": "Test Blog Post",
    "created_at": "2026-01-16T10:00:00Z",
    "chat_messages": [
      {"sender": "Human", "text": "Help me write a blog post about music production"},
      {"sender": "Assistant", "text": "Here's an outline for your blog post..."}
    ]
  }
]
```

### 2. Run Sample Import

```bash
./import-chats.py --sample --count 1 --source claude
```

### 3. Check Output

Look at the generated file's frontmatter:
```yaml
domains: ["writing"]  # Should match expected domain
tags: ["writing", "blog", "music"]  # Should include relevant tags
```

### 4. Adjust Keywords

If domain is wrong, adjust keywords in config and retest.

## Example Configurations

### Minimal Setup (3 domains)

```yaml
domains:
  default: system
  custom:
    "@work":
      - project
      - meeting
      - deadline
      - deliverable
    "@personal":
      - fitness
      - health
      - family
      - personal
    "@learning":
      - tutorial
      - course
      - study
      - learn
```

### Content Creator Setup

```yaml
domains:
  default: system
  custom:
    "@youtube":
      - video
      - youtube
      - thumbnail
      - script
    "@blog":
      - blog post
      - article
      - seo
      - content
    "@social":
      - tweet
      - instagram
      - linkedin
      - social media
```

### Developer Setup

```yaml
domains:
  default: system
  custom:
    "@frontend":
      - react
      - vue
      - css
      - html
      - ui
    "@backend":
      - api
      - database
      - server
      - microservice
    "@devops":
      - docker
      - kubernetes
      - ci/cd
      - deployment
```

---

**Need help?** See [CONFIGURATION.md](../CONFIGURATION.md) or [open an issue](https://github.com/yourusername/ai-chat-archive/issues)
