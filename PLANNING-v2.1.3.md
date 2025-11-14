# TAMINATOR v2.1.3 - Planning Document

**Target Release:** November 2025 (Quick Follow-up)  
**Type:** Backend Bundling Fix  
**Status:** Planning

---

## 🎯 Primary Goal

**Bundle Python backend service in AppImage** to enable full functionality.

---

## 🐛 Issue to Fix

**Problem:** v2.1.2 AppImage doesn't include the Python backend service

**Impact:**
- GUI works but backend API fails
- JIRA integration unavailable
- Intelligence engine unavailable
- Report operations unavailable

**Root Cause:**
- `taminator-service` binary not included in electron-builder `extraResources`
- Workflow doesn't build Python backend binary

---

## 🔧 Solution: Build & Bundle Backend

### Step 1: Build Python Backend Binary

Add to `.github/workflows/release.yml` before Linux build:

```yaml
build-python-backend:
  name: Build Python Backend Binary
  runs-on: ubuntu-latest
  needs: pre-build-checks
  
  steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        
    - name: Install PyInstaller
      run: pip install pyinstaller
      
    - name: Build backend binary
      run: |
        cd src
        pyinstaller --onefile --name taminator-service \
          --hidden-import=taminator \
          ../bin/tam-rfe
        
    - name: Verify binary
      run: |
        dist/taminator-service --version
        ls -lh dist/taminator-service
        
    - name: Upload backend binary
      uses: actions/upload-artifact@v4
      with:
        name: backend-binary
        path: dist/taminator-service
        retention-days: 1
```

### Step 2: Download Backend in Build Jobs

Add to `build-linux` and `build-macos` jobs:

```yaml
- name: Download backend binary
  uses: actions/download-artifact@v4
  with:
    name: backend-binary
    path: backend/
    
- name: Make backend executable
  run: chmod +x backend/taminator-service
```

### Step 3: Update package.json extraResources

Verify `gui/package.json` includes:

```json
{
  "build": {
    "extraResources": [
      {
        "from": "../backend/taminator-service",
        "to": "bin/taminator-service"
      },
      {
        "from": "../src/taminator",
        "to": "taminator"
      }
    ]
  }
}
```

### Step 4: Update service-manager.js Path

Verify `gui/service-manager.js` looks for backend in:
- Development: `../bin/tam-rfe`
- Production: `resources/bin/taminator-service`

---

## ✅ Testing Plan

### Test Checklist

**Before Release:**
- [ ] Build AppImage locally
- [ ] Extract and verify backend binary exists
- [ ] Launch AppImage
- [ ] Verify backend service starts
- [ ] Test JIRA connection
- [ ] Test report operations
- [ ] Test intelligence features

**CI/CD:**
- [ ] Workflow builds backend binary
- [ ] Backend included in AppImage
- [ ] All tests pass
- [ ] Release created successfully

---

## 📋 Changes Required

### Files to Modify

1. **`.github/workflows/release.yml`**
   - Add `build-python-backend` job
   - Update `build-linux` to download backend
   - Update `build-macos` to download backend

2. **`gui/package.json`** (verify/update)
   - Ensure `extraResources` includes backend

3. **`gui/service-manager.js`** (verify)
   - Check backend path resolution

4. **`CHANGELOG.md`**
   - Add v2.1.3 entry

5. **`README.md`**
   - Update version to 2.1.3
   - Remove "Preview" note

---

## 📊 Estimated Effort

**Development:** 2-4 hours
- Add backend build job: 1 hour
- Test locally: 1 hour
- Fix any issues: 1-2 hours

**Testing:** 1-2 hours
- Full functional testing
- Multi-platform verification

**Documentation:** 30 minutes
- Update README
- Update CHANGELOG
- Release notes

**Total:** 4-7 hours

---

## 🚀 Release Process

### Step 1: Implement Changes
```bash
# Update workflow
vim .github/workflows/release.yml

# Verify package.json
vim gui/package.json

# Test locally
cd gui
npm run build:linux
```

### Step 2: Test Local Build
```bash
# Extract AppImage
./gui/dist/Taminator-2.1.3.AppImage --appimage-extract

# Check backend exists
ls -lh squashfs-root/resources/bin/taminator-service

# Test backend
squashfs-root/resources/bin/taminator-service --version
```

### Step 3: Commit & Push
```bash
git add -A
git commit -m "feat: Bundle Python backend in AppImage

- Add build-python-backend job to workflow
- Include backend binary in electron-builder
- Enables full functionality in AppImage

Fixes: Backend service not found in v2.1.2"

git push origin main
```

### Step 4: Tag & Release
```bash
git tag -a v2.1.3 -m "Release v2.1.3 - Backend Bundling"
git push origin v2.1.3
git push ci v2.1.3
```

### Step 5: Verify Release
- Check GitHub Actions succeeds
- Download AppImage from release
- Test all functionality
- Update documentation

---

## 📚 Documentation Updates

### CHANGELOG.md
```markdown
## [2.1.3] - 2025-11-XX

### 🔧 Backend Bundling Release

### Fixed
- **Backend service now bundled in AppImage**
  - Python backend binary included
  - Full functionality available
  - No separate installation required

### Changed
- Updated build workflow to include PyInstaller
- Backend binary packaged with Electron app
- Service manager paths updated

### Verified
- ✅ JIRA integration works
- ✅ Intelligence engine works
- ✅ Report operations work
- ✅ All features functional
```

### README.md
```markdown
**Version**: 2.1.3 (Full Functionality)
```

---

## 🎯 Success Criteria

**v2.1.3 is complete when:**
- [ ] Backend binary builds in CI/CD
- [ ] Backend included in AppImage
- [ ] AppImage launches with working backend
- [ ] All JIRA operations work
- [ ] Intelligence engine works
- [ ] Report operations work
- [ ] macOS DMG includes backend
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Release created and available

---

## 💡 Alternative Approaches

### Option A: PyInstaller (Recommended)
**Pros:**
- Single binary, easy to bundle
- No Python runtime needed
- Fast startup

**Cons:**
- Larger file size
- Build complexity

### Option B: Bundle Python Source
**Pros:**
- Smaller size
- Easier to debug

**Cons:**
- Requires Python runtime
- More complex path management

### Option C: Separate Backend Package
**Pros:**
- Clean separation
- Independent updates

**Cons:**
- Two-step installation
- User confusion

**Decision:** Use Option A (PyInstaller) - cleanest for end users

---

## 🔗 Related

- Known Issues: `/KNOWN-ISSUES-v2.1.2.md`
- Build Strategy: `/BUILD-STRATEGY.md`
- Workflow: `.github/workflows/release.yml`

---

**Created:** November 14, 2025  
**Target Release:** November 2025  
**Priority:** High (fixes v2.1.2 limitation)  
**Estimated Time:** 4-7 hours

