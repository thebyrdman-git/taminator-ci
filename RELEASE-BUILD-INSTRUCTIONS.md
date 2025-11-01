# Taminator Release Build Instructions

**Version**: 2.0.1  
**Date**: 2025-11-01  
**Platforms**: Linux, macOS

---

## 🚀 Quick Release

### Automated (Ansible)

```bash
cd /home/jbyrd/TAMINATOR
ansible-playbook ansible/playbooks/taminator-release.yml
```

This will:
- ✅ Run all pre-release checks
- ✅ Bump version to 2.0.1
- ✅ Build for Linux (AppImage)
- ✅ Build for macOS (DMG + ZIP)
- ✅ Generate release notes
- ✅ Create checksums
- ✅ Prepare for git tagging

---

## 📦 Manual Build Process

### Prerequisites

```bash
# Install electron-builder
cd gui
npm install --save-dev electron-builder

# For macOS builds on Linux, you'll need:
# (Note: macOS builds work best on macOS, but can be done on Linux)
```

### Build for Linux

```bash
cd gui
npx electron-builder --linux AppImage
```

**Output**: `gui/dist/*.AppImage`

### Build for macOS

```bash
cd gui

# Build DMG (installer)
npx electron-builder --mac dmg

# Build ZIP (portable)
npx electron-builder --mac zip
```

**Output**: 
- `gui/dist/*.dmg` - macOS installer
- `gui/dist/*-mac.zip` - macOS portable

### Build for Both

```bash
cd gui
npx electron-builder --linux AppImage --mac dmg zip
```

---

## 🏗️ Build Configuration

### package.json Build Section

```json
{
  "name": "taminator",
  "version": "2.0.1",
  "build": {
    "appId": "com.redhat.taminator",
    "productName": "Taminator",
    "directories": {
      "output": "dist"
    },
    "files": [
      "main.js",
      "service-manager.js",
      "public/**/*",
      "!public/**/*.map"
    ],
    "linux": {
      "target": ["AppImage"],
      "category": "Utility",
      "icon": "public/img/icon.png"
    },
    "mac": {
      "target": ["dmg", "zip"],
      "category": "public.app-category.productivity",
      "icon": "public/img/icon.icns",
      "hardenedRuntime": true,
      "gatekeeperAssess": false,
      "entitlements": "entitlements.mac.plist",
      "entitlementsInherit": "entitlements.mac.plist"
    }
  }
}
```

Add this to `gui/package.json` if not present.

---

## 📋 Release Checklist

### Pre-Release

- [x] All bugs fixed (10/10)
- [x] ESLint passing (0 errors)
- [x] Service tested
- [x] Version bumped
- [ ] CHANGELOG updated
- [ ] Release notes generated

### Build

- [ ] Linux AppImage built
- [ ] macOS DMG built
- [ ] macOS ZIP built
- [ ] All builds tested
- [ ] Checksums created

### Post-Build

- [ ] Test Linux build
- [ ] Test macOS build (on macOS)
- [ ] Sign macOS build (if certificate available)
- [ ] Create GitHub release
- [ ] Upload artifacts
- [ ] Announce release

---

## 🍎 macOS Specific Notes

### Code Signing (Optional but Recommended)

If you have an Apple Developer certificate:

```bash
# Set environment variables
export APPLEID="your@email.com"
export APPLEIDPASS="app-specific-password"

# Build with signing
npx electron-builder --mac dmg --publish never
```

### Notarization (Required for macOS 10.15+)

```bash
# After building, notarize
xcrun notarytool submit Taminator-2.0.1.dmg \
  --apple-id your@email.com \
  --password app-specific-password \
  --team-id TEAM_ID
```

### Without Code Signing

Users will need to:
1. Download the DMG/ZIP
2. Right-click and select "Open"
3. Confirm they want to open it

Add this to the release notes.

---

## 🐧 Linux Specific Notes

### AppImage

- **Advantages**: Single file, no installation needed
- **Usage**: `chmod +x Taminator-2.0.1.AppImage && ./Taminator-2.0.1.AppImage`
- **Integration**: Can be integrated with AppImageLauncher

### Distribution

```bash
# Make executable
chmod +x Taminator-2.0.1.AppImage

# Test
./Taminator-2.0.1.AppImage

# Optional: Extract
./Taminator-2.0.1.AppImage --appimage-extract
```

---

## 📊 Expected Output Files

### Linux

```
Taminator-2.0.1.AppImage          (~136 MB)
Taminator-2.0.1-x86_64.AppImage   (alternative name)
```

### macOS

```
Taminator-2.0.1.dmg               (~120 MB) - Installer
Taminator-2.0.1-mac.zip           (~115 MB) - Portable
```

### Checksums

```
SHA256SUMS                        - All checksums
```

---

## 🔍 Verification

### Verify Checksums

```bash
cd releases/v2.0.1
sha256sum -c SHA256SUMS
```

### Test Builds

**Linux**:
```bash
./Taminator-2.0.1.AppImage
```

**macOS**:
```bash
# Mount DMG
open Taminator-2.0.1.dmg
# Or extract ZIP
unzip Taminator-2.0.1-mac.zip
open Taminator.app
```

---

## 🚨 Common Issues

### electron-builder Not Found

```bash
cd gui
npm install --save-dev electron-builder
```

### macOS Build on Linux Fails

This is expected for some features. Options:
1. Build on macOS (recommended)
2. Use CI/CD with macOS runner
3. Build unsigned (users need to right-click → Open)

### AppImage Won't Run

```bash
# Make executable
chmod +x *.AppImage

# Check FUSE
modprobe fuse

# Or extract and run
./Taminator-2.0.1.AppImage --appimage-extract
./squashfs-root/AppRun
```

---

## 📤 Distribution

### GitHub Release

```bash
# Create release
gh release create v2.0.1 \
  --title "v2.0.1 - Hotfix Release" \
  --notes-file RELEASE-NOTES-2.0.1.md \
  releases/v2.0.1/*
```

### Manual Upload

1. Go to GitHub Releases
2. Draft new release
3. Tag: `v2.0.1`
4. Upload files from `releases/v2.0.1/`
5. Publish

### Internal Distribution

```bash
# Upload to server
scp releases/v2.0.1/* server:/var/www/downloads/taminator/

# Or use rsync
rsync -av releases/v2.0.1/ server:/var/www/downloads/taminator/v2.0.1/
```

---

## 📝 Release Announcement Template

```markdown
# Taminator v2.0.1 Released! 🎉

We're excited to announce the release of Taminator v2.0.1, a critical hotfix with 10 bug fixes.

## 📦 Downloads

### Linux
- [Taminator-2.0.1.AppImage](link) (136 MB)
  - `chmod +x Taminator-2.0.1.AppImage && ./Taminator-2.0.1.AppImage`

### macOS
- [Taminator-2.0.1.dmg](link) (120 MB) - Installer
- [Taminator-2.0.1-mac.zip](link) (115 MB) - Portable

**macOS Note**: Right-click and select "Open" on first launch.

## ✨ What's Fixed

- Fixed 10 critical bugs
- Enhanced error handling
- Memory leak prevention
- Improved stability

See [full release notes](RELEASE-NOTES-2.0.1.md) for details.

## 🔒 Verify Downloads

```bash
sha256sum -c SHA256SUMS
```
```

---

## 🛠️ Development Builds

For testing before release:

```bash
# Dev build (faster, no optimization)
cd gui
npm start

# Production build (optimized)
npm run build
```

---

## 📞 Support

- **Build Issues**: Check this document
- **Runtime Issues**: See DEBUGGING-WITH-ANSAI-TOOLS.md
- **Questions**: Use tam-dev tools

---

**Last Updated**: 2025-11-01  
**Next Release**: v2.1.0 (planned)


