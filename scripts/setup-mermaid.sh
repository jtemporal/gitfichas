#!/bin/bash
# GitFichas Mermaid Generator Setup Script
# Run this in a fresh codespace to set up all dependencies

set -e  # Exit on any error

echo "🚀 Setting up GitFichas Mermaid Generator..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to the scripts directory
cd "$SCRIPT_DIR"

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
    python3 generate_embedded_fonts.py
    echo "✅ Embedded fonts generated"
else
    echo "✅ Embedded fonts already exist"
fi

# Test the setup
echo "🧪 Testing the setup..."
if python3 generate_images_only.py --help &> /dev/null; then
    echo "✅ Script is working correctly!"
else
    echo "❌ Script test failed. Please check the error messages above."
    exit 1
fi

echo ""
echo "🎉 Setup complete! You can now use:"
echo "   cd $SCRIPT_DIR"
echo "   python3 generate_images_only.py --help"
echo "   python3 generate_images_only.py --verbose"
echo "   python3 generate_embedded_fonts.py"
echo ""
echo "📚 For more information, see $PROJECT_ROOT/MERMAID_CONVERTER_README.md"
