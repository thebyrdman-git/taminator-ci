#!/bin/bash
# Push GitHub Actions configuration to taminator-ci repository

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   🚀 PUSH GITHUB ACTIONS TO TAMINATOR-CI                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

cd /home/jbyrd/pai/taminator

echo "📍 Current directory: $(pwd)"
echo "📍 Current branch: $(git branch --show-current)"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 1: Check Git Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
git status

echo ""
read -p "Continue with commit? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Aborted by user"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 2: Stage Changes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
git add gui/package.json
git add .github/workflows/release.yml
git add GITHUB-ACTIONS-SETUP-COMPLETE.md
git add push-github-actions.sh
echo "✅ Files staged"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 3: Commit Changes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
git commit -m "feat: Add automated cross-platform builds for all platforms

- Add Linux AppImage build (was missing)
- Add Python dependency installation
- Add platform-specific build scripts to package.json
- Update release workflow to build Linux, Windows, macOS
- Add release notes support
- Add push script and documentation"
echo "✅ Committed"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 4: Push to taminator-ci"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Pushing to: taminator-ci"
echo ""

if git push taminator-ci $(git branch --show-current):main; then
    echo "✅ Successfully pushed to taminator-ci"
else
    echo "⚠️ Push failed. Try manually:"
    echo "   git push taminator-ci $(git branch --show-current):main"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 5: Create and Push v1.9.2 Tag"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Create v1.9.2 tag and trigger build? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating tag v1.9.2..."
    
    # Delete tag if it exists locally
    git tag -d v1.9.2 2>/dev/null || true
    
    # Create new tag
    git tag v1.9.2
    
    # Push tag
    echo "Pushing tag to taminator-ci..."
    git push taminator-ci v1.9.2 --force
    
    echo "✅ Tag v1.9.2 pushed"
    echo ""
    echo "🎉 GitHub Actions will now build:"
    echo "   - Linux AppImage"
    echo "   - Windows NSIS Installer"
    echo "   - macOS Universal DMG"
    echo ""
    echo "📊 Monitor build:"
    echo "   https://github.com/thebyrdman-git/taminator-ci/actions"
    echo ""
    echo "📦 Release will be here:"
    echo "   https://github.com/thebyrdman-git/taminator-ci/releases/tag/v1.9.2"
else
    echo "⏭️  Skipped tag creation. You can create it later:"
    echo "   git tag v1.9.2"
    echo "   git push taminator-ci v1.9.2"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   ✅ COMPLETE - GitHub Actions Configured                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📝 See GITHUB-ACTIONS-SETUP-COMPLETE.md for details"
echo ""

