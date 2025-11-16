# TAMINATOR v2.1.3 - Release Notes

**Release Date:** November 16, 2025  
**Type:** Backend Bundling Release  
**Codename:** "Full Functionality"

---

## 🎉 Backend Service Now Included!

**v2.1.3 completes the v2.1.2 foundation with full backend functionality.**

---

## 🚀 What's New in v2.1.3

### Backend Service Bundled ✅

**The #1 issue from v2.1.2 is now FIXED:**
- ✅ Python backend service (19MB) included in AppImage
- ✅ Backend starts automatically with GUI
- ✅ Full JIRA integration functional
- ✅ Intelligence engine operational
- ✅ All API endpoints available
- ✅ No separate installation required

**Before v2.1.3:**
- ⚠️ GUI worked, but backend API unavailable
- ⚠️ JIRA operations failed
- ⚠️ Intelligence features non-functional

**After v2.1.3:**
- ✅ Everything works out of the box!
- ✅ Complete TAMINATOR experience
- ✅ Production-ready

---

## 📦 Available Platforms

**v2.1.3 supports:**
- ✅ Linux (x86_64 AppImage) - **Full functionality**
- ✅ macOS (Universal DMG - Intel & Apple Silicon) - **Full functionality**
- ⏳ Windows (coming in v2.2.0)

---

## 📊 What's Included

### From v2.1.2 (CI/CD Foundation)
- ✅ Complete 5-stage automated pipeline
- ✅ Multi-platform builds (Linux, macOS)
- ✅ Zero ESLint warnings (perfect code quality)
- ✅ Jest testing infrastructure
- ✅ Documentation at taminator.dev
- ✅ One-command releases

### New in v2.1.3 (Backend Functionality)
- ✅ **Backend service bundled in AppImage**
- ✅ **JIRA integration works**
- ✅ **Intelligence engine operational**
- ✅ **Report operations functional**
- ✅ **All features production-ready**

---

## 🔧 Technical Details

### What Was Fixed

**Problem:**
- v2.1.2 AppImage didn't include the Python backend service
- Service manager looked for `bin/taminator-service`
- Package config tried to copy from non-existent `dist/taminator-service`

**Solution:**
```json
{
  "extraResources": [
    {
      "from": "../bin/tam-rfe",
      "to": "bin/taminator-service"
    }
  ]
}
```

**Result:**
- 19MB PyInstaller binary now included
- Backend launches automatically
- Full functionality restored

---

## 📦 Installation

### Linux (AppImage)
```bash
# Download from GitLab CEE (VPN required)
chmod +x Taminator-2.1.3.AppImage
./Taminator-2.1.3.AppImage
```

### macOS (DMG)
```bash
# Download from GitLab CEE (VPN required)
open Taminator-2.1.3.dmg
# Drag to Applications
# First run: Right-click → Open
```

### Verify Checksums
```bash
sha256sum -c SHA256SUMS
```

---

## ✅ Features Now Working

### JIRA Integration
- ✅ Connect to Red Hat JIRA
- ✅ Query RFEs and Bugs
- ✅ Update case reports
- ✅ Track status changes

### Intelligence Engine
- ✅ Email analysis
- ✅ Case classification
- ✅ Urgency detection
- ✅ Pattern recognition

### Report Operations
- ✅ Generate customer reports
- ✅ Status tracking
- ✅ Automated updates
- ✅ Historical data

### API Server
- ✅ RESTful API at localhost:8765
- ✅ FastAPI documentation at /docs
- ✅ Health checks
- ✅ Automatic startup/shutdown

---

## 🎯 Upgrade from v2.1.2

**Why upgrade?**
- v2.1.2: GUI only (preview)
- v2.1.3: **Full functionality** ✅

**How to upgrade:**
1. Download v2.1.3 from GitLab CEE
2. Replace v2.1.2 AppImage/DMG
3. Launch - backend starts automatically!

**No configuration changes needed.**

---

## 📊 Comparison: v2.1.2 vs v2.1.3

| Feature | v2.1.2 | v2.1.3 |
|---------|--------|--------|
| GUI | ✅ Works | ✅ Works |
| Backend Service | ❌ Missing | ✅ **Bundled** |
| JIRA Integration | ❌ Failed | ✅ **Works** |
| Intelligence Engine | ❌ Unavailable | ✅ **Works** |
| Report Operations | ❌ Failed | ✅ **Works** |
| Production Ready | ⚠️ Preview | ✅ **YES** |

---

## 🚀 Build Information

**Size:**
- AppImage: 136 MB (up from 135 MB in v2.1.2)
- DMG: ~131 MB (up from 130 MB)
- Backend: 19 MB (now included!)

**Build Time:**
- ~5 minutes for Linux
- ~8 minutes for macOS
- Total CI/CD: ~20 minutes

**Quality:**
- ✅ 0 ESLint warnings
- ✅ 0 ESLint errors
- ✅ All tests pass
- ✅ Local testing verified

---

## 🐛 Known Issues

**None!** 🎉

All major features are functional. Minor enhancements planned for v2.2.0.

---

## 🛣️ What's Next

### v2.2.0 (December 2025)
- Windows builds (NSIS installer)
- Enhanced intelligence features
- Performance optimizations
- Additional integrations
- 50%+ test coverage

---

## 📚 Documentation

- **Website:** [taminator.dev](https://taminator.dev)
- **Installation:** [taminator.dev/get-started/installation](https://taminator.dev/get-started/installation/)
- **GitLab Repository:** https://gitlab.cee.redhat.com/jbyrd/taminator
- **Changelog:** `CHANGELOG.md`

---

## 🔗 Download

**GitLab CEE Release:**
```
https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v2.1.3
```

**Requirements:**
- Red Hat employee
- Red Hat VPN connection
- GitLab CEE access

---

## 🙏 Credits

**Built by:** Jimmy Byrd (jbyrd@redhat.com)  
**For:** Red Hat TAM Team  
**Philosophy:** Container-First + Everything-as-Code + Automation-First

---

## 📝 Release Summary

**v2.1.3 is the completion of v2.1.2:**
- v2.1.2 built the CI/CD foundation (95% complete)
- v2.1.3 adds the missing backend (100% complete)

**Together they represent:**
- ✅ Perfect code quality (0 warnings)
- ✅ Full automation (CI/CD)
- ✅ Complete functionality (backend)
- ✅ Production-ready release

---

**Status:** ✅ Production Ready  
**Platforms:** Linux & macOS  
**Functionality:** Complete

🚀 **The Skynet TAMs Actually Want™** - Now with full backend support!

