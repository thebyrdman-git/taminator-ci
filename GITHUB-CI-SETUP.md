# GitHub CI/CD Setup for Taminator

**Purpose**: Automate multi-platform builds (Linux + macOS) using GitHub Actions  
**Repository**: `github.com/your-org/taminator-ci`  
**Status**: Ready to deploy

---

## 🚀 Quick Start

### 1. Create GitHub Repository

```bash
# Option A: Create on GitHub.com
# Go to https://github.com/new
# Name: taminator-ci
# Description: Taminator Intelligence - CI/CD Pipeline
# Private or Public (your choice)

# Option B: Use GitHub CLI
gh repo create taminator-ci --public --description "Taminator CI/CD Pipeline"
```

### 2. Push Code to GitHub

```bash
cd /home/jbyrd/TAMINATOR

# Add GitHub remote
git remote add github https://github.com/YOUR-USERNAME/taminator-ci.git

# Or if using SSH:
git remote add github git@github.com:YOUR-USERNAME/taminator-ci.git

# Push code
git push github main

# Push tags
git push github --tags
```

### 3. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click "Actions" tab
3. GitHub Actions should be automatically enabled
4. The workflow file is already in `.github/workflows/release.yml`

---

## 📋 Workflow Overview

The CI/CD pipeline automatically triggers on:
- **Tag push**: `git push github v2.0.1`
- **Manual trigger**: From GitHub Actions UI

### Jobs

```
┌─────────────────────────────────────────┐
│  Pre-Build Checks                       │
│  • ESLint validation                    │
│  • Version consistency check            │
└────────────┬────────────────────────────┘
             │
             ├──────────┬──────────────┐
             ▼          ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Linux Build  │ │ macOS Build  │ │ Python Build │
│ • AppImage   │ │ • DMG        │ │ • Package    │
│ • Checksums  │ │ • ZIP        │ │ • Tests      │
└──────┬───────┘ └──────┬───────┘ └──────────────┘
       │                │
       └────────┬───────┘
                ▼
    ┌────────────────────┐
    │ Create Release     │
    │ • Combine artifacts│
    │ • Upload to GitHub │
    │ • Generate notes   │
    └────────┬───────────┘
             ▼
    ┌────────────────────┐
    │ Notify Success     │
    └────────────────────┘
```

---

## 🔧 Configuration

### Repository Secrets (Optional)

For code signing and advanced features:

```bash
# GitHub repository → Settings → Secrets and variables → Actions

# macOS Code Signing
APPLE_ID                  # your@email.com
APPLE_ID_PASSWORD         # app-specific password
APPLE_TEAM_ID             # Your team ID
CSC_LINK                  # Base64 encoded certificate
CSC_KEY_PASSWORD          # Certificate password

# Notifications (optional)
SLACK_WEBHOOK_URL         # For Slack notifications
DISCORD_WEBHOOK_URL       # For Discord notifications
```

### Without Code Signing

The workflow works without signing! Users will see:
- macOS: "App from unidentified developer" → Right-click → Open
- This is normal for unsigned apps

---

## 🎯 Usage

### Automated Release (Recommended)

```bash
cd /home/jbyrd/TAMINATOR

# Update version
cd gui
npm version patch  # 2.0.1 → 2.0.2
cd ..

# Commit changes
git add gui/package.json gui/package-lock.json
git commit -m "Bump version to 2.0.2"

# Create and push tag
git tag -a v2.0.2 -m "Release v2.0.2"
git push github main
git push github v2.0.2

# ✨ GitHub Actions automatically:
# 1. Runs ESLint checks
# 2. Builds Linux AppImage
# 3. Builds macOS DMG + ZIP
# 4. Creates GitHub Release
# 5. Uploads all files
```

**Wait time**: 10-15 minutes for all builds

---

### Manual Trigger

1. Go to GitHub Actions tab
2. Select "Release Build" workflow
3. Click "Run workflow"
4. Enter version number (e.g., `2.0.1`)
5. Click "Run workflow"

---

### Local Build + CI Deploy

```bash
# Build locally with Ansible
ansible-playbook ansible/playbooks/taminator-release.yml

# Test locally
./releases/v2.0.1/Taminator-2.0.1.AppImage

# If good, trigger CI for macOS
git push github v2.0.1

# CI will add macOS builds to the same release
```

---

## 📦 Artifacts

### What Gets Built

| Platform | Artifact | Size | Runner |
|----------|----------|------|--------|
| Linux | Taminator-X.Y.Z.AppImage | ~136 MB | ubuntu-latest |
| macOS | Taminator-X.Y.Z.dmg | ~120 MB | macos-latest |
| macOS | Taminator-X.Y.Z-mac.zip | ~115 MB | macos-latest |
| - | SHA256SUMS | <1 KB | - |

### Download URLs

After release, files available at:
```
https://github.com/YOUR-ORG/taminator-ci/releases/download/v2.0.1/Taminator-2.0.1.AppImage
https://github.com/YOUR-ORG/taminator-ci/releases/download/v2.0.1/Taminator-2.0.1.dmg
https://github.com/YOUR-ORG/taminator-ci/releases/download/v2.0.1/Taminator-2.0.1-mac.zip
https://github.com/YOUR-ORG/taminator-ci/releases/download/v2.0.1/SHA256SUMS
```

---

## 🔍 Monitoring Builds

### GitHub Actions UI

1. Go to repository on GitHub
2. Click "Actions" tab
3. See all workflow runs
4. Click on a run to see details
5. Download artifacts (if needed before release)

### Check Status

```bash
# Using GitHub CLI
gh run list --repo YOUR-ORG/taminator-ci

# Watch a specific run
gh run watch RUN_ID --repo YOUR-ORG/taminator-ci

# View logs
gh run view RUN_ID --log --repo YOUR-ORG/taminator-ci
```

---

## 🐛 Troubleshooting

### Build Fails on ESLint

```yaml
# Temporary: Make ESLint non-blocking
- name: Run ESLint
  run: npx eslint public/js/*.js || true
  continue-on-error: true
```

### macOS Build Fails

**Issue**: Code signing error

**Fix**: Disable code signing
```yaml
env:
  CSC_IDENTITY_AUTO_DISCOVERY: false
```

### Version Mismatch

**Issue**: Tag version != package.json version

**Fix**: Update package.json before tagging
```bash
cd gui
npm version 2.0.1 --no-git-tag-version
git add package.json package-lock.json
git commit -m "Bump version"
git tag v2.0.1
```

---

## 🔐 Security

### Secrets Management

- Never commit secrets to git
- Use GitHub Secrets for sensitive data
- Rotate credentials regularly

### Code Signing (Production)

For production releases with code signing:

1. Get Apple Developer certificate
2. Export certificate as .p12
3. Base64 encode: `base64 certificate.p12 > cert.txt`
4. Add to GitHub Secrets as `CSC_LINK`
5. Add password as `CSC_KEY_PASSWORD`

Update workflow:
```yaml
env:
  APPLE_ID: ${{ secrets.APPLE_ID }}
  APPLE_ID_PASSWORD: ${{ secrets.APPLE_ID_PASSWORD }}
  CSC_LINK: ${{ secrets.CSC_LINK }}
  CSC_KEY_PASSWORD: ${{ secrets.CSC_KEY_PASSWORD }}
```

---

## 📊 Cost

### GitHub Actions Free Tier

- **Linux**: 2,000 minutes/month free
- **macOS**: 10x multiplier (200 effective minutes)
- **Storage**: 500 MB artifacts (30 days retention)

### Typical Usage

- One complete release: ~15 minutes
- Linux build: ~5 minutes (5 minutes used)
- macOS build: ~10 minutes (100 minutes used)
- **Total per release**: 105 minutes

**Releases per month (free tier)**: ~15-20 releases

---

## 🚀 Advanced Features

### Add Windows Support

```yaml
build-windows:
  runs-on: windows-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
    - run: npm ci
      working-directory: gui
    - run: npm run build:win
      working-directory: gui
    - uses: actions/upload-artifact@v4
      with:
        name: windows-builds
        path: gui/dist/*.exe
```

### Add Notifications

```yaml
- name: Notify Slack
  if: success()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
    payload: |
      {
        "text": "✅ Taminator v${{ steps.version.outputs.version }} released!"
      }
```

### Add Automated Testing

```yaml
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
    - run: npm ci && npm test
      working-directory: gui
```

---

## 📝 Integration with Ansible

### Update Ansible Release Playbook

Add CI trigger option:

```yaml
- name: "🚀 Trigger GitHub Actions build"
  shell: |
    cd {{ project_root }}
    
    # Push tag to GitHub
    git push github v{{ new_version }}
    
    echo "✅ Triggered GitHub Actions build"
    echo "Monitor at: https://github.com/YOUR-ORG/taminator-ci/actions"
    echo ""
    echo "macOS builds will be available in ~10 minutes"
  when: trigger_ci|default(false)|bool
```

Usage:
```bash
ansible-playbook taminator-release.yml -e trigger_ci=true
```

---

## 🎯 Best Practices

### 1. Test Before Tagging

```bash
# Test build locally first
npm run build:linux

# If successful, then tag
git tag v2.0.1
git push github v2.0.1
```

### 2. Use Semantic Versioning

- **Major**: v3.0.0 (breaking changes)
- **Minor**: v2.1.0 (new features)
- **Patch**: v2.0.1 (bug fixes)

### 3. Write Good Release Notes

Create `RELEASE-NOTES-X.Y.Z.md` before tagging:
- CI will automatically include it in GitHub Release
- Makes releases more professional

### 4. Monitor First Build

Watch the first CI build to ensure everything works:
```bash
gh run watch --repo YOUR-ORG/taminator-ci
```

---

## 📞 Support

### Resources

- **Workflow File**: `.github/workflows/release.yml`
- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **electron-builder CI**: https://www.electron.build/configuration/configuration.html#ci

### Troubleshooting

```bash
# View recent runs
gh run list --repo YOUR-ORG/taminator-ci

# View specific run
gh run view RUN_ID --log

# Re-run failed build
gh run rerun RUN_ID

# Cancel running build
gh run cancel RUN_ID
```

---

## ✅ Setup Checklist

- [ ] Create taminator-ci repository on GitHub
- [ ] Push code to GitHub
- [ ] Verify `.github/workflows/release.yml` exists
- [ ] Enable GitHub Actions
- [ ] Create test tag and push
- [ ] Monitor first build
- [ ] Verify artifacts are created
- [ ] Download and test builds
- [ ] Document repository URL for team
- [ ] Add repository to release playbook

---

**Repository**: `github.com/YOUR-ORG/taminator-ci`  
**Workflow**: `.github/workflows/release.yml`  
**Status**: ✅ Ready to use  
**Cost**: Free (within GitHub Actions limits)  

🚀 **Automated multi-platform builds in 15 minutes!**


