# Contributing Guide

Thank you for considering contributing to the AI Chat Archive!

## Ways to Contribute

- **Report bugs** - Open an issue with details
- **Suggest features** - Share ideas for improvements
- **Submit code** - Pull requests for bug fixes or features
- **Improve docs** - Fix typos, add examples, clarify explanations
- **Share configs** - Submit custom domain configurations

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/yourusername/ai-chat-archive.git
cd ai-chat-archive
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
# or
pip install pyyaml anthropic pytest
```

### 4. Run Tests

```bash
pytest tests/
```

### 5. Make Changes

Create a feature branch:

```bash
git checkout -b feature/your-feature-name
```

## Code Style

Follow these conventions:

### Python

- Use 4 spaces for indentation
- Max line length: 100 characters
- Follow PEP 8 where practical
- Use type hints for function signatures

### Example

```python
def parse_conversation(chat: Dict, context: Dict) -> Optional[Dict]:
    """Parse a conversation from JSON export.

    Args:
        chat: Raw chat data from export
        context: Human OS context (if enabled)

    Returns:
        Parsed conversation data or None if invalid
    """
    if not chat.get("name"):
        return None

    return {
        "title": chat["name"],
        "date": parse_date(chat),
    }
```

### Documentation

- Use clear, concise language
- Include examples for complex features
- Update relevant docs when changing behavior
- Add "PR #" references to close related issues

## Testing

### Write Tests

Add tests for new features in `tests/test_import.py`:

```python
def test_new_feature():
    """Test new feature description."""
    result = new_function(input_data)
    assert result == expected_output
```

### Test Fixtures

Add sample data in `tests/fixtures/`:

- `sample-claude-export.json`
- `sample-chatgpt-export.json`
- `expected-output.md`

### Run Tests

```bash
# All tests
pytest tests/

# Specific test
pytest tests/test_import.py::test_sanitize_topic

# With coverage
pytest --cov=bin tests/

# Verbose output
pytest -v tests/
```

## Pull Request Process

### 1. Update Tests

Ensure all tests pass:

```bash
pytest tests/
```

### 2. Update Documentation

If changing behavior:
- Update README.md if user-facing
- Update relevant docs in docs/
- Add examples to QUICKSTART.md if helpful

### 3. Commit Changes

Use conventional commits:

```
feat: add support for custom export formats
fix: handle missing created_at field gracefully
docs: update QUICKSTART with new configuration
test: add tests for domain detection edge cases
refactor: simplify config loading logic
```

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear title describing the change
- Description of what you changed and why
- Link to related issues (fixes #123)
- Screenshots if applicable (UI changes)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Added tests for new features
- [ ] All tests pass locally
- [ ] Manual testing completed

## Related Issues
Fixes #123
Related to #456

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
```

## Feature Guidelines

### Small Changes

Bug fixes, small improvements:
- Just submit a PR
- Include tests if applicable

### Medium Changes

New features, refactoring:
1. Open an issue first to discuss
2. Get feedback on approach
3. Submit PR with tests

### Large Changes

Major new features, breaking changes:
1. Open an issue to discuss
2. Wait for approval
3. Create design document (if complex)
4. Implement with comprehensive tests
5. Submit PR for review

## Documentation Contributions

### Typos and Small Fixes

Just submit a PR with the fix.

### Adding Examples

Greatly appreciated! Add to:
- QUICKSTART.md - Common workflows
- IMPORT.md - Export/import examples
- docs/CUSTOM_DOMAINS.md - Domain examples

### New Documentation

If adding new docs:
1. Use clear headings (# ## ###)
2. Include code examples with syntax highlighting
3. Add "Last updated" date at bottom
4. Link from relevant sections

## Reporting Issues

### Bug Reports

Use the bug report template with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python version)
- Error messages
- Config (sanitized)

### Feature Requests

Use the feature request template with:
- Problem statement
- Proposed solution
- Alternatives considered
- Use cases

## Community Guidelines

- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes for significant contributions
- Credited in relevant documentation

## Questions?

- Open a discussion on GitHub
- Ask in an existing issue
- Check existing documentation first

---

Thank you for contributing! 🎉
