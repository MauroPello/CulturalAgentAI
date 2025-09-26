#!/bin/bash

# Quick test setup script for Cultural Agent Firefox Extension

echo "🧪 Cultural Agent Extension - Quick Test Setup"
echo "=============================================="
echo ""

# Check if Firefox is installed
if command -v firefox &> /dev/null; then
    echo "✅ Firefox found"
else
    echo "❌ Firefox not found. Please install Firefox to test the extension."
    exit 1
fi

# Get the extension directory
EXTENSION_DIR="/home/mattia/Documents/GitHub/CulturalAgentAI/web_extension"
TEST_PAGE="$EXTENSION_DIR/test-page.html"

echo "📁 Extension directory: $EXTENSION_DIR"
echo ""

# Check if all required files exist
echo "🔍 Checking extension files..."
required_files=("manifest.json" "background.js" "content.js" "popup.html" "popup.js")
missing_files=()

for file in "${required_files[@]}"; do
    if [[ -f "$EXTENSION_DIR/$file" ]]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (missing)"
        missing_files+=("$file")
    fi
done

if [[ ${#missing_files[@]} -gt 0 ]]; then
    echo ""
    echo "❌ Missing required files. Please ensure all extension files are present."
    exit 1
fi

echo ""
echo "🚀 Ready to test! Follow these steps:"
echo ""
echo "1. Open Firefox"
echo "2. Go to: about:debugging"
echo "3. Click 'This Firefox' in the sidebar"
echo "4. Click 'Load Temporary Add-on...'"
echo "5. Navigate to: $EXTENSION_DIR"
echo "6. Select: manifest.json"
echo "7. Click 'Open'"
echo ""
echo "📄 Test page available at:"
echo "   file://$TEST_PAGE"
echo ""
echo "🔧 To open test page automatically:"
echo "   firefox '$TEST_PAGE'"
echo ""
echo "📚 For detailed testing instructions:"
echo "   cat '$EXTENSION_DIR/TESTING.md'"
echo ""

# Ask if user wants to open test page
read -p "Would you like to open the test page in Firefox now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌐 Opening test page in Firefox..."
    firefox "$TEST_PAGE" &
    echo "✅ Test page opened!"
    echo ""
    echo "💡 Remember to install the extension first using the steps above!"
fi

echo ""
echo "Happy testing! 🎉"