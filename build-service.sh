#!/bin/bash
# Build Taminator Service with custom spec (excludes system libraries)

set -e

echo "🔨 Building Taminator Service (glibc-compatible)..."

# Check if PyInstaller is installed
if ! python3 -m PyInstaller --version &> /dev/null; then
    echo "📦 Installing PyInstaller..."
    pip3 install --user pyinstaller
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/taminator-service

# Build the service binary with custom spec
echo "🏗️  Building service binary with custom spec..."
python3 -m PyInstaller taminator-service.spec --clean

# Check if build succeeded
if [ -f "dist/taminator-service" ]; then
    echo "✅ Service binary built successfully"
    
    # Check glibc requirements
    echo "🔍 Checking glibc requirements..."
    ldd dist/taminator-service | grep GLIBC || echo "No GLIBC symbols found"
    
    # Test the binary
    echo "🧪 Testing binary..."
    ./dist/taminator-service --help 2>&1 | head -5 || echo "Service binary ready"
    
    echo ""
    echo "✅ Build complete!"
    echo "📦 Binary location: $(pwd)/dist/taminator-service"
    echo "📏 Binary size: $(du -h dist/taminator-service | cut -f1)"
    echo ""
    echo "Next step: cd gui && npm run build"
else
    echo "❌ Build failed - service binary not found in dist/"
    exit 1
fi

