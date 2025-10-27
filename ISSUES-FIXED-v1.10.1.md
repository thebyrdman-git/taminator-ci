# GitLab Issues Fixed in v1.10.1

**Release:** Taminator v1.10.1  
**Date:** October 27, 2025

---

## ✅ Issues Resolved

### Issue #25: Adding accounts through UI fails with spawn tam-rfe ENOENT
**Reported by:** Frank Hirtz (1 hour ago)  
**Status:** ✅ **FIXED**

**Problem:**
```
Error discovering RFEs/Bugs: Error invoking remote method 'onboard-discover': 
Error: Failed to execute tam-rfe: spawn tam-rfe ENOENT
```

**Root Cause:**
- GUI expected `tam-rfe` command in system PATH
- Python CLI source was bundled but dependencies weren't
- Users without Python dev environment → broken onboarding

**Fix:**
- Created standalone PyInstaller binary (19MB) with all dependencies
- GUI now uses bundled binary with smart detection
- Falls back to system PATH if needed
- Zero external dependencies required

**Files Changed:**
- `build-cli.spec` - PyInstaller configuration
- `build-cli-binary.sh` - Build automation
- `gui/main.js` - Smart CLI detection
- `gui/package.json` - Bundle binary
- `.github/workflows/build.yml` - Build binary first

---

### Issue #24: Using 'Migrate from Auth Box' button fails with hardcoded path
**Reported by:** Jacob Hunt (4 days ago)  
**Status:** ✅ **FIXED**

**Problem:**
```javascript
// Hardcoded path in gui/index.html:1729
const result = await execPromise('/home/jbyrd/pai/bin/tam-vault migrate 2>&1');
```

**Fix:**
- Now tries multiple common locations:
  - `~/pai/bin/tam-vault`
  - `~/hatter-pai/bin/tam-vault`
  - System PATH (`tam-vault`)
- Provides clear error if not found
- Portable across all user installations

**Files Changed:**
- `gui/index.html` - vaultMigrate() function

---

### Issue #21: GETTING-STARTED document is missing
**Reported by:** Alexey Masolov (6 days ago)  
**Status:** ✅ **FIXED**

**Problem:**
- GETTING-STARTED.md existed in `docs/archive/` but not at repository root
- Users expected it at root level for quick access

**Fix:**
- Copied GETTING-STARTED.md to repository root
- Now accessible at: `/GETTING-STARTED.md`
- Maintained copy in docs/archive for historical reference

**Files Changed:**
- `GETTING-STARTED.md` - Added at root

---

## ℹ️ Issues Analyzed (Not Fixed)

### Issue #23: Blank page on v1.9.2 AppImage
**Reported by:** Jacob Hunt (4 days ago)  
**Status:** 🟢 **LIKELY RESOLVED IN v1.10.0**

**Analysis:**
- Issue reported against v1.9.2 (old version)
- v1.10.0 included major GUI refactoring
- OOBE wizard and improved initialization
- Recommend testing v1.10.1 and closing if resolved

---

### Issue #22: tam-onboard-wizard requires rhcase
**Reported by:** Alexey Masolov (6 days ago)  
**Status:** 📝 **EXTERNAL DEPENDENCY**

**Analysis:**
- `rhcase` is Red Hat's case management CLI tool
- External dependency, not part of Taminator
- Required for TAM workflows that integrate with cases

**Documentation Update:**
- Added to README prerequisites section
- Installation: `sudo dnf install rhcase` or via Red Hat IT
- Not a Taminator bug - working as designed

---

### Issue #20: Convert to containerized tool
**Reported by:** Alexey Masolov (1 week ago)  
**Status:** 🔮 **FEATURE REQUEST** (Deferred to v2.0)

**Analysis:**
- Feature request, not a bug
- Current AppImage/DMG/EXE covers most use cases
- Containerization would be beneficial for:
  - CI/CD pipelines
  - Server deployments
  - Standardized environments

**Recommendation:**
- Defer to v2.0.0 or later
- Would require significant architecture changes
- Current desktop app model is working well

---

## 📊 Summary

### Fixed in v1.10.1
- ✅ Issue #25 - spawn tam-rfe ENOENT (Critical)
- ✅ Issue #24 - Hardcoded tam-vault path
- ✅ Issue #21 - GETTING-STARTED missing
- ✅ **BONUS:** Hardcoded email in JIRA auth

### Not Requiring Fix
- 🟢 Issue #23 - Old version (likely resolved)
- 📝 Issue #22 - External dependency (documented)
- 🔮 Issue #20 - Feature request (deferred)

### Success Rate
**100% of actionable bugs fixed** (3/3)

---

## 🧪 Testing Verification

### Issue #25 Verification
```bash
# Test on system without Python packages
./Taminator-1.10.1.AppImage
# Navigate to Onboard tab
# Click "Add Customer"
# Should work without errors
```

### Issue #24 Verification
```bash
# Test with different PAI installation locations
# Settings → Vault → Migrate from Auth Box
# Should work regardless of PAI location
```

### Issue #21 Verification
```bash
# Check for GETTING-STARTED.md at root
ls -la GETTING-STARTED.md
# Should exist and be readable
```

---

## 📝 Release Notes Entry

**v1.10.1 (October 27, 2025) - Bug Fix Release**

Fixes:
- Fixed onboarding failure with "spawn tam-rfe ENOENT" error (#25)
- Fixed hardcoded path in "Migrate from Auth Box" button (#24)
- Added GETTING-STARTED.md to repository root (#21)
- Fixed hardcoded email in JIRA authentication

Improvements:
- Bundled standalone CLI binary with all dependencies
- Smart path detection for PAI tools
- Better error messages for missing dependencies

---

## 🙏 Acknowledgments

**Bug Reporters:**
- Frank Hirtz - Issue #25 (spawn tam-rfe ENOENT)
- Jacob Hunt - Issue #24 (hardcoded path), Issue #23 (blank page)
- Alexey Masolov - Issues #22, #21, #20

Thank you for helping make Taminator better!

---

**Last Updated:** October 27, 2025  
**Release:** v1.10.1  
**Status:** All actionable issues resolved

