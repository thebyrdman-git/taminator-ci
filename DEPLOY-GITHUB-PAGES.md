# Deploy Taminator Docs to GitHub Pages

**Automated deployment via GitLab CI/CD → GitHub Pages**

---

## Overview

Taminator documentation is:
- **Source**: GitLab CEE (internal Red Hat)
- **CI/CD**: GitLab CI/CD pipeline
- **Hosting**: GitHub Pages (public docs)
- **Domain**: taminator.dev (via Cloudflare)

---

## Setup (One-Time)

### 1. Create GitHub Repository

```bash
# Option A: Via GitHub web interface
# Go to: https://github.com/new
# Name: taminator
# Visibility: Private (docs will be public via GitHub Pages)
# Initialize: No (we'll push existing code)

# Option B: Via GitHub CLI
gh repo create taminator --private --description "AI-Augmented TAM Assistant"
```

### 2. Add GitHub Remote

```bash
cd /home/jbyrd/TAMINATOR

# Add GitHub as remote (keep GitLab as origin)
git remote add github git@github.com:YOUR_USERNAME/taminator.git

# Verify remotes
git remote -v
# origin: gitlab.cee.redhat.com/jbyrd/taminator (internal)
# github: github.com/YOUR_USERNAME/taminator (public docs)
```

### 3. Configure GitLab CI/CD Variable

```bash
# In GitLab CEE:
# 1. Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/settings/ci_cd
# 2. Expand "Variables"
# 3. Add variable:
#    Key: GITHUB_TOKEN
#    Value: <your GitHub Personal Access Token>
#    Type: Variable (not file)
#    Protected: Yes
#    Masked: Yes
#    Scope: All environments

# Create GitHub token:
# 1. Go to: https://github.com/settings/tokens/new
# 2. Note: "Taminator CI/CD"
# 3. Scopes: repo (full control)
# 4. Generate token
# 5. Copy token to GitLab variable
```

### 4. Configure DNS (Cloudflare)

Add these records for **taminator.dev**:

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| A | @ | 185.199.108.153 | ✅ |
| A | @ | 185.199.109.153 | ✅ |
| A | @ | 185.199.110.153 | ✅ |
| A | @ | 185.199.111.153 | ✅ |
| CNAME | www | taminator.dev | ✅ |

### 5. Configure GitHub Pages

```bash
# After first deployment:
# 1. Go to: https://github.com/YOUR_USERNAME/taminator/settings/pages
# 2. Source: Deploy from branch → gh-pages / (root)
# 3. Custom domain: taminator.dev
# 4. Wait 5 minutes, then:
# 5. ✅ Enforce HTTPS
```

---

## Automatic Deployment

### How It Works

```
1. Push to GitLab main branch
   ↓
2. GitLab CI/CD triggered
   ↓
3. Test stage: mkdocs build --strict
   ↓
4. Deploy stage: mkdocs gh-deploy
   ↓
5. Pushes to GitHub gh-pages branch
   ↓
6. GitHub Pages publishes
   ↓
7. Available at https://taminator.dev
```

### Trigger Deployment

```bash
cd /home/jbyrd/TAMINATOR

# Make documentation changes
vi docs-site/index.md

# Commit and push to GitLab
git add docs-site/
git commit -m "docs: Update homepage"
git push origin main

# GitLab CI/CD automatically:
# - Tests build
# - Deploys to GitHub Pages
# - Site live in 2-3 minutes
```

---

## Manual Deployment

If you need to deploy manually:

```bash
cd /home/jbyrd/TAMINATOR

# Build and deploy to GitHub Pages
mkdocs gh-deploy --remote-name github --remote-branch gh-pages

# Or specify full GitHub URL
mkdocs gh-deploy --remote-branch gh-pages \
  --remote-name github \
  --force
```

---

## Monitor Deployment

### GitLab Pipeline

```bash
# View pipelines
# https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines

# Watch latest pipeline
gitlab pipeline logs

# Or via web interface:
# GitLab → CI/CD → Pipelines → Latest
```

### GitHub Pages Status

```bash
# Check deployment status
# https://github.com/YOUR_USERNAME/taminator/deployments

# Or via CLI
gh api repos/YOUR_USERNAME/taminator/pages
```

### Verify Live Site

```bash
# Check site is live
curl -I https://taminator.dev

# Should return:
# HTTP/2 200
# server: GitHub.com
```

---

## Architecture

```
┌─────────────────────────────────────┐
│   GitLab CEE (Source + CI/CD)       │
│   - Internal Red Hat network        │
│   - Source code repository          │
│   - GitLab CI/CD pipeline           │
│   - VPN required                    │
└─────────────────────────────────────┘
              ↓ (CI/CD deploys)
┌─────────────────────────────────────┐
│   GitHub (Hosting)                  │
│   - gh-pages branch only            │
│   - GitHub Pages publishes          │
│   - Public access                   │
└─────────────────────────────────────┘
              ↓ (serves via)
┌─────────────────────────────────────┐
│   Cloudflare (CDN + DNS)            │
│   - taminator.dev domain            │
│   - SSL/TLS termination             │
│   - Caching + optimization          │
└─────────────────────────────────────┘
              ↓
        taminator.dev (Users)
```

---

## Security Considerations

### What's Public vs. Private

**Public (GitHub Pages - taminator.dev):**
- ✅ Documentation site (rendered HTML only)
- ✅ Architecture diagrams
- ✅ User guides
- ✅ API documentation
- ✅ Installation instructions

**Private (GitHub Repository):**
- 🔒 Repository contents (not publicly browsable)
- 🔒 Source markdown files
- 🔒 Build configuration
- 🔒 Commit history

**Private (GitLab CEE - Internal Red Hat Only):**
- 🔒 Application source code
- 🔒 Internal notes
- 🔒 Credentials/tokens
- 🔒 Customer-specific configs
- 🔒 CI/CD variables
- 🔒 Download binaries (.AppImage, .dmg, .exe)

### Download Links

All download links point to **GitLab CEE**:
```markdown
Download from [GitLab CEE](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases)
(Requires Red Hat VPN)
```

**GitHub repo:**
- 🔒 Private repository (not publicly browsable)
- ✅ GitHub Pages enabled (docs are public)
- ❌ No releases (all releases on GitLab CEE)
- ❌ No source code (just docs build)

---

## Troubleshooting

### Pipeline Fails: "Permission denied"

**Cause:** GitHub token missing or invalid

**Fix:**
```bash
# Regenerate GitHub token
# https://github.com/settings/tokens

# Update in GitLab
# Settings → CI/CD → Variables → GITHUB_TOKEN
```

### DNS Not Resolving

**Cause:** DNS propagation or configuration issue

**Fix:**
```bash
# Check DNS
dig taminator.dev A

# Should show 4 GitHub IPs
# If not, verify Cloudflare DNS records

# Check nameservers
dig taminator.dev NS

# Should show Cloudflare nameservers
```

### SSL Certificate Error

**Cause:** GitHub Pages needs time to provision certificate

**Fix:**
```bash
# Wait 10-15 minutes after configuring custom domain
# Then enable "Enforce HTTPS" in GitHub Pages settings

# Force certificate renewal (if needed)
# Remove and re-add custom domain in GitHub
```

### Site Shows Old Content

**Cause:** Cloudflare cache

**Fix:**
```bash
# Purge Cloudflare cache
# Cloudflare Dashboard → Caching → Purge Everything

# Or wait 1-2 hours for cache expiration
```

---

## Updating Documentation

### Workflow

```bash
cd /home/jbyrd/TAMINATOR

# 1. Create branch
git checkout -b docs/update-installation

# 2. Make changes
vi docs-site/get-started/installation.md

# 3. Test locally
mkdocs serve
# Visit http://localhost:8000

# 4. Commit
git add docs-site/
git commit -m "docs: Update installation guide"

# 5. Push to GitLab
git push origin docs/update-installation

# 6. Create merge request
# GitLab → Merge Requests → New

# 7. After merge to main:
# - CI/CD automatically deploys
# - Live in 2-3 minutes
```

---

## Rollback

### Roll back to previous version

```bash
cd /home/jbyrd/TAMINATOR

# Find previous commit
git log --oneline docs-site/

# Revert to specific commit
git revert <commit-hash>

# Or reset to previous version
git reset --hard <previous-commit>

# Push to trigger redeployment
git push origin main --force

# CI/CD will deploy old version
```

---

## Maintenance

### Update MkDocs Plugins

```bash
# Update locally
pip install --upgrade mkdocs-material \
                      mkdocs-minify-plugin \
                      mkdocs-git-revision-date-localized-plugin

# Test
mkdocs build --strict

# If successful, update in CI/CD
# (CI/CD always installs latest from pip)
```

### Monitor Site Health

```bash
# Check uptime
curl -I https://taminator.dev

# Check build time
# GitLab → CI/CD → Pipelines → Duration

# Check page size
curl -s https://taminator.dev | wc -c
```

---

## Summary

**Deployment is now automatic:**

1. ✅ Edit docs in `docs-site/`
2. ✅ Commit to GitLab main branch
3. ✅ CI/CD tests and deploys
4. ✅ Live at taminator.dev in minutes

**No manual steps required!**

---

**Powered by Ansai - Everything as Code**

*GitLab CEE (source) → GitLab CI/CD (build) → GitHub Pages (host) → taminator.dev (domain)*

