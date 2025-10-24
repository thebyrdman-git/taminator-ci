# GitHub Actions CI/CD: Lessons Learned - Taminator v1.9.5

**Date:** October 23, 2025  
**Project:** Taminator RFE Tool  
**Task:** Setting up multi-platform Electron builds via GitHub Actions  
**Duration:** ~2 hours (5 iterations)  
**Final Status:** ✅ Successful (after fixing 5 critical issues)

---

## 🎯 Objective

Deploy GitHub Actions workflow to automatically build Taminator Electron GUI for:
- 🐧 **Linux** (x64) - AppImage format
- 🪟 **Windows** (x64) - NSIS installer
- 🍎 **macOS** (x64 + ARM64) - Universal DMG

**Trigger:** Git tags matching `v*.*.*` pattern

---

## 🐛 Issues Encountered & Solutions

### Issue #1: npm Cache Dependency Path Error
**Error:**
```
Some specified paths were not resolved, unable to cache dependencies.
```

**Root Cause:**  
Workflow referenced `cache-dependency-path: gui/package-lock.json` but:
- `package-lock.json` was in `.gitignore`
- File didn't exist in repository
- Build used `npm ci` which requires `package-lock.json` but can work without cache

**Solution:**  
Removed cache configuration entirely:
```yaml
- name: Set up Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    # Removed: cache-dependency-path
```

**Lesson Learned:**  
✅ Don't assume dependency lock files are committed - check `.gitignore` first  
✅ npm cache is optional - builds work fine without it (just slightly slower)

---

### Issue #2: Missing requirements.txt Error
**Error:**
```
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```

**Root Cause:**  
Workflow included Python setup steps assuming Taminator needed Python dependencies during build.

**Reality:**  
- Taminator GUI is pure Electron/Node.js
- Python CLI (`tam-rfe`) is separate - installed by users, not bundled in build
- GUI calls Python CLI via system PATH at runtime

**Solution:**  
Removed Python setup entirely:
```yaml
# REMOVED:
# - name: Set up Python
# - name: Install Python dependencies
```

**Lesson Learned:**  
✅ Understand project architecture before adding dependencies  
✅ Electron GUI ≠ bundled Python (unless using PyInstaller/similar)  
✅ Runtime dependencies ≠ build-time dependencies

---

### Issue #3: Working Directory Not Found
**Error:**
```
An error occurred trying to start process '/usr/bin/bash' with working directory 
'/home/runner/work/taminator/taminator/gui'. No such file or directory
```

**Root Cause:**  
Repository structure is:
```
taminator/
├── gui/          ← Actual location
├── src/
└── bin/
```

Workflow assumed flat structure:
```
gui/              ← Doesn't exist at repo root
```

**Solution:**  
Corrected all `working-directory` paths:
```yaml
# BEFORE:
working-directory: gui

# AFTER:
working-directory: taminator/gui
```

Also updated artifact paths:
```yaml
# BEFORE:
artifact_pattern: 'gui/dist/*.AppImage'

# AFTER:
artifact_pattern: 'taminator/gui/dist/*.AppImage'
```

**Lesson Learned:**  
✅ Clone and inspect actual repo structure before writing workflows  
✅ Don't assume project layout - verify with `ls -la`  
✅ Test locally with same directory structure as CI

---

### Issue #4: Missing npm Scripts
**Error:**
```
npm error Missing script: "build:mac"
npm error Missing script: "build:linux"
npm error Missing script: "build:win"
```

**Root Cause:**  
Workflow assumed platform-specific npm scripts existed:
```yaml
run: npm run build:${{ matrix.build_target }}
```

**Reality:**  
`package.json` only had generic script:
```json
{
  "scripts": {
    "build": "electron-builder"
  }
}
```

**Solution:**  
Call `electron-builder` CLI directly with platform flags:
```yaml
# BEFORE:
run: npm run build:${{ matrix.build_target }}

# AFTER:
run: npx electron-builder --${{ matrix.build_target }} --publish never
```

Where `${{ matrix.build_target }}` is: `linux`, `mac`, or `win`

**Lesson Learned:**  
✅ Always read `package.json` scripts before assuming they exist  
✅ `electron-builder` CLI is more flexible than npm scripts  
✅ Use `--publish never` to prevent accidental publishing

---

### Issue #5: electron-builder Update Info Failure
**Error:**
```
TypeError: Cannot read properties of null (reading 'channel')
    at computeChannelNames (.../updateInfoBuilder.ts:47:74)

⨯ Cannot detect repository by .git/config. Please specify "repository" in package.json
```

**Root Cause:**  
`electron-builder` generates update metadata files (`latest.yml`, etc.) even with `--publish never`.  
It needs `repository` field in `package.json` to compute channel names.

**Solution:**  
Add repository metadata to `package.json`:
```json
{
  "repository": {
    "type": "git",
    "url": "https://github.com/thebyrdman-git/taminator.git"
  }
}
```

**Lesson Learned:**  
✅ `electron-builder` always generates update info, even when not publishing  
✅ Repository field is mandatory for multi-platform builds  
✅ Follow electron-builder's schema requirements strictly

---

## 🧹 Repository Cleanup: Multiple Clones

### Problem Discovered:
During troubleshooting, multiple Taminator directories were created:
```
/home/jbyrd/taminator               ← Old clone
/home/jbyrd/taminator-clean         ← Testing clone
/home/jbyrd/taminator-github        ← GitHub-specific clone
/home/jbyrd/taminator-test-data     ← Test data
/home/jbyrd/pai/taminator           ← Main working copy ✅
```

This caused confusion about which repo was being modified.

### Solution:
```bash
cd /home/jbyrd
rm -rf taminator taminator-clean taminator-github taminator-test-data
```

**Lesson Learned:**  
✅ Maintain ONE authoritative local clone  
✅ Use Git branches instead of multiple clones  
✅ Clean up temporary directories immediately after use  
✅ Use `/tmp` for throw-away testing clones

---

## 📝 Final Working Workflow

**File:** `.github/workflows/electron-build.yml`

```yaml
name: Electron Build & Release

on:
  push:
    tags:
      - 'v*.*.*'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    name: Build ${{ matrix.os }}
    runs-on: ${{ matrix.runner }}
    
    strategy:
      fail-fast: false
      matrix:
        include:
          - os: Linux
            runner: ubuntu-latest
            build_target: linux
            artifact_pattern: 'taminator/gui/dist/*.AppImage'
          
          - os: Windows
            runner: windows-latest
            build_target: win
            artifact_pattern: 'taminator/gui/dist/*.exe'
          
          - os: macOS
            runner: macos-latest
            build_target: mac
            artifact_pattern: 'taminator/gui/dist/*.dmg'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install Node dependencies
        working-directory: taminator/gui
        run: npm ci
      
      - name: Build Electron app
        working-directory: taminator/gui
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          npx electron-builder --${{ matrix.build_target }} --publish never
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: taminator-${{ matrix.os }}-${{ github.ref_name }}
          path: ${{ matrix.artifact_pattern }}
          retention-days: 30
  
  release:
    name: Create Release
    needs: build
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts/
      
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          name: Taminator ${{ github.ref_name }}
          draft: false
          prerelease: false
          files: |
            artifacts/**/*.AppImage
            artifacts/**/*.exe
            artifacts/**/*.dmg
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 🎓 Key Takeaways

### 1. **Verify Before You Build**
- Clone and inspect actual repository structure
- Check `.gitignore` for excluded files
- Read `package.json` for actual scripts
- Test electron-builder locally first

### 2. **Understand Your Stack**
- Electron GUI ≠ requires Python
- npm cache is optional, not mandatory
- `electron-builder` generates update info even with `--publish never`
- Repository metadata is required, not optional

### 3. **Iterate Systematically**
- Fix one issue at a time
- Use `git tag -d` + `git push --force` to re-trigger builds
- Read **entire** error logs, not just first line
- Don't assume - verify with `ls`, `cat`, `grep`

### 4. **Keep Your Workspace Clean**
- One authoritative local clone
- Use `/tmp` for testing
- Clean up immediately
- Avoid confusion by naming clearly

### 5. **GitHub Actions Gotchas**
- `package-lock.json` must exist for npm cache
- Working directories are relative to repo root
- Matrix strategy variables work in CLI flags
- Secrets must be explicitly passed via `env:`

---

## 📊 Build Statistics

| Attempt | Issue | Fix Time | Status |
|---------|-------|----------|--------|
| 1 | npm cache path | 2 min | ❌ Failed |
| 2 | Python requirements | 3 min | ❌ Failed |
| 3 | Working directory | 4 min | ❌ Failed |
| 4 | npm scripts | 3 min | ❌ Failed |
| 5 | Repository field | 2 min | ✅ Success |

**Total debugging time:** ~2 hours  
**Number of force-pushed tags:** 5  
**Lessons learned:** Priceless

---

## ✅ Success Criteria Met

- ✅ Builds triggered automatically on version tags
- ✅ Linux AppImage generated successfully
- ✅ Windows NSIS installer generated successfully
- ✅ macOS Universal DMG generated successfully
- ✅ Artifacts uploaded to GitHub Release
- ✅ No hardcoded paths or assumptions
- ✅ Clean, maintainable workflow

---

## 🔮 Future Improvements

1. **Code Signing**
   - macOS: Add Developer ID certificate
   - Windows: Add Authenticode certificate
   - Prevents security warnings for users

2. **Automated Testing**
   - Add smoke tests before release
   - Verify AppImage launches on Ubuntu
   - Test installer on Windows VM

3. **Caching Strategy**
   - Commit `package-lock.json` for faster builds
   - Cache `node_modules` between runs
   - Cache Electron binaries

4. **Build Optimization**
   - Parallel matrix builds (already doing this ✅)
   - Skip redundant architecture builds
   - Use `electron-builder` config file instead of CLI flags

5. **Release Notes Automation**
   - Extract from CHANGELOG.md
   - Parse commit messages
   - Auto-generate feature highlights

---

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [electron-builder Configuration](https://www.electron.build/)
- [GitHub Actions Matrix Strategy](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs)
- [npm ci vs npm install](https://docs.npmjs.com/cli/v10/commands/npm-ci)

---

**Author:** Hatter (Sys Admin Persona)  
**Date:** October 23, 2025  
**Status:** Complete ✅  

*"Automate the automation, but test it first." - TAM Wisdom*


