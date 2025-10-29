# Cross-Platform Build Strategy

**Question**: Does the glibc compatibility issue affect Windows and macOS builds?

**Answer**: No, but similar principles apply to all platforms.

---

## 🐧 Linux (Current Issue)

### Problem
- **Library**: glibc (GNU C Library)
- **Issue**: Built on Fedora 42 (glibc 2.40) won't run on Rocky 9 (glibc 2.34)
- **Error**: `GLIBC_ABI_DT_RELR not found`
- **Scope**: Only affects Linux builds

### Solution
- **Build on**: Rocky Linux 9 (oldest target)
- **Works on**: Rocky 9+, RHEL 9+, Fedora 38+, Ubuntu 22.04+

---

## 🪟 Windows (No glibc Issue)

### Different C Runtime
- **Library**: MSVCRT (Microsoft Visual C++ Runtime) or UCRT (Universal C Runtime)
- **Not affected by glibc**: Windows doesn't use glibc
- **Different issue**: Minimum Windows version support

### Windows Build Considerations

**If you build on Windows 11**:
- ✅ Works on Windows 11
- ✅ Works on Windows 10 (usually)
- ❓ May not work on Windows 7/8 (if using new APIs)

**Best practice**:
- **Build on**: Windows 10 (oldest supported version)
- **Works on**: Windows 10, 11
- **Don't support**: Windows 7/8 (EOL)

**Electron Windows builds**:
- electron-builder handles MSVCRT automatically
- Usually not an issue unless using native modules
- PyInstaller on Windows bundles MSVCRT correctly

### Potential Windows Issues

**Native Python modules** (if using):
- Built with specific MSVC version
- May require Visual C++ Redistributable
- electron-builder can bundle these

**Recommendation**: Build on Windows 10, test on Windows 10 and 11.

---

## 🍎 macOS (No glibc Issue)

### Different C Library
- **Library**: libSystem (macOS system library)
- **Not affected by glibc**: macOS doesn't use glibc
- **Different issue**: Minimum macOS version and architecture

### macOS Build Considerations

**If you build on macOS 14 (Sonoma)**:
- ✅ Works on macOS 14 (Sonoma)
- ✅ Works on macOS 13 (Ventura)
- ✅ Usually works on macOS 12 (Monterey)
- ❓ May not work on macOS 11 (Big Sur) or older

**Best practice**:
- **Build on**: macOS 11 (Big Sur) - oldest supported
- **Target**: macOS 11+
- **Don't support**: macOS 10.x (too old)

**Architecture considerations**:
- **Intel (x86_64)**: Traditional Mac architecture
- **Apple Silicon (arm64)**: M1, M2, M3 chips
- **Universal Binary**: Both architectures in one .app

**Electron macOS builds**:
- electron-builder can create universal binaries
- Specify `mac.target: ["dmg", "zip"]` and `mac.arch: ["x64", "arm64", "universal"]`

### Potential macOS Issues

**Code signing** (required for distribution):
- Need Apple Developer account
- Need to sign .app bundle
- Need to notarize for macOS 10.15+

**Gatekeeper**:
- Unsigned apps show security warning
- Right-click → Open bypasses (first time)

**Recommendation**: Build universal binary on macOS 11+, test on Intel and Apple Silicon.

---

## 📊 Platform-Specific Build Matrix

| Platform | Build On | Works On | C Runtime | Main Issue |
|----------|----------|----------|-----------|------------|
| **Linux** | Rocky 9 | Rocky 9+, RHEL 9+, Fedora 38+ | glibc 2.34 | glibc version (CURRENT) |
| **Windows** | Windows 10 | Windows 10, 11 | MSVCRT/UCRT | API compatibility |
| **macOS** | macOS 11 | macOS 11+ | libSystem | SDK version, arch |

---

## 🎯 Universal Build Principle

**Rule**: Always build on the **oldest platform** you want to support.

**Why?**
- Newer platforms can run older binaries (usually)
- Older platforms **cannot** run newer binaries (symbol/API not found)
- This applies to **all platforms**, not just Linux

**Examples**:
- Build on Rocky 9 → Works on Rocky 9, 10, 11, Fedora 38+
- Build on Windows 10 → Works on Windows 10, 11
- Build on macOS 11 → Works on macOS 11, 12, 13, 14

---

## 🔧 Taminator Build Strategy (Recommended)

### Current State (v2.0 Alpha)
- **Linux**: Build on Rocky 9 ✅ (fixing now)
- **Windows**: Not built yet (planned v2.1)
- **macOS**: Not built yet (planned v2.1)

### Recommended Build Environments

**Linux AppImage**:
```yaml
Platform: Rocky Linux 9
Tools: Node 16+, Python 3.9+, gcc
Target: RHEL 9+, Rocky 9+, Fedora 38+
Distribution: AppImage (single file)
```

**Windows NSIS Installer**:
```yaml
Platform: Windows 10 (x64)
Tools: Node 16+, Python 3.9+, Visual Studio Build Tools
Target: Windows 10, 11
Distribution: .exe installer
```

**macOS DMG**:
```yaml
Platform: macOS 11 (Big Sur)
Tools: Node 16+, Python 3.9+, Xcode Command Line Tools
Target: macOS 11+ (Intel + Apple Silicon)
Distribution: Universal .dmg
```

---

## 🚀 Multi-Platform CI/CD (Future)

**GitLab CI with multiple runners**:

```yaml
# .gitlab-ci.yml

# Linux build (Rocky 9 runner)
build-linux:
  tags:
    - rocky9
  script:
    - npm install
    - cd gui && npm run build
  artifacts:
    paths:
      - gui/dist/*.AppImage

# Windows build (Windows 10 runner)
build-windows:
  tags:
    - windows10
  script:
    - npm install
    - cd gui && npm run build
  artifacts:
    paths:
      - gui/dist/*.exe

# macOS build (macOS 11 runner)
build-macos:
  tags:
    - macos11
  script:
    - npm install
    - cd gui && npm run build
  artifacts:
    paths:
      - gui/dist/*.dmg
```

---

## 🐛 Platform-Specific Issues to Watch

### Linux
- ✅ **glibc version** (current issue)
- ✅ **FUSE** (for AppImage mounting)
- ⚠️ **Wayland vs X11** (Electron compatibility)
- ⚠️ **GTK themes** (UI appearance)

### Windows
- ⚠️ **MSVCRT dependencies** (usually auto-handled)
- ⚠️ **Windows Defender** (false positives for PyInstaller)
- ⚠️ **UAC** (admin privileges if needed)
- ⚠️ **Path length limits** (260 char max)

### macOS
- ⚠️ **Code signing** (required for distribution)
- ⚠️ **Notarization** (required for macOS 10.15+)
- ⚠️ **Gatekeeper** (security warnings)
- ⚠️ **ARM vs Intel** (architecture compatibility)

---

## 📋 Pre-Release Testing Checklist

### Linux
- [ ] Test on Rocky 9
- [ ] Test on RHEL 9
- [ ] Test on Fedora 40
- [ ] Test on Ubuntu 22.04 (if supporting)
- [ ] Check glibc requirements: `ldd binary | grep GLIBC`

### Windows
- [ ] Test on Windows 10
- [ ] Test on Windows 11
- [ ] Test without admin rights
- [ ] Check for false positives (Windows Defender)

### macOS
- [ ] Test on Intel Mac
- [ ] Test on Apple Silicon Mac
- [ ] Test on macOS 11, 12, 13, 14
- [ ] Verify code signature: `codesign -v /path/to/app`

---

## 🎯 Current Focus (Alpha Release)

**Priority 1: Linux Build** (Now)
- ✅ Fix glibc issue (build on Rocky 9)
- ✅ Test on Rocky 9 VM
- ✅ Distribute to TAMs (mostly Linux users)

**Priority 2: Windows Build** (v2.1)
- Build on Windows 10
- Create NSIS installer
- Test on Windows 10/11

**Priority 3: macOS Build** (v2.1)
- Build on macOS 11+
- Create universal DMG
- Code sign and notarize

---

## ✅ Summary

**Does glibc issue affect Windows/macOS?**

**No**:
- ❌ Windows uses MSVCRT, not glibc
- ❌ macOS uses libSystem, not glibc
- ✅ This is a **Linux-only** issue

**But similar principles apply**:
- ✅ Build on oldest supported platform
- ✅ Test on target platforms
- ✅ Check for compatibility issues

**Current action**:
- Fix Linux build (Rocky 9)
- Windows/macOS builds later (v2.1)

---

## 🔗 Related Documents

- `ROCKY-BUILD-GUIDE.md` - How to build on Rocky Linux 9
- `APPIMAGE-COMPATIBILITY-ISSUE.md` - Detailed glibc issue analysis
- `README.md` - Platform requirements

---

**TL;DR**: Windows and macOS are fine. This is a Linux glibc issue. Fix by building on Rocky 9.

