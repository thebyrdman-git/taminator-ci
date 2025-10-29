#!/bin/bash
# Build tam-rfe CLI as standalone binary using PyInstaller

set -e

echo "🔨 Building Taminator CLI Binary..."

# Check if PyInstaller is installed
if ! python3 -m PyInstaller --version &> /dev/null; then
    echo "📦 Installing PyInstaller..."
    pip3 install pyinstaller
fi

# Check if dependencies are installed
echo "📦 Installing Taminator dependencies..."
pip3 install -r requirements.txt

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/

# Build the binary
echo "🏗️  Building binary with PyInstaller..."
python3 -m PyInstaller build-cli.spec

# Check if build succeeded
if [ -f "dist/tam-rfe" ]; then
    echo "✅ Binary built successfully: dist/tam-rfe"
    
    # Test the binary
    echo "🧪 Testing binary..."
    ./dist/tam-rfe --help
    
    echo ""
    echo "✅ Build complete!"
    echo "📦 Binary location: $(pwd)/dist/tam-rfe"
    echo "📏 Binary size: $(du -h dist/tam-rfe | cut -f1)"
    echo ""
    echo "Next steps:"
    echo "1. Copy binary to gui/bin/: mkdir -p gui/bin && cp dist/tam-rfe gui/bin/"
    echo "2. Rebuild Electron app: cd gui && npm run build"
else
    echo "❌ Build failed - binary not found in dist/"
    exit 1
fi

