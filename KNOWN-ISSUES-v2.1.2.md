# TAMINATOR v2.1.2 - Known Issues

**Release Date:** November 14, 2025  
**Status:** Binaries built, minor backend issue

---

## ⚠️ Backend Service Not Bundled

**Issue:** AppImage launches GUI but backend service fails to start

**Error Message:**
```
[ServiceManager] ❌ Failed to start service: Error: spawn taminator-service ENOENT
```

**Root Cause:**
- The Python backend service (`taminator-service`) is not bundled in the AppImage
- Electron GUI works fine
- Backend functionality unavailable

**Impact:**
- ⚠️ GUI launches successfully
- ⚠️ OOBE wizard may work (GUI-only features)
- ❌ API calls to backend will fail
- ❌ JIRA integration unavailable
- ❌ Intelligence engine unavailable
- ❌ Report operations unavailable

**Workaround:**
Install backend separately:
```bash
# Install from source
cd ~/TAMINATOR
pip install -e .

# Or use the CLI directly
./bin/tam-rfe --help
```

**Fix for v2.1.3:**
Update `.github/workflows/release.yml` to:
1. Build Python backend binary with PyInstaller
2. Include in `extraResources` for electron-builder
3. Ensure backend is bundled in AppImage

---

## ✅ What Works

**GUI Features:**
- ✅ Application launches
- ✅ Electron GUI renders
- ✅ OOBE wizard (GUI parts)
- ✅ Settings interface
- ✅ Theme switching

**Known Good:**
- ✅ Code quality (0 ESLint warnings)
- ✅ CI/CD pipeline (automated builds)
- ✅ Multi-platform packaging
- ✅ Documentation (taminator.dev)

---

## 🎯 Severity Assessment

**Severity:** Medium (not blocking for demo/UI testing)

**Can Use For:**
- ✅ Demo of GUI/UX improvements
- ✅ Testing Electron app structure
- ✅ Showing CI/CD automation
- ✅ Documentation reference

**Cannot Use For:**
- ❌ Production TAM work
- ❌ JIRA integration testing
- ❌ Intelligence engine testing
- ❌ Full functional testing

---

## 🔧 Quick Fix Plan (v2.1.3)

### Option 1: Bundle Python Binary
```yaml
# In .github/workflows/release.yml, before electron build:
- name: Build Python Backend
  run: |
    pip install pyinstaller
    pyinstaller --onefile bin/tam-rfe -n taminator-service
    cp dist/taminator-service ../dist/
```

### Option 2: Use Python Source
Update `electron-builder` config to include Python source:
```json
{
  "extraResources": [
    {
      "from": "../src/taminator",
      "to": "taminator"
    }
  ]
}
```

And modify `service-manager.js` to run via Python interpreter.

### Option 3: Separate Backend
Document that backend must be installed separately:
- AppImage = GUI only
- Backend via pip install or system package

---

## 📋 Action Items

**For v2.1.3:**
1. [ ] Decide on backend bundling strategy
2. [ ] Update build workflow
3. [ ] Test AppImage with bundled backend
4. [ ] Verify all features work

**For Current v2.1.2:**
1. [x] Document the issue
2. [x] Provide workarounds
3. [ ] Update release notes
4. [ ] Communicate to users

---

## 💡 Recommendation

**For v2.1.2:**
- Document as "GUI Preview Release"
- Emphasize CI/CD automation achievements
- Note backend bundling coming in v2.1.3

**For Production Use:**
- Wait for v2.1.3 with bundled backend
- Or install backend separately via pip

---

## 🔗 Related

- Build Strategy: `/BUILD-STRATEGY.md`
- Release Notes: `/RELEASE-NOTES-v2.1.2.md`
- CI/CD Pipeline: `.github/workflows/release.yml`

---

**Status:** Documented  
**Priority:** Medium  
**Target Fix:** v2.1.3  
**Workaround Available:** Yes (install backend separately)

