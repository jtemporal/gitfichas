#!/bin/bash
# GitFichas Mermaid Generator Setup Script
# Run this in a fresh codespace to set up all dependencies

set -e  # Exit on any error

echo "🚀 Setting up GitFichas Mermaid Generator..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to the project root directory
cd "$PROJECT_ROOT"

# Check if we're in the right project structure
if [ ! -f "$PROJECT_ROOT/gitfichas-mermaid-theme.json" ]; then
    echo "❌ Error: GitFichas project structure not found"
    echo "   Script location: $SCRIPT_DIR"
    echo "   Project root: $PROJECT_ROOT"
    echo "   Expected file: $PROJECT_ROOT/gitfichas-mermaid-theme.json"
    exit 1
fi

echo "✅ Found project files"

# Check Node.js and npm
echo "📦 Checking Node.js and npm..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js first."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install npm first."
    exit 1
fi

echo "✅ Node.js $(node --version) and npm $(npm --version) found"

# Install system dependencies for headless Chrome/Puppeteer
echo "🖥️  Checking for OS-specific dependencies for headless Chrome..."

if [[ "$(uname)" == "Linux" ]]; then
    if command -v apt-get &> /dev/null; then
        echo "🐧 Detected Debian/Ubuntu-based Linux. Installing dependencies with apt-get..."
        # Update package list
        sudo apt-get update -qq

        # Install required libraries for Chrome/Puppeteer
        sudo apt-get install -y -qq \
            libasound2t64 \
            libatk-bridge2.0-0t64 \
            libatk1.0-0t64 \
            libdrm2 \
            libgtk-3-0t64 \
            libgbm1 \
            libnss3 \
            libxss1 \
            libxtst6 \
            xvfb

        echo "✅ System dependencies installed for Linux."
    else
        echo "⚠️  Detected Linux, but 'apt-get' is not found."
        echo "   Please manually install the required dependencies for headless Chrome/Puppeteer on your distribution."
    fi
elif [[ "$(uname)" == "Darwin" ]]; then
    echo "🍏 Detected macOS. No special system dependencies are typically required."
    echo "   The Mermaid CLI will download its own Chromium browser."
    echo "   If you encounter issues, ensure Xcode Command Line Tools are installed ('xcode-select --install')."
else
    echo "⚠️  Unsupported OS: $(uname). Please manually install dependencies for headless Chrome/Puppeteer."
    echo "   For Windows users, it is recommended to use WSL (Windows Subsystem for Linux), as the script is compatible with distributions that use 'apt'."
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    pip install -r "$PROJECT_ROOT/requirements.txt"
    echo "✅ Python dependencies installed"
else
    echo "⚠️  No requirements.txt found, installing PyYAML manually..."
    pip install PyYAML
fi

# Install Mermaid CLI
echo "🎨 Installing Mermaid CLI..."
if ! command -v npx &> /dev/null; then
    echo "❌ npx not found. Please ensure npm is properly installed."
    exit 1
fi

# Check if Mermaid CLI is already installed
if npx @mermaid-js/mermaid-cli --version &> /dev/null; then
    echo "✅ Mermaid CLI already installed: $(npx @mermaid-js/mermaid-cli --version)"
else
    echo "📥 Installing Mermaid CLI globally..."
    npm install -g @mermaid-js/mermaid-cli
    echo "✅ Mermaid CLI installed: $(npx @mermaid-js/mermaid-cli --version)"
fi

# Generate embedded fonts if needed
echo "🔤 Checking embedded fonts..."
if [ ! -f "$PROJECT_ROOT/assets/css/embedded-fonts.css" ]; then
    echo "📥 Generating embedded fonts..."
    python3 scripts/generate_embedded_fonts.py
    echo "✅ Embedded fonts generated"
else
    echo "✅ Embedded fonts already exist"
fi

# Install the card fonts (Mermaid needs them installed to measure text for the 16:9 cards)
echo "🔤 Installing card fonts..."
python3 scripts/generate_cards.py --install-fonts

# Test the setup
echo "🧪 Testing the setup..."
if python3 scripts/generate_cards.py --help &> /dev/null; then
    echo "✅ Script help command works"

    # Test actual image generation to catch Chrome/Puppeteer issues
    echo "🧪 Testing image generation..."
    if python3 scripts/generate_cards.py 001 --lang pt --force --output "$(mktemp -d)" &> /dev/null; then
        echo "✅ Image generation test passed!"
    else
        echo "⚠️  Image generation test failed, but basic script works."
        echo "   This might be due to missing system dependencies."
        echo "   Try running: python3 scripts/generate_cards.py 001 --force --verbose"
        echo "   If you see Chrome/Puppeteer errors, the system dependencies may need updating."
    fi
else
    echo "❌ Script test failed. Please check the error messages above."
    exit 1
fi

echo ""
echo "🎉 Setup complete! You can now use:"
echo "   cd $PROJECT_ROOT"
echo "   python3 scripts/generate_cards.py --help"
echo "   python3 scripts/generate_cards.py --verbose"
echo ""
echo "📚 For more information, see $PROJECT_ROOT/MERMAID_CONVERTER_README.md"
