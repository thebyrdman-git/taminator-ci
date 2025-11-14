#!/bin/bash
# Upload release files to GitLab via Git LFS (one at a time)
# This ensures large files are properly tracked and uploaded

set -e

VERSION="v2.1.2"
RELEASE_DIR="release/v2.1.2"

cd "$(dirname "$0")"

echo "🚀 Uploading TAMINATOR $VERSION release files via Git LFS"
echo "=========================================================="
echo ""

# Check if release directory exists
if [ ! -d "$RELEASE_DIR" ]; then
    echo "❌ Error: Release directory not found: $RELEASE_DIR"
    exit 1
fi

# Check Git LFS is installed
if ! command -v git-lfs &> /dev/null; then
    echo "❌ Error: Git LFS is not installed"
    echo "Install with: sudo dnf install git-lfs"
    exit 1
fi

# Initialize Git LFS if needed
git lfs install

# Function to upload one file
upload_file() {
    local file=$1
    local filename=$(basename "$file")
    
    echo "📦 Uploading: $filename"
    echo "   Size: $(du -h "$file" | cut -f1)"
    
    # Check if file is already tracked by LFS
    if git lfs ls-files | grep -q "$filename"; then
        echo "   ✅ Already tracked by LFS"
    else
        # Migrate file to LFS
        echo "   🔄 Migrating to LFS..."
        git lfs migrate import --include="$file" --everything
    fi
    
    # Stage and commit the file
    git add "$file"
    git commit -m "release: Add $filename for $VERSION

Size: $(du -h "$file" | cut -f1)
SHA256: $(sha256sum "$file" | cut -d' ' -f1)" --no-verify || echo "   ℹ️  No changes to commit"
    
    # Push to GitLab
    echo "   ⬆️  Pushing to GitLab CEE..."
    git push origin main
    
    echo "   ✅ $filename uploaded successfully!"
    echo ""
}

# Upload files one at a time
echo "Step 1/3: Uploading AppImage..."
if [ -f "$RELEASE_DIR/Taminator-2.1.2.AppImage" ]; then
    upload_file "$RELEASE_DIR/Taminator-2.1.2.AppImage"
else
    echo "⚠️  AppImage not found, skipping"
fi

echo "Step 2/3: Uploading DMG..."
if [ -f "$RELEASE_DIR/Taminator-2.1.2.dmg" ]; then
    upload_file "$RELEASE_DIR/Taminator-2.1.2.dmg"
else
    echo "⚠️  DMG not found, skipping"
fi

echo "Step 3/3: Uploading SHA256SUMS..."
if [ -f "$RELEASE_DIR/SHA256SUMS" ]; then
    upload_file "$RELEASE_DIR/SHA256SUMS"
else
    echo "⚠️  SHA256SUMS not found, skipping"
fi

echo "=========================================================="
echo "✅ All files uploaded successfully!"
echo ""
echo "Files are now available at:"
echo "  https://gitlab.cee.redhat.com/jbyrd/taminator/-/tree/main/release/v2.1.2"
echo ""
echo "📋 Next: Add these to your GitLab release"
echo "  https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v2.1.2/edit"

