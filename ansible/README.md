# Taminator Release Automation

**Ansible playbooks for automated build and release**

---

## 📋 Playbook Overview

| Playbook | Purpose | Duration | Audit Trail |
|----------|---------|----------|-------------|
| `00-pre-release-audit.yml` | Pre-release checks | 1 min | `release-audit-*.log` |
| `01-build-appimage.yml` | Build AppImage | 5-10 min | `build-appimage-*.log` |
| `02-build-deb.yml` | Verify DEB package | 1 min | `build-deb-*.log` |
| `03-build-container.yml` | Build container image | 3-5 min | `build-container-*.log` |
| `10-release-github.yml` | Push to GitHub staging | 2 min | `release-github-*.log` |
| `11-release-gitlab.yml` | Push to GitLab production | 2 min | `release-gitlab-*.log` |
| `release-all.yml` | Complete pipeline | 15-25 min | All logs |

---

## 🚀 Quick Start

### **Individual Playbooks (Recommended):**

```bash
# 1. Pre-release audit
ansible-playbook ansible/00-pre-release-audit.yml

# 2. Build AppImage
ansible-playbook ansible/01-build-appimage.yml

# 3. Verify DEB
ansible-playbook ansible/02-build-deb.yml

# 4. Build container
ansible-playbook ansible/03-build-container.yml

# 5. Release to GitHub staging
ansible-playbook ansible/10-release-github.yml

# 6. Test GitHub release, then push to GitLab
ansible-playbook ansible/11-release-gitlab.yml
```

### **Complete Pipeline (Advanced):**

```bash
# Run all steps with pauses for testing
ansible-playbook ansible/release-all.yml
```

---

## 📊 Audit Trail

Each playbook creates a timestamped log file:

```
release-audit-20251029T120000.log
build-appimage-20251029T120100.log
build-deb-20251029T120600.log
build-container-20251029T120700.log
release-github-20251029T121200.log
release-gitlab-20251029T121400.log
```

**Log Contents:**
- Timestamp and user
- All checks performed
- Build artifacts created
- Checksums (SHA256)
- Test results
- Final summary

---

## ✅ Pre-Release Audit Checks

The audit playbook verifies:

1. **No customer data** in tracked files
2. **GitIgnore working** (test files excluded)
3. **Version consistency** (package.json matches)
4. **README updated** for new version
5. **CHANGELOG exists** and updated
6. **Intelligence engine** present
7. **Container files** present
8. **Documentation** complete (10+ files)

**If audit fails, release is blocked.**

---

## 🔨 Build Process

### **AppImage Build:**
1. Install npm dependencies
2. Run `npm run build:linux`
3. Verify AppImage created
4. Extract and verify Python files
5. Calculate SHA256 checksum

### **DEB Build:**
- Built alongside AppImage
- Verified separately for audit trail

### **Container Build:**
1. Build with Podman
2. Tag with version and `latest`
3. Test intelligence engine loads
4. Verify container runs

---

## 🚀 Release Process

### **GitHub Staging:**
1. Verify working directory clean
2. Push code to `github` remote
3. Push tag `v2.1.0`
4. Verify artifacts exist
5. **Manual:** Create GitHub release and upload artifacts

### **GitLab Production:**
1. Verify working directory clean
2. Final customer data audit
3. Push code to `origin` remote (GitLab)
4. Push tag `v2.1.0`
5. Verify artifacts exist
6. **Manual:** Create GitLab release and upload artifacts

---

## 🎯 Variables

Edit at top of each playbook:

```yaml
vars:
  version: "2.1.0"  # Update for new releases
  project_root: "{{ playbook_dir | dirname }}"
  # ... other vars
```

---

## 🔐 Security

### **Customer Data Protection:**
- Pre-release audit checks for customer data
- Final audit before GitLab push
- `.gitignore` verified working
- Test files with real data excluded

### **Audit Trail:**
- Every step logged with timestamp
- SHA256 checksums for all artifacts
- User and host recorded
- Git remote URLs logged

---

## 🛠️ Troubleshooting

### **Audit Fails:**
```bash
# Check what failed
cat release-audit-*.log

# Fix issues and re-run
ansible-playbook ansible/00-pre-release-audit.yml
```

### **Build Fails:**
```bash
# Check build log
cat build-appimage-*.log

# Clean and rebuild
cd gui
rm -rf dist node_modules
npm install
cd ..
ansible-playbook ansible/01-build-appimage.yml
```

### **Push Fails:**
```bash
# Check git status
git status

# Check remotes
git remote -v

# Verify credentials
ssh -T git@github.com
ssh -T git@gitlab.cee.redhat.com
```

---

## 📝 Manual Steps

### **After GitHub Release:**
1. Go to: https://github.com/thebyrdman-git/taminator-staging/releases/new
2. Select tag: `v2.1.0`
3. Title: `Taminator Intelligence v2.1.0 - AI-Augmented TAM Assistant`
4. Copy description from `CHANGELOG.md`
5. Upload: `Taminator-2.1.0.AppImage` and `taminator-gui_2.1.0_amd64.deb`
6. Mark as "Latest release"
7. Publish

### **After GitLab Release:**
1. Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/new
2. Select tag: `v2.1.0`
3. Title: `Taminator Intelligence v2.1.0 - AI-Augmented TAM Assistant`
4. Copy description from `CHANGELOG.md`
5. Upload: `Taminator-2.1.0.AppImage` and `taminator-gui_2.1.0_amd64.deb`
6. Mark as "Latest release"
7. Publish
8. Announce to TAM team

---

## 🎓 Best Practices

### **For Development:**
- Run audit before starting builds
- Test each build individually
- Review logs after each step

### **For Production:**
- Always test GitHub staging first
- Review all logs before GitLab push
- Verify no customer data in final audit
- Keep audit logs for compliance

### **For Team:**
- Document any manual steps taken
- Share audit logs with team
- Update playbooks for new requirements

---

## 📚 Related Documentation

- [../docs/BUILD-AND-RELEASE.md](../docs/BUILD-AND-RELEASE.md) - Manual build guide
- [../docs/DEPLOYMENT-STRATEGY.md](../docs/DEPLOYMENT-STRATEGY.md) - Deployment options
- [../CHANGELOG.md](../CHANGELOG.md) - Release notes
- [../PRE-PUSH-AUDIT.md](../PRE-PUSH-AUDIT.md) - Audit requirements

---

**Automated releases with full audit trail.**

*Build once. Deploy everywhere. Audit everything.*

