#!/bin/bash
# Claude Code Skills Installer
#
# Installs AI Chat Archive skills to Claude Code

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$PROJECT_ROOT/claude-skills"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"

echo "================================"
echo "AI Chat Archive Skills Installer"
echo "================================"
echo ""

# Check if skills directory exists
if [ ! -d "$SKILLS_DIR" ]; then
    echo -e "${RED}Error: Skills directory not found: $SKILLS_DIR${NC}"
    echo "Make sure you're running this script from the AI-CHAT-ARCHIVE repository."
    exit 1
fi

# Check if Claude Code skills directory exists
if [ ! -d "$CLAUDE_SKILLS_DIR" ]; then
    echo "Creating Claude Code skills directory: $CLAUDE_SKILLS_DIR"
    mkdir -p "$CLAUDE_SKILLS_DIR"
fi

# Function to install a skill
install_skill() {
    local skill_name=$1
    local skill_source="$SKILLS_DIR/$skill_name"
    local skill_target="$CLAUDE_SKILLS_DIR/$skill_name"

    echo -n "Installing $skill_name... "

    if [ -L "$skill_target" ]; then
        # Already a symlink, remove it
        rm "$skill_target"
    elif [ -e "$skill_target" ]; then
        # Exists but not a symlink, back it up
        backup="${skill_target}.backup.$(date +%Y%m%d%H%M%S)"
        mv "$skill_target" "$backup"
        echo -e "${YELLOW}(backed up to $backup)${NC}"
        echo -n "  Installing $skill_name... "
    fi

    # Create symlink
    ln -s "$skill_source" "$skill_target"
    echo -e "${GREEN}✓${NC}"
}

# Install skills
install_skill "archive"
install_skill "archive-query"

echo ""
echo "================================"
echo -e "${GREEN}Installation complete!${NC}"
echo "================================"
echo ""
echo "Installed skills:"
echo "  - /archive      — Archive current conversation"
echo "  - /archive-query — Search archived conversations"
echo ""
echo "Skills location: $CLAUDE_SKILLS_DIR"
echo "Project location: $PROJECT_ROOT"
echo ""
echo "To uninstall, run:"
echo "  rm $CLAUDE_SKILLS_DIR/archive"
echo "  rm $CLAUDE_SKILLS_DIR/archive-query"
echo ""
echo "For usage, see:"
echo "  - QUICKSTART.md"
echo "  - claude-skills/archive/SKILL.md"
echo "  - claude-skills/archive-query/SKILL.md"
