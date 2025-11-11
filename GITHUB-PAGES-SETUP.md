# GitHub Pages Setup - Private Repo, Public Docs

**Repository: Private | Documentation: Public**

---

## Overview

The setup uses:
- **Private GitHub repository** - Source files not publicly browsable
- **Public GitHub Pages** - Documentation served publicly at taminator.dev
- **GitLab CEE** - Primary source repository (internal Red Hat only)

---

## Why This Setup?

**Private Repository:**
- 🔒 Keep documentation source files private
- 🔒 Control who can see commit history
- 🔒 Prevent unauthorized modifications
- 🔒 Maintain build process privacy

**Public Documentation:**
- ✅ Taminator docs accessible to TAMs
- ✅ No login required to view docs
- ✅ Searchable by search engines (if desired)
- ✅ Professional public-facing presence

---

## GitHub Pages with Private Repos

### How It Works

GitHub Pages can publish from **private repositories**:

1. **Repository** = Private (requires authentication to browse)
2. **gh-pages branch** = Built HTML (publicly served)
3. **taminator.dev** = Public website

**Users see:** Professional documentation site  
**Users don't see:** Repository contents, source files, commits

---

## Setup Steps

### 1. Create Private Repository

```bash
# Via GitHub web interface
# https://github.com/new
# Name: taminator
# Visibility: ⚫ Private
# Initialize: No

# Or via CLI
gh repo create taminator --private --description "Taminator Documentation"
```

### 2. Add as Remote

```bash
cd /home/jbyrd/TAMINATOR

# Add GitHub as remote
git remote add github git@github.com:YOUR_USERNAME/taminator.git

# Verify
git remote -v
```

### 3. Enable GitHub Pages

```bash
# After first deployment:
# 1. Go to: https://github.com/YOUR_USERNAME/taminator/settings/pages
# 2. Under "Build and deployment":
#    - Source: Deploy from a branch
#    - Branch: gh-pages / (root)
# 3. Under "Custom domain":
#    - Domain: taminator.dev
# 4. Wait 5 minutes, then:
# 5. ✅ Enforce HTTPS
```

### 4. Configure Repository Visibility

```bash
# Verify repository is private
# Settings → General → Danger Zone → Change repository visibility
# Should show: ⚫ Private

# GitHub Pages will still be public
```

---

## GitLab CI/CD Configuration

The `.gitlab-ci.yml` handles deployment:

```yaml
deploy_github_pages:
  stage: deploy
  script:
    - mkdocs build --strict
    - git config --global user.email "ci@taminator.dev"
    - git config --global user.name "Taminator CI"
    # Deploy to private repo, public docs
    - mkdocs gh-deploy --force --remote-name github --remote-branch gh-pages
  only:
    - main
```

**Key points:**
- Uses `GITHUB_TOKEN` from GitLab variables
- Token needs `repo` scope (for private repo access)
- Pushes to `gh-pages` branch
- GitHub Pages serves from `gh-pages` publicly

---

## Access Control

### Who Can See What?

**Repository Contents (Private):**
- ❌ General public cannot view
- ✅ Repo collaborators can view
- ✅ CI/CD can access (via token)
- ✅ You control access via GitHub settings

**Documentation Site (Public):**
- ✅ Anyone can view taminator.dev
- ✅ No GitHub login required
- ✅ Search engines can index (if configured)
- ✅ Direct links work for everyone

---

## Security Benefits

### Private Repository

**Protects:**
- 🔒 Documentation source (markdown files)
- 🔒 Build configuration (mkdocs.yml)
- 🔒 CI/CD configuration
- 🔒 Commit history and contributors
- 🔒 Issue discussions (if enabled)
- 🔒 Pull request content

**Allows:**
- ✅ Public documentation serving
- ✅ Custom domain (taminator.dev)
- ✅ SSL/HTTPS
- ✅ CDN via Cloudflare

### What Gets Published

**Only published to taminator.dev:**
```
site/               # Built HTML, CSS, JS
├── index.html
├── get-started/
├── user-guide/
└── assets/
```

**NOT published:**
```
docs-site/          # Source markdown (stays private)
mkdocs.yml          # Build config (stays private)
.gitlab-ci.yml      # CI/CD config (stays private)
.git/               # Git history (stays private)
```

---

## Managing Access

### Repository Access

```bash
# Add collaborators (if needed)
# Settings → Collaborators and teams → Add people

# Or keep it completely private (just you)
```

### Documentation Access

**Public by default** once GitHub Pages is enabled. To restrict:

```bash
# Option 1: Keep repo private, Pages private
# Not applicable - we want public docs

# Option 2: Use authentication layer
# Add via Cloudflare Access or similar
# (Advanced setup, not needed for Taminator)
```

---

## Verification

### Verify Repository is Private

```bash
# Try accessing without authentication
curl -I https://github.com/YOUR_USERNAME/taminator
# Should return 404 (private repo)

# Try accessing while authenticated
gh repo view YOUR_USERNAME/taminator
# Should work
```

### Verify Documentation is Public

```bash
# Access docs without authentication
curl -I https://taminator.dev
# Should return 200 OK

# View in browser (incognito mode)
# Should load without GitHub login
```

---

## Cloudflare Configuration

Same as public repos:

**DNS Records:**
| Type | Name | Content |
|------|------|---------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | taminator.dev |

**SSL/TLS:**
- Mode: Full (strict)
- Always Use HTTPS: ✅
- Minimum TLS: 1.2

---

## Deployment Flow

```
1. GitLab CEE (Private - Internal Red Hat)
   └── Push to main branch
       ↓
2. GitLab CI/CD
   └── Build with mkdocs
       ↓
3. GitHub (Private Repository)
   └── Push to gh-pages branch
       ↓
4. GitHub Pages (Public Service)
   └── Serve HTML publicly
       ↓
5. Cloudflare (Public CDN)
   └── Cache and serve via taminator.dev
       ↓
6. Users access https://taminator.dev
   (No GitHub login required)
```

---

## Advantages

### Private Repository

✅ **Control**: Full control over who sees source  
✅ **Security**: Source files protected  
✅ **Clean**: Commit history stays private  
✅ **Professional**: No "messy" history visible  

### Public Documentation

✅ **Accessible**: No login barrier for users  
✅ **SEO**: Search engines can index (optional)  
✅ **Fast**: GitHub's CDN + Cloudflare  
✅ **Reliable**: GitHub Pages 99.9% uptime  

---

## Cost

**GitHub:**
- Private repo: Free (included with GitHub Free)
- GitHub Pages: Free (even with private repos)
- Custom domain: Free
- HTTPS: Free (Let's Encrypt)

**Cloudflare:**
- DNS: Free
- CDN: Free
- SSL: Free

**Total: $0/month** 🎉

---

## FAQ

**Q: Can people see my repository if docs are public?**  
A: No. Repository stays private. Only built HTML is public.

**Q: Can I make docs private later?**  
A: Yes. Disable GitHub Pages in settings to make docs private.

**Q: Does this work with custom domains?**  
A: Yes. taminator.dev works perfectly with private repos.

**Q: Do I need a paid GitHub plan?**  
A: No. GitHub Free includes private repos + GitHub Pages.

**Q: Can I restrict docs to specific users?**  
A: Not with standard GitHub Pages. Use Cloudflare Access for that.

---

## Summary

**Perfect setup for Taminator:**

- 🔒 **Repository**: Private (source protected)
- ✅ **Documentation**: Public (easy access for TAMs)
- 🔒 **Downloads**: GitLab CEE only (requires VPN)
- ✅ **Domain**: taminator.dev (professional)
- $0 **Cost**: Completely free

---

**Professional public docs. Private source control. Best of both worlds.**

*Powered by Ansai - Everything as Code*

**Last Updated:** November 11, 2025

