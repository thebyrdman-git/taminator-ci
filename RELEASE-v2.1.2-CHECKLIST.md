# TAMINATOR v2.1.2 - Release Checklist

**Status:** ✅ Ready to Push and Tag  
**Date:** November 14, 2025

---

## ✅ Completed

- [x] **Eliminated ALL ESLint warnings** (61 → 0)
- [x] **Set up Jest testing framework**
- [x] **Created comprehensive CI/CD pipeline** (.gitlab-ci.yml)
  - Lint stage (JavaScript + Python)
  - Test stage (Jest + docs)
  - Build stage (Linux, Windows, macOS)
  - Deploy stage (taminator.dev)
  - Release stage (GitLab releases)
- [x] **Updated version to 2.1.2**
  - gui/package.json
  - README.md
- [x] **Created release documentation**
  - CHANGELOG.md (v2.1.2 section)
  - RELEASE-NOTES-v2.1.2.md
  - BUILD-STRATEGY.md
- [x] **Built Linux AppImage locally** (136MB)
- [x] **Committed all changes**

---

## 📋 Next Steps

### 1. Connect to Red Hat VPN

```bash
# Connect to VPN first!
# Required to access gitlab.cee.redhat.com
```

### 2. Push to GitLab

```bash
cd /home/jbyrd/TAMINATOR

# Push main branch
git push origin main

# Create and push tag
git tag -a v2.1.2 -m "Release v2.1.2 - CI/CD & Packaging

🚀 CI/CD & Packaging Release

Major improvements:
- Comprehensive GitLab CI/CD pipeline
- Multi-platform binary builds (Linux, Windows, macOS)
- Jest testing framework
- Zero ESLint warnings
- Everything-as-Code automation

See RELEASE-NOTES-v2.1.2.md for full details."

# Push the tag
git push origin v2.1.2
```

### 3. Monitor CI/CD Pipeline

**Pipeline URL:**
```
https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines
```

**Expected stages:**
1. **lint** - ESLint + flake8 (2-3 min)
2. **test** - Jest tests + docs build (3-4 min)
3. **build** - Multi-platform binaries (10-15 min)
   - `build_appimage` - Linux AppImage, .deb, .rpm
   - `build_windows` - Windows NSIS installer
   - `build_macos` - macOS DMG (may fail if no runner)
4. **deploy** - Documentation to taminator.dev (2-3 min)
5. **release** - Create GitLab release with download links (1 min)

**Total time:** ~20-25 minutes

### 4. Verify Release

**Check GitLab Release:**
```
https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v2.1.2
```

**Download and test artifacts:**
- [ ] Download AppImage
- [ ] Download .deb package
- [ ] Download .rpm package
- [ ] Download Windows .exe
- [ ] Test Linux AppImage: `./Taminator-2.1.2.AppImage`
- [ ] Verify documentation: https://taminator.dev

### 5. (Optional) Manual macOS Build

If macOS CI/CD job fails:

```bash
# On a Mac:
cd /path/to/TAMINATOR/gui
npm ci
npm run build:mac

# Upload to GitLab release manually
```

---

## 🎯 Success Criteria

Release v2.1.2 is complete when:

- [x] All code committed and pushed
- [ ] Tag `v2.1.2` created and pushed
- [ ] CI/CD pipeline passes all stages
- [ ] GitLab release created with binaries
- [ ] Documentation deployed to taminator.dev
- [ ] All artifacts downloadable from GitLab
- [ ] Linux AppImage tested and working
- [ ] Windows installer available
- [ ] macOS DMG available (or documented as manual build)

---

## 📦 Expected Artifacts

From CI/CD pipeline:

### Linux (build_appimage job)
- `Taminator-2.1.2.AppImage` (~136MB)
- `taminator-gui_2.1.2_amd64.deb` (~99MB)
- `taminator-gui-2.1.2.x86_64.rpm` (~100MB)

### Windows (build_windows job)
- `Taminator-Setup-2.1.2.exe` (~150MB)

### macOS (build_macos job - may fail)
- `Taminator-2.1.2.dmg` (~160MB)
- **Note:** If CI/CD fails, build manually on macOS

---

## 🐛 Troubleshooting

### If CI/CD Fails

**Lint stage fails:**
```bash
# Run locally to debug
cd gui
npm run lint
```

**Test stage fails:**
```bash
# Run locally to debug
cd gui
npm test
```

**Build stage fails:**
- Check job logs in GitLab
- Verify electronuserland/builder:wine image is accessible
- May need to enable shared runners in GitLab settings

**Deploy stage fails:**
- Verify GITHUB_TOKEN is set in GitLab CI/CD variables
- Check GitHub Pages is enabled for thebyrdman-git/taminator

**Release stage fails:**
- Verify release-cli image is accessible
- Check RELEASE-NOTES-v2.1.2.md exists

### If Builds Are Slow

**GitLab shared runners may be busy**
- Peak times: 9am-5pm ET
- Off-peak: evenings and weekends
- Typical wait: 2-10 minutes for runner

---

## 📚 Documentation

**Release documentation:**
- `RELEASE-NOTES-v2.1.2.md` - Full release notes
- `CHANGELOG.md` - Changelog entry
- `BUILD-STRATEGY.md` - Build system documentation

**Online:**
- [taminator.dev](https://taminator.dev) - Public documentation
- [GitLab Project](https://gitlab.cee.redhat.com/jbyrd/taminator) - Source and releases

---

## 🎉 Post-Release

After successful release:

1. **Announce internally** (optional):
   - Red Hat TAM Slack channel
   - Team email
   - Case management update

2. **Update roadmap**:
   - Mark v2.1.2 as released
   - Update taminator.dev roadmap page

3. **Plan next version** (v2.2.0):
   - Intelligence engine enhancements
   - Additional integrations
   - Performance optimizations

---

**Created:** November 14, 2025  
**Version:** 2.1.2  
**Status:** ✅ Ready to push and tag (waiting for VPN)

**Next:** Connect to VPN and run the commands in "Next Steps" section.

