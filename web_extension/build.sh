#!/bin/bash

# Build script for Cultural Agent Firefox Extension

echo "🤖 Building Cultural Agent Firefox Extension..."

# Create build directory
BUILD_DIR="build"
EXTENSION_DIR="/home/mattia/Documents/GitHub/CulturalAgentAI/web_extension"

# Remove existing build directory
if [ -d "$BUILD_DIR" ]; then
    rm -rf "$BUILD_DIR"
fi

# Create fresh build directory
mkdir -p "$BUILD_DIR"

echo "📦 Copying extension files..."

# Copy all necessary files
cp manifest.json "$BUILD_DIR/"
cp background.js "$BUILD_DIR/"
cp content.js "$BUILD_DIR/"
cp content.css "$BUILD_DIR/"
cp popup.html "$BUILD_DIR/"
cp popup.css "$BUILD_DIR/"
cp popup.js "$BUILD_DIR/"
cp -r icons "$BUILD_DIR/"

echo "🗜️  Creating ZIP package..."

# Create ZIP file for distribution
cd "$BUILD_DIR"
zip -r ../cultural-agent-extension.zip . -x "*.DS_Store"
cd ..

echo "✅ Extension built successfully!"
echo "📁 Files copied to: $BUILD_DIR/"
echo "📦 ZIP package created: cultural-agent-extension.zip"
echo ""
echo "To install in Firefox:"
echo "1. Open Firefox and go to about:debugging"
echo "2. Click 'This Firefox'"
echo "3. Click 'Load Temporary Add-on'"
echo "4. Select manifest.json from the build directory"
echo ""
echo "🚀 Happy coding!"