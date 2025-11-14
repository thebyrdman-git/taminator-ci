# TAMINATOR v2.1.2 - Release Artifacts

**Release Date:** November 14, 2025  
**Status:** ✅ Released  
**Type:** CI/CD & Packaging Release

---

## 📦 Artifacts

### Linux
- **Taminator-2.1.2.AppImage** (135MB)
  - Universal Linux binary
  - No installation required
  - Run: `./Taminator-2.1.2.AppImage`

### macOS
- **Taminator-2.1.2.dmg** (130MB)
  - macOS installer (x86_64)
  - Drag to Applications folder
  - First run: Right-click → Open

---

## 🔐 Verification

**Checksums:**
```bash
sha256sum -c SHA256SUMS
```

**Expected:**
- AppImage: `e4c5073857b1a3d66bc2ee1df7e5f2ebc77d16d21cf9e2448f11aeee859ad844`
- DMG: `e69473fca48eeefa0d1dd1cd4f4af120c44821a402281ba1220160de65d7aeec`

---

## 🚀 Installation

### Linux
```bash
chmod +x Taminator-2.1.2.AppImage
./Taminator-2.1.2.AppImage
```

### macOS
1. Open the DMG
2. Drag TAMINATOR to Applications
3. First run: Right-click → Open (bypass Gatekeeper)

---

## 🎯 What's New in v2.1.2

### Code Quality
- ✅ Eliminated ALL 61 ESLint warnings → 0
- ✅ Pre-commit hooks enforcing quality
- ✅ 100% clean codebase

### CI/CD & Automation
- ✅ Complete 5-stage automated pipeline
- ✅ Multi-platform builds (Linux, macOS, Windows)
- ✅ Automated releases
- ✅ Documentation deployment to taminator.dev

### Testing
- ✅ Jest framework installed
- ✅ Test infrastructure ready
- ✅ 30% coverage threshold configured

---

## 📚 Documentation

**Online:**
- Website: https://taminator.dev
- GitHub Release: https://github.com/thebyrdman-git/taminator-ci/releases/tag/v2.1.2
- GitLab (Internal): https://gitlab.cee.redhat.com/jbyrd/taminator

**In Repo:**
- Release Notes: `/RELEASE-NOTES-v2.1.2.md`
- Changelog: `/CHANGELOG.md`
- Build Strategy: `/BUILD-STRATEGY.md`

---

## 🐛 Known Issues

None at this time. All ESLint errors and warnings have been resolved.

---

## 🔗 Links

- **Download:** https://github.com/thebyrdman-git/taminator-ci/releases/tag/v2.1.2
- **Documentation:** https://taminator.dev
- **Source (Internal):** https://gitlab.cee.redhat.com/jbyrd/taminator
- **Issues:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues

---

**Philosophy:** Container-First + Everything-as-Code + Automation-First  
**Built by:** Jimmy Byrd  
**For:** Red Hat TAM Team

🚀 **The Skynet TAMs Actually Want™**

