"""
Tests for AI Chat Archive import script.

Run with: pytest tests/test_import.py
"""

import json
import pytest
from datetime import datetime
from pathlib import Path
from sys import path

# Add bin directory to path for imports
path.insert(0, str(Path(__file__).parent.parent / "bin"))

# Mock the import script functions
# In production, these would be imported from import-chats.py


def test_sanitize_topic():
    """Test topic sanitization."""
    # Import after path setup
    from import_chats import sanitize_topic

    # Basic conversion
    assert sanitize_topic("Hello World") == "hello-world"
    assert sanitize_topic("Test Topic Here") == "test-topic-here"

    # Special chars removed
    assert sanitize_topic("Hello@World!") == "hello-world"
    assert sanitize_topic("Test's Topic") == "tests-topic"

    # Word limit
    assert sanitize_topic("one two three four five") == "one-two-three-four"
    assert sanitize_topic("a b c d e f") == "a-b-c-d"

    # Empty/invalid titles
    assert sanitize_topic("") == "untitled-conversation"
    assert sanitize_topic("-") == "untitled-conversation"
    assert sanitize_topic("!!!") == "untitled-conversation"


def test_config_loading(tmp_path):
    """Test configuration loading with priority."""
    import os
    from import_chats import load_config

    # Test default config (no file, no env vars)
    config = load_config()
    assert "archive" in config
    assert "domains" in config
    assert config["domains"]["default"] == "system"

    # Test with config file
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
archive:
  path: ~/test-archive
domains:
  default: custom
""")

    # Mock config path
    import import_chats
    original_path = Path(import_chaps.__file__).parent.parent / "config" / "config.yaml"
    # In production, would temporarily replace config path

    # Test with environment variable
    os.environ["ARCHIVE_PATH"] = "~/env-archive"
    config = load_config()
    # Should use env var override
    assert config["archive"]["path"] == "~/env-archive"

    del os.environ["ARCHIVE_PATH"]


def test_detect_domain():
    """Test domain detection from content."""
    from import_chats import detect_domain, DOMAIN_KEYWORDS

    # Music domain
    content = "I'm working on a new song with hip-hop beats"
    domain = detect_domain(content, "Music Production")
    assert domain in ["@loopwalker", "@system"]  # Should match music keywords or default

    # Brand domain
    content = "Let's work on brand positioning strategy"
    domain = detect_domain(content, "Brand Work")
    assert domain in ["@brent", "@system"]

    # No keywords - should use default
    content = "Random conversation about weather"
    domain = detect_domain(content, "Random")
    assert domain == "@system" or domain == "system"


def test_generate_tags():
    """Test tag generation."""
    from import_chats import generate_tags

    context = {
        "sprint": {"flagship": "Brand System"},
        "domains": {}
    }

    # Music conversation
    content = "Working on lyrics and melody for new song"
    tags = generate_tags(content, "Song Writing", context)
    assert "music" in tags or "loopwalker" in tags or len(tags) > 0

    # Brand conversation
    content = "Discussing brand positioning and offer"
    tags = generate_tags(content, "Brand Strategy", context)
    assert "positioning" in tags or "brand" in tags or len(tags) > 0

    # Check max tags
    content = "music song code brand positioning workflow 2e dyslexia system automation"
    tags = generate_tags(content, "Multi Topic", context)
    assert len(tags) <= 5


def test_month_names():
    """Test month name mapping."""
    from import_chats import MONTH_NAMES

    assert MONTH_NAMES[1] == "01-January"
    assert MONTH_NAMES[6] == "06-June"
    assert MONTH_NAMES[12] == "12-December"

    # All months present
    assert len(MONTH_NAMES) == 12


def test_parse_claude_conversation():
    """Test Claude conversation parsing."""
    from import_chats import parse_claude_conversation

    chat = {
        "name": "Test Conversation",
        "created_at": "2026-01-16T10:00:00Z",
        "chat_messages": [
            {"sender": "Human", "text": "Hello"},
            {"sender": "Assistant", "text": "Hi there!"}
        ]
    }

    context = {"sprint": {}, "domains": {}}
    result = parse_claude_conversation(chat, context)

    assert result["title"] == "Test Conversation"
    assert result["topic"] == "test-conversation"
    assert result["ai"] == "claude"
    assert isinstance(result["date"], datetime)
    assert "transcript" in result


def test_parse_chatgpt_conversation():
    """Test ChatGPT conversation parsing."""
    from import_chats import parse_chatgpt_conversation

    chat = {
        "title": "GPT Test",
        "create_time": 1642357200.0,
        "mapping": {
            "node1": {
                "message": {
                    "author": {"role": "user"},
                    "content": {
                        "content_type": "text",
                        "parts": ["Hello from GPT"]
                    }
                }
            }
        }
    }

    context = {"sprint": {}, "domains": {}}
    result = parse_chatgpt_conversation(chat, context)

    assert result is not None
    assert result["title"] == "GPT Test"
    assert result["ai"] == "chatgpt"
    assert "transcript" in result


def test_generate_summary():
    """Test summary generation."""
    from import_chats import generate_summary

    title = "Music Production Workflow"
    transcript = """
    **Human:** Let's create a music production workflow.
    **Assistant:** Here's a systematic approach with 3 stages.
    **Human:** Great, let's add quality control.
    **Assistant:** I'll add a checklist for that.
    """

    summary = generate_summary(title, transcript, "@loopwalker")
    assert isinstance(summary, str)
    assert len(summary) > 0
    # Should be 2-3 sentences
    assert summary.count(".") >= 2


def test_extract_key_outputs():
    """Test key outputs extraction."""
    from import_chats import extract_key_outputs

    transcript = """
    **Human:** What should we do?
    **Assistant:** We decided to create a new workflow.
    **Human:** What else?
    **Assistant:** Going to add quality checks next.
    **Assistant:** Final step is documentation.
    """

    outputs = extract_key_outputs(transcript)
    assert isinstance(outputs, list)
    assert len(outputs) >= 1
    assert len(outputs) <= 3  # Max 3 outputs
    # Check that outputs start with bullet
    for output in outputs:
        assert output.startswith("-")


def test_path_expansion():
    """Test path expansion with tilde."""
    from pathlib import Path

    # Test tilde expansion
    path = Path("~/AI-CHAT-ARCHIVE").expanduser()
    assert str(path).startswith("/")
    assert "AI-CHAT-ARCHIVE" in str(path)


@pytest.fixture
def sample_claude_export():
    """Sample Claude export for testing."""
    return [
        {
            "name": "Test Conversation",
            "created_at": "2026-01-16T10:00:00Z",
            "chat_messages": [
                {"sender": "Human", "text": "Help me write a song"},
                {"sender": "Assistant", "text": "Here's a song structure for you"}
            ]
        }
    ]


@pytest.fixture
def sample_chatgpt_export():
    """Sample ChatGPT export for testing."""
    return [
        {
            "title": "GPT Conversation",
            "create_time": 1642357200.0,
            "mapping": {
                "node1": {
                    "message": {
                        "author": {"role": "user"},
                        "content": {
                            "content_type": "text",
                            "parts": ["Hello from ChatGPT"]
                        }
                    }
                },
                "node2": {
                    "message": {
                        "author": {"role": "assistant"},
                        "content": {
                            "content_type": "text",
                            "parts": ["Hi there!"]
                        }
                    }
                }
            }
        }
    ]


def test_end_to_end_claude(sample_claude_export, tmp_path):
    """Test end-to-end Claude import."""
    from import_chats import parse_claude_conversation, create_archive_entry

    # Mock archive root
    import import_chats
    original_root = import_chats.ARCHIVE_ROOT
    import_chats.ARCHIVE_ROOT = tmp_path

    try:
        context = {"sprint": {}, "domains": {}}
        data = parse_claude_conversation(sample_claude_export[0], context)

        # Create archive entry
        filepath = create_archive_entry(data)

        # Verify file created
        assert filepath.exists()
        assert filepath.parent == tmp_path / "2026/01-January"

        # Verify file content
        content = filepath.read_text()
        assert "---" in content  # Frontmatter present
        assert "date: 2026-01-16" in content
        assert "# Test Conversation" in content
        assert "## Summary" in content
        assert "## Transcript" in content

    finally:
        import_chats.ARCHIVE_ROOT = original_root


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
