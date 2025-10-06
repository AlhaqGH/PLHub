#!/usr/bin/env bash
# ============================================================================
# PLHub Installation Script for Linux/macOS
# ============================================================================
# This script installs PLHub and makes it globally accessible
# Usage: ./install.sh
# ============================================================================

set -e

echo ""
echo "╔════════════════════════════════════════╗"
echo "║   PLHUB INSTALLATION FOR LINUX/MACOS   ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Get the directory where PLHub is located
PLHUB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "⏳ Installing PLHub..."
echo "   Location: $PLHUB_ROOT"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo ""
    echo "Please install Python 3.8 or higher first:"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   macOS: brew install python3"
    echo "   Fedora: sudo dnf install python3 python3-pip"
    echo ""
    exit 1
fi

echo "✅ Python found"
python3 --version
echo ""

# Install Python dependencies
echo "⏳ Installing Python dependencies..."
if pip3 install -r "$PLHUB_ROOT/requirements.txt" > /dev/null 2>&1; then
    echo "✅ Dependencies installed"
else
    echo "⚠️  Some dependencies may have issues, but continuing..."
fi
echo ""

# Make plhub.sh executable
chmod +x "$PLHUB_ROOT/plhub.sh"
echo "✅ plhub.sh made executable"
echo ""

# Create symlink in user's local bin
LOCAL_BIN="$HOME/.local/bin"
mkdir -p "$LOCAL_BIN"

# Remove old symlink if exists
if [ -L "$LOCAL_BIN/plhub" ]; then
    rm "$LOCAL_BIN/plhub"
fi

# Create symlink
ln -s "$PLHUB_ROOT/plhub.sh" "$LOCAL_BIN/plhub"
echo "✅ Created symlink: $LOCAL_BIN/plhub"
echo ""

# Check if LOCAL_BIN is in PATH
if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
    echo "⚠️  $LOCAL_BIN is not in your PATH"
    echo ""
    echo "Add this line to your shell configuration:"
    echo ""
    
    # Detect shell
    if [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    else
        SHELL_RC="$HOME/.profile"
    fi
    
    echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "To your shell configuration file: $SHELL_RC"
    echo ""
    
    # Offer to add automatically
    read -p "Add to $SHELL_RC automatically? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "" >> "$SHELL_RC"
        echo "# Added by PLHub installer" >> "$SHELL_RC"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"
        echo "✅ Added to $SHELL_RC"
        echo "   Run: source $SHELL_RC"
    fi
else
    echo "✅ $LOCAL_BIN is already in PATH"
fi

echo ""
echo "╔════════════════════════════════════════╗"
echo "║      INSTALLATION SUCCESSFUL! ✓        ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "PLHub has been installed successfully!"
echo ""
echo "📍 Installation Location: $PLHUB_ROOT"
echo "🔧 Command: plhub"
echo ""
echo "✨ You can now use PLHub from anywhere:"
echo ""
echo "   plhub run app.poh"
echo "   plhub build apk --release"
echo "   plhub build apk --debug"
echo "   plhub create my-app"
echo "   plhub doctor"
echo ""
echo "⚠️  IMPORTANT: Reload your shell or run:"
echo "   source $SHELL_RC"
echo ""
echo "📚 Documentation: $PLHUB_ROOT/docs/"
echo "🚀 Quick Start: $PLHUB_ROOT/docs/ANDROID_QUICKSTART.md"
echo ""
echo "Test installation with: plhub --version"
echo ""
