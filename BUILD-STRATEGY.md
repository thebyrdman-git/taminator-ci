# TAMINATOR Build Strategy

**Philosophy:** Container-First Architecture + Everything-as-Code

---

## 🏗️ Build System Overview

TAMINATOR uses a **hybrid build strategy** to support all platforms:

1. **Linux builds:** Local + GitLab CI/CD
2. **Windows builds:** GitLab CI/CD (electronuserland/builder:wine container)
3. **macOS builds:** Manual or GitHub Actions (requires macOS runner)

---

## 📦 Platform-Specific Builds

### Linux (✅ Automated)

**Build locally:**
```bash
cd gui
npm ci
npx electron-builder --linux appimage
```

**Outputs:**
- `Taminator-{version}.AppImage` (136MB) - Universal Linux binary
- `taminator-gui_{version}_amd64.deb` - Debian/Ubuntu package
- `taminator-gui-{version}.x86_64.rpm` - RHEL/Fedora package (requires rpmbuild)

**CI/CD:**
- Builds automatically on every tag
- Uses standard Linux runner
- No special configuration needed

### Windows (✅ CI/CD Only)

**Local build (not recommended):**
```bash
cd gui
npm ci
npx electron-builder --win nsis
```

**Requirements:**
- Wine with 32-bit support
- Windows code signing tools (rcedit)
- Complex Wine configuration

**Why CI/CD is better:**
- Uses `electronuserland/builder:wine` Docker image
- Pre-configured Wine environment
- All tools included
- Reproducible builds

**CI/CD:**
```yaml
build_windows:
  image: electronuserland/builder:wine
  script:
    - cd gui
    - npm ci
    - npm run build:win
```

**Output:**
- `Taminator-Setup-{version}.exe` - NSIS installer

### macOS (⚠️ Manual or GitHub Actions)

**Build locally (requires macOS):**
```bash
cd gui
npm ci
npx electron-builder --mac dmg
```

**Requirements:**
- macOS machine (or VM)
- Xcode Command Line Tools
- Code signing certificate (optional)

**Why manual:**
- GitLab CEE has no macOS runners
- macOS builds require Apple hardware
- Alternative: GitHub Actions with macOS runner

**GitHub Actions Alternative:**
```yaml
build_macos:
  runs-on: macos-latest
  steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-node@v3
    - run: cd gui && npm ci
    - run: cd gui && npm run build:mac
```

**Output:**
- `Taminator-{version}.dmg` - macOS disk image

---

## 🚀 CI/CD Pipeline

### Trigger Builds

**Manual builds:**
```bash
# Linux only
cd /home/jbyrd/TAMINATOR/gui
npx electron-builder --linux appimage
```

**Automated builds (all platforms):**
```bash
# Tag and push
git tag -a v2.1.2 -m "Release v2.1.2"
git push origin v2.1.2

# GitLab CI/CD will:
# 1. Run linters
# 2. Run tests
# 3. Build Linux (AppImage, deb, rpm)
# 4. Build Windows (NSIS)
# 5. Build macOS (if runner available)
# 6. Create GitLab release
# 7. Upload all artifacts
```

### Pipeline Stages

```
lint → test → build → deploy → release
  ↓      ↓      ↓       ↓        ↓
 JS+Py  Jest  3 Plats  Docs   GitLab
```

**Build matrix:**
| Platform | Method | Location | Time |
|----------|--------|----------|------|
| Linux    | Docker | GitLab CI| 5 min |
| Windows  | Wine   | GitLab CI| 8 min |
| macOS    | Manual | Local    | 10 min|

---

## 📥 Download Locations

### Internal (Red Hat CEE)

**Primary:** GitLab Releases
```
https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v2.1.2
```

**Assets:**
- AppImage (x86_64)
- Debian Package (.deb)
- RPM Package (.rpm)
- Windows Installer (.exe)
- macOS DMG (when available)

### Public

**Documentation only:**
```
https://taminator.dev
```

**No binaries on public site** - all downloads are internal to Red Hat CEE.

---

## 🔧 Build Configuration

### Electron Builder Config

Location: `gui/package.json` (build section)

**Key settings:**
```json
{
  "build": {
    "appId": "com.redhat.taminator",
    "productName": "TAMINATOR",
    "linux": {
      "target": ["AppImage", "deb", "rpm"],
      "category": "Development"
    },
    "win": {
      "target": [{"target": "nsis", "arch": ["x64"]}]
    },
    "mac": {
      "target": [{"target": "dmg", "arch": ["x64", "arm64"]}]
    }
  }
}
```

### Dependencies

**Build tools (dev dependencies):**
```json
{
  "electron": "^33.2.0",
  "electron-builder": "^25.1.8",
  "electron-builder-squirrel-windows": "^25.1.8"
}
```

**System requirements:**
- Node.js 18+
- npm 9+
- (Optional) rpmbuild for RPM packages
- (Optional) Wine for Windows builds

---

## 🎯 Best Practices

### 1. Version Management

**Single source of truth:**
```bash
# Update version
cd gui
npm version 2.1.2

# This updates:
# - gui/package.json
# - gui/package-lock.json
```

**Don't forget:**
- Update `README.md`
- Update `CHANGELOG.md`
- Create `RELEASE-NOTES-v{version}.md`

### 2. Testing Builds

**Before tagging:**
```bash
# Test Linux build locally
cd gui
npm run build:linux

# Verify output
ls -lh dist/
./dist/Taminator-*.AppImage --version
```

**After tagging:**
- Monitor GitLab CI/CD pipeline
- Download artifacts from job
- Test each platform binary

### 3. Release Process

**Full release workflow:**
```bash
# 1. Update version
cd gui && npm version 2.1.2

# 2. Update documentation
vim ../README.md
vim ../CHANGELOG.md
vim ../RELEASE-NOTES-v2.1.2.md

# 3. Commit changes
git add -A
git commit -m "chore: Release v2.1.2"

# 4. Tag release
git tag -a v2.1.2 -m "Release v2.1.2 - CI/CD & Packaging"

# 5. Push to GitLab
git push origin main
git push origin v2.1.2

# 6. Monitor CI/CD
# https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines

# 7. Verify release
# https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v2.1.2
```

---

## 🐛 Troubleshooting

### Linux Build Fails

**Issue:** RPM build fails
```
rpmbuild failed (exit code 1)
```

**Solution:** Install rpmbuild
```bash
sudo dnf install rpm-build
```

### Windows Build Fails

**Issue:** Wine errors
```
wine: failed to start
```

**Solution:** Use GitLab CI/CD instead
- Don't build Windows locally
- Let CI/CD handle it with proper Wine setup

### macOS Build Fails

**Issue:** No macOS runner
```
No runner found for macOS builds
```

**Solution:** Build manually or use GitHub Actions
```bash
# On a Mac:
cd gui
npm ci
npm run build:mac
```

---

## 📊 Build Artifacts

### Size Comparison

| Platform | Format | Size | Compressed |
|----------|--------|------|------------|
| Linux    | AppImage | 136MB | N/A |
| Linux    | .deb     | 99MB  | N/A |
| Linux    | .rpm     | ~100MB | N/A |
| Windows  | .exe     | ~150MB | N/A |
| macOS    | .dmg     | ~160MB | N/A |

### Retention

**GitLab CI/CD artifacts:**
- Expire after: 30 days
- Download from: Job artifacts page
- Archive old releases manually

**GitLab Releases:**
- Permanent (until deleted)
- Linked to tags
- Accessible via Releases page

---

## 🔗 Resources

**Documentation:**
- Electron Builder: https://www.electron.build/
- GitLab CI/CD: https://docs.gitlab.com/ee/ci/
- electronuserland/builder: https://hub.docker.com/r/electronuserland/builder

**Internal:**
- GitLab CI/CD config: `.gitlab-ci.yml`
- Build config: `gui/package.json` (build section)
- GitLab pipeline: https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines

---

**Last updated:** November 14, 2025  
**Version:** 2.1.2

