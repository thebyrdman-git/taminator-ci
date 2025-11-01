# macOS Build Notes for Taminator v2.0.1

**Issue**: macOS builds (DMG/ZIP) cannot be fully created on Linux  
**Solution**: Use one of the methods below

---

## 🍎 Option 1: Build on macOS (Recommended)

### On a Mac Computer

```bash
# Clone the repository
git clone <repo-url>
cd TAMINATOR

# Checkout the release tag
git checkout v2.0.1

# Install dependencies
cd gui
npm install

# Build for macOS
npm run build:mac

# Or specifically:
npx electron-builder --mac dmg zip

# Output will be in gui/dist/
```

**Result**: 
- `Taminator-2.0.1.dmg` - Installer (x64 + arm64 universal)
- `Taminator-2.0.1-mac.zip` - Portable version

---

## 🔧 Option 2: Use GitHub Actions / GitLab CI

### Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-mac:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        working-directory: gui
        run: npm install
      
      - name: Build macOS
        working-directory: gui
        run: npm run build:mac
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: macos-builds
          path: |
            gui/dist/*.dmg
            gui/dist/*-mac.zip
```

---

## 🐳 Option 3: Use Docker (Limited Support)

```bash
# Note: This may not work perfectly due to macOS-specific requirements
docker run --rm -ti \
  -v $(pwd):/project \
  electronuserland/builder:wine \
  bash -c "cd /project/gui && npm install && npm run build:mac"
```

**Limitations**: 
- Code signing won't work
- Some macOS-specific features may fail
- App won't be notarized

---

## 📦 Current Status

### ✅ Available Now
- **Linux AppImage**: `Taminator-2.0.1.AppImage` (136 MB)
  - Built successfully
  - Tested and working
  - Ready for distribution

### ⏳ macOS Builds Needed
- **macOS DMG**: Build on macOS or CI/CD
- **macOS ZIP**: Build on macOS or CI/CD

---

## 🚀 Recommended Workflow

### Immediate Release (Linux Only)

```bash
# Release Linux version now
git add releases/v2.0.1/Taminator-2.0.1.AppImage \
        releases/v2.0.1/RELEASE-NOTES-2.0.1.md

git commit -m "Release v2.0.1 - Linux builds"
git tag -a v2.0.1-linux -m "Linux-only release"
git push origin main v2.0.1-linux
```

### Add macOS Builds Later

```bash
# After building on Mac:
cp gui/dist/*.dmg releases/v2.0.1/
cp gui/dist/*-mac.zip releases/v2.0.1/

# Update checksums
cd releases/v2.0.1
sha256sum *.{AppImage,dmg,zip} > SHA256SUMS

# Commit macOS builds
git add releases/v2.0.1/*.dmg \
        releases/v2.0.1/*-mac.zip \
        releases/v2.0.1/SHA256SUMS

git commit -m "Add macOS builds to v2.0.1"
git tag -a v2.0.1 -m "Complete release with macOS"
git push origin main v2.0.1
```

---

## 🔐 Code Signing (macOS)

If you have an Apple Developer account:

```bash
# Set environment variables
export APPLEID="your@email.com"
export APPLEIDPASS="app-specific-password"
export TEAM_ID="your-team-id"

# Add to package.json build config:
{
  "mac": {
    "identity": "Developer ID Application: Your Name (TEAM_ID)",
    "hardenedRuntime": true,
    "gatekeeperAssess": false,
    "entitlements": "entitlements.mac.plist"
  }
}

# Build with signing
npx electron-builder --mac dmg zip
```

### Create `entitlements.mac.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>com.apple.security.cs.allow-jit</key>
  <true/>
  <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
  <true/>
  <key>com.apple.security.cs.allow-dyld-environment-variables</key>
  <true/>
</dict>
</plist>
```

---

## ⚠️ For TAMs (Users)

### Unsigned macOS App

If the macOS build is not signed:

1. Download the DMG or ZIP
2. **Do not** double-click to open
3. Instead: **Right-click → Open**
4. Click "Open" in the security dialog
5. App will run and remember permission

### Signed macOS App

If properly signed and notarized:
- Double-click to install
- No security warnings
- Seamless experience

---

## 📊 Build Comparison

| Platform | Status | Size | Notes |
|----------|--------|------|-------|
| Linux AppImage | ✅ Built | 136 MB | Ready for distribution |
| macOS DMG | ⏳ Pending | ~120 MB | Build on macOS |
| macOS ZIP | ⏳ Pending | ~115 MB | Build on macOS |

---

## 💡 Quick Solution for Now

### Release Linux-only v2.0.1

Since all bugs were fixed in the JavaScript/Python code (platform-independent), the Linux build contains all the fixes. macOS users can:

1. **Wait** for macOS builds (when built on Mac)
2. **Build from source** on their Mac
3. **Use previous version** if on macOS (if  critical bugs don't affect them)

### Update Release Notes

Add this notice:

```markdown
## Platform Availability

- ✅ **Linux**: Available now (AppImage)
- ⏳ **macOS**: Coming soon (building on macOS required)

All bug fixes are in the code - macOS users can build from source.
```

---

## 🔧 Building from Source (For macOS Users)

```bash
# Prerequisites
- Node.js 18+
- Git
- Xcode Command Line Tools

# Steps
git clone <repo>
cd TAMINATOR
git checkout v2.0.1

# Backend
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Frontend
cd gui
npm install
npm start

# Or build:
npm run build:mac
```

---

## 📞 Next Steps

1. **Option A**: Release Linux-only now, add macOS later
2. **Option B**: Wait to build on macOS, release all at once
3. **Option C**: Set up CI/CD for automated multi-platform builds

**Recommended**: **Option A** - Linux users get fixes now, macOS follows

---

**Status**: Linux build ready ✅  
**macOS**: Requires Mac hardware or CI/CD  
**All fixes**: Platform-independent (work on both)  


