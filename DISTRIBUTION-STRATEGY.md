# Taminator Distribution Strategy

**Date:** October 23, 2025  
**Version:** v1.9.5+

---

## 🎯 Primary Distribution Channel

### GitLab (Internal Red Hat TAMs) - **PRIMARY**

**Location:** https://gitlab.cee.redhat.com/jbyrd/taminator  
**Audience:** Red Hat TAMs (internal)  
**Access:** Requires Red Hat VPN + SSO

**Why GitLab Primary:**
- TAMs work inside Red Hat network
- Requires VPN for KB/T3/Portal features anyway
- Corporate compliance (internal tools on internal infrastructure)
- Single source of truth for Red Hat employees

**Build System:** GitLab CI/CD (`.gitlab-ci.yml`)
- **Linux Only:** x86_64 + ARM64 AppImages
- Builds on push to `main` and tags
- Creates GitLab Releases with artifacts
- Uses shared runners (no Windows/macOS runners available)

---

## 🌍 Secondary Distribution Channel

### GitHub (Public/External) - **MULTI-PLATFORM BUILDS**

**Location:** https://github.com/thebyrdman-git/taminator  
**Audience:** Public showcase, external TAMs, Windows/macOS users  
**Access:** Public

**Why GitHub for Multi-Platform:**
- **Free hosted runners** for Linux, Windows, and macOS
- Only platform with all 3 OS runners available
- Public visibility for portfolio/resume
- Allows external contributions
- Easier sharing with non-Red Hat folks

**Build System:** GitHub Actions (`.github/workflows/electron-build.yml`)
- **All Platforms:** Linux (x64 + ARM64), Windows (x64), macOS (Universal)
- Builds on tag push
- Creates GitHub Releases with artifacts
- Hosted runners provided by GitHub

---

## 📦 Release Workflow

### For New Versions:

1. **Develop & Test** (local or GitLab MRs)
2. **Tag Version** (e.g., `v1.9.6`)
   ```bash
   git tag v1.9.6
   git push gitlab v1.9.6    # Triggers Linux builds
   git push github v1.9.6    # Triggers all platform builds
   ```
3. **GitLab CI Builds** (automatically) - **Linux Only**
   - ✅ Linux x64 AppImage
   - ✅ Linux ARM64 AppImage (Fedora on M1/M2/M3 MacBooks)
4. **GitLab Release Created** (automatically)
   - Internal TAMs download Linux builds
   - Links to GitHub for Windows/macOS
5. **GitHub CI Builds** (automatically) - **All Platforms**
   - ✅ Linux x64 AppImage
   - ✅ Linux ARM64 AppImage
   - ✅ Windows x64 Installer
   - ✅ macOS Universal DMG (Intel + Apple Silicon)
6. **GitHub Release Created** (automatically)
   - Public/external users download any platform
   - Windows/macOS TAMs use GitHub releases

---

## 🔧 CI/CD Configuration

### GitLab CI (`.gitlab-ci.yml`)
- **Status:** ✅ Working - Linux Only (Oct 24, 2025)
- **Platforms:** Linux x64 + ARM64
- **Runners:** Uses GitLab shared runners (no tags)
- **Limitations:** 
  - No Windows/macOS runners available on gitlab.cee.redhat.com
  - Windows/macOS jobs disabled (prefixed with `.`)
- **Fixed Issues:**
  - Removed runner tags requirement
  - Changed `expire_in` from variable to direct value
  - Configured custom CI path: `taminator/.gitlab-ci.yml`

### GitHub Actions (`.github/workflows/electron-build.yml`)
- **Status:** ✅ Working - All Platforms (Oct 23, 2025)
- **Platforms:** Linux (x64 + ARM64), Windows x64, macOS Universal
- **Fixed Issues:**
  1. npm cache dependency path error
  2. Python requirements not needed
  3. Working directory path issues
  4. Missing npm scripts
  5. Repository field in package.json
  6. Windows PowerShell ls syntax
- **Runners:** GitHub-hosted (ubuntu-latest, windows-latest, macos-latest)

---

## 📄 Installation Files

### Naming Convention:
- **Linux x64:** `Taminator-{version}.AppImage`
- **Linux ARM64:** `Taminator-{version}-arm64.AppImage`
- **Windows:** `Taminator.Setup.{version}.exe`
- **macOS Intel:** `Taminator-{version}.dmg`
- **macOS ARM:** `Taminator-{version}-arm64.dmg`

### File Locations:
- **NOT in Git:** Binaries excluded (too large)
- **GitLab Releases:** Primary download location
- **GitHub Releases:** Secondary download location
- **Local `releases/` dir:** Ignored (`.gitignore`)

---

## 👥 User Personas & Download Guidance

### Primary: Red Hat TAM (Internal - Linux)
- **Needs:** RFE/Bug tracking, Portal integration
- **Access:** Red Hat VPN, SSO, KB/T3
- **Downloads From:** ✅ GitLab Releases (Linux builds)
- **Platform:** Fedora (x64 and ARM64 on Apple Silicon)

### Red Hat TAM (Internal - Windows/macOS)
- **Needs:** RFE/Bug tracking, Portal integration
- **Access:** Red Hat VPN, SSO, KB/T3
- **Downloads From:** ✅ GitHub Releases (Windows/macOS builds)
- **Platform:** Windows laptops, macOS (Intel or Apple Silicon)
- **Note:** GitLab releases link to GitHub for these platforms

### External TAMs / Community
- **Needs:** General JIRA tracking, learning tool
- **Access:** Public internet
- **Downloads From:** ✅ GitHub Releases (all platforms)
- **Platform:** Varied (Linux, Windows, macOS)

---

## 🚀 Deployment Checklist

**Before releasing a new version:**
- [ ] All tests passing locally
- [ ] Version bumped in `gui/package.json`
- [ ] CHANGELOG updated
- [ ] GitLab CI will build successfully (check .gitlab-ci.yml)
- [ ] GitHub Actions will build successfully (check .github/workflows/)
- [ ] Tag created: `git tag vX.Y.Z`
- [ ] Pushed to GitLab: `git push gitlab vX.Y.Z` ← **PRIMARY**
- [ ] Pushed to GitHub: `git push github vX.Y.Z` ← Secondary
- [ ] Wait for CI/CD to complete (~10-15 min)
- [ ] Verify GitLab Release artifacts (5 files)
- [ ] Verify GitHub Release artifacts (4 files - no ARM64 Linux)
- [ ] Test download from GitLab (at least one platform)
- [ ] Announce to TAM team (Slack, email)

---

## 📊 Build Times (Approximate)

| Platform | GitLab | GitHub |
|----------|--------|--------|
| Linux x64 | ~5 min | ~4 min |
| Linux ARM64 | ~30 min | N/A |
| Windows | ~6 min | ~3 min |
| macOS Intel | ~8 min | ~2 min |
| macOS ARM | ~8 min | ~2 min |
| **Total** | ~40-50 min | ~10-15 min |

**Note:** GitLab ARM64 build takes longer due to QEMU emulation.

---

## 🐛 Common Issues

### GitLab CI Failures:
- **Runner not available:** Check runner availability in GitLab
- **npm ci fails:** Verify `package-lock.json` exists in GUI
- **electron-builder fails:** Check package.json has repository field
- **Artifact upload fails:** Check artifact paths in `.gitlab-ci.yml`

### GitHub Actions Failures:
- **Large files rejected:** Don't commit binaries to Git
- **Build timeouts:** Check for hung processes
- **Permission errors:** Verify `GITHUB_TOKEN` has correct permissions

---

## 📝 Recent Changes (v1.9.5)

**Oct 23, 2025:**
- Fixed GitLab CI to use `electron-builder` CLI directly
- Fixed GitHub Actions (6 iterations, all issues resolved)
- Removed Python dependency steps (not needed for Electron)
- Added repository field to package.json
- Force bash shell for cross-platform compatibility

**Lessons Learned:** See `GITHUB-ACTIONS-LESSONS-LEARNED.md`

---

## 🔮 Future Improvements

1. **Code Signing**
   - macOS: Add Developer ID certificate
   - Windows: Add Authenticode certificate
   - Prevents security warnings for users

2. **Automated Testing**
   - Smoke tests before release
   - Verify AppImage launches
   - Test installer on clean VM

3. **ARM64 Native Builds**
   - Use native ARM64 runners instead of QEMU
   - Faster build times
   - Better performance

4. **Auto-Update Mechanism**
   - Built-in update checker
   - Download and install updates from GitLab
   - Notify users of new versions

---

**Remember:** GitLab is PRIMARY for TAMs. Always verify GitLab releases work before announcing.

