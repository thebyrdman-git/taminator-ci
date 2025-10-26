# GitLab CI/CD Lessons Learned

**Project:** Taminator  
**CI Platform:** GitLab.cee.redhat.com  
**First Pipeline Run:** October 24, 2025

This document tracks all issues encountered and fixed during GitLab CI setup for Taminator.

---

## Issue 1: Custom CI Configuration Path Required

**Date:** October 24, 2025  
**Symptom:** Pipeline not triggering on push or tag despite `.gitlab-ci.yml` existing

**Root Cause:**
- GitLab expects `.gitlab-ci.yml` at repository root
- Taminator has it at `taminator/.gitlab-ci.yml` (non-standard location)
- GitLab was not detecting the CI config file

**Fix:**
1. Navigate to GitLab: Settings → CI/CD → General pipelines
2. Find "CI/CD configuration file" setting
3. Set custom path: `taminator/.gitlab-ci.yml`
4. Save changes

**Impact:** ✅ Pipeline now detects configuration file

---

## Issue 2: Variable Expansion in `expire_in` Not Working

**Date:** October 24, 2025  
**Symptom:** `Pipeline cannot be run. jobs:build:linux:x64:artifacts expire in should be a duration`

**Root Cause:**
- Used variable syntax: `expire_in: ${ARTIFACTS_EXPIRE}`
- Variable was defined: `ARTIFACTS_EXPIRE: "7 days"`
- GitLab CI was not expanding the variable correctly in `artifacts.expire_in` context

**Original Code:**
```yaml
variables:
  ARTIFACTS_EXPIRE: "7 days"

build:linux:x64:
  artifacts:
    expire_in: ${ARTIFACTS_EXPIRE}  # ❌ Failed
```

**Fix:**
Replace variable expansion with direct value:
```yaml
build:linux:x64:
  artifacts:
    expire_in: 7 days  # ✅ Works
```

**Applied to:**
- `build:linux:x64`
- `build:linux:arm64`
- `build:windows`
- `build:macos`

**Commit:** `49847fc52` - "fix(ci): Use direct duration value instead of variable for expire_in"

**Impact:** ✅ Pipeline validation now passes

**Lesson:** GitLab CI variable expansion may not work in all YAML contexts. For `artifacts.expire_in`, use direct duration values.

---

## GitLab CI Best Practices (From Experience)

1. **Custom CI Path Configuration**
   - If your `.gitlab-ci.yml` is not at repo root, configure custom path in Settings
   - GitLab does NOT auto-detect non-standard locations

2. **Artifact Expiration**
   - Use direct duration values: `7 days`, `1 week`, `30 days`
   - Avoid variable expansion in `expire_in` field

3. **Runner Tags**
   - Use specific runner tags: `docker`, `windows`, `macos`
   - Helps GitLab select appropriate runners for platform-specific builds

4. **Manual Pipeline Triggers**
   - Go to: CI/CD → Pipelines → "Run pipeline"
   - Can manually run on any branch/tag for testing

---

## Issue 3: No Windows/macOS Runners Available

**Date:** October 24, 2025  
**Symptom:** Pipeline stuck with "no runners available" even after removing tags

**Root Cause:**
- GitLab.cee.redhat.com only has Linux shared runners
- No Windows or macOS runners available on corporate GitLab instance
- Pipeline was trying to run 4 jobs but only 2 could execute

**Solution:**
1. **Disable Windows/macOS Jobs:**
   - Renamed `build:windows` → `.build:windows` (dot prefix disables)
   - Renamed `build:macos` → `.build:macos`
   - Updated release job dependencies to only include Linux builds

2. **Update Release Documentation:**
   - Changed release description to "Linux Only"
   - Added link to GitHub Releases for Windows/macOS
   - Updated artifact links to only include AppImages

3. **Split Build Strategy:**
   - **GitLab:** Linux x64 + ARM64 (for internal TAMs)
   - **GitHub Actions:** All platforms (for Windows/macOS TAMs + public)

**Commits:**
- `19ecc47ea` - "fix(ci): Configure GitLab CI for Linux-only builds"
- `67d31880f` - "docs: Update distribution strategy for Linux-only GitLab builds"

**Impact:** ✅ Pipeline can now run with available runners

---

## Next Steps

- [x] Remove runner tags (use shared runners)
- [x] Fix `expire_in` variable expansion
- [x] Disable Windows/macOS builds
- [x] Update `DISTRIBUTION-STRATEGY.md`
- [ ] Monitor first successful pipeline run
- [ ] Verify Linux x64 AppImage build
- [ ] Verify Linux ARM64 AppImage build
- [ ] Test artifact downloads from GitLab Releases

---

*This document follows the Self-Healing Automation Model from AGENTS.md*

