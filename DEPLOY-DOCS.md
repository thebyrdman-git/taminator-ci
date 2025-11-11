# Deploying Taminator Documentation to taminator.dev

## Overview

The Taminator documentation site is built with MkDocs Material and deployed to GitLab Pages at **https://taminator.dev**.

---

## Prerequisites

```bash
# Install MkDocs and dependencies
pip install mkdocs-material mkdocs-minify-plugin mkdocs-git-revision-date-localized-plugin
```

---

## Quick Deploy

```bash
# From TAMINATOR directory
cd /home/jbyrd/TAMINATOR

# Build and preview locally
mkdocs serve
# Visit http://localhost:8000

# Deploy to GitLab Pages (automatic via CI/CD)
git add .
git commit -m "docs: Update documentation"
git push origin main

# GitLab CI/CD will automatically build and deploy
```

---

## Manual Deployment Steps

### 1. Cloudflare DNS Setup

**Add these DNS records in Cloudflare:**

| Type | Name | Content | Proxy | TTL |
|------|------|---------|-------|-----|
| A | @ | 35.185.44.232 | ✅ Proxied | Auto |
| CNAME | www | taminator.dev | ✅ Proxied | Auto |
| TXT | _gitlab-pages-verification-code | `<from GitLab>` | ❌ DNS only | Auto |

**SSL/TLS Settings:**
- Encryption mode: **Full (strict)**
- ✅ Always Use HTTPS
- ✅ Automatic HTTPS Rewrites
- Minimum TLS: 1.2

### 2. GitLab Pages Configuration

1. Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/pages
2. Click **"New Domain"**
3. Domain: `taminator.dev`
4. Copy the verification TXT record
5. Add TXT record to Cloudflare DNS
6. Click **"Create New Domain"**
7. Wait 5-10 minutes for SSL certificate

### 3. Build Documentation Locally

```bash
cd /home/jbyrd/TAMINATOR

# Build site
mkdocs build

# Output will be in site/ directory
ls -la site/
```

### 4. Deploy via GitLab CI/CD

The `.gitlab-ci.yml` file handles automatic deployment:

```yaml
pages:
  script:
    - mkdocs build --strict
    - mv site public
  artifacts:
    paths:
      - public
  only:
    - main
```

**Trigger deployment:**
```bash
git add .
git commit -m "docs: Update documentation"
git push origin main
```

**Monitor deployment:**
- Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines
- Watch the pipeline progress
- Deployment completes in ~2-3 minutes

---

## Documentation Structure

```
TAMINATOR/
├── mkdocs.yml                    # Site configuration
├── .gitlab-ci.yml               # CI/CD configuration
├── docs-site/                   # Documentation source
│   ├── index.md                 # Homepage
│   ├── get-started/
│   ├── user-guide/
│   ├── deployment/
│   ├── architecture/
│   ├── development/
│   ├── integration/
│   ├── intelligence/
│   ├── administration/
│   ├── reference/
│   ├── about/
│   └── stylesheets/
│       └── redhat.css           # Custom Red Hat styling
└── site/                        # Built site (generated)
```

---

## Writing Documentation

### Create New Page

```bash
# Create new markdown file
vi docs-site/user-guide/new-feature.md
```

```markdown
# New Feature

Description of the feature...

## Usage

```bash
taminator command --option
```

## Examples

...
```

### Add to Navigation

Edit `mkdocs.yml`:

```yaml
nav:
  - User Guide:
    - user-guide/index.md
    - New Feature: user-guide/new-feature.md  # Add here
```

### Preview Changes

```bash
# Start live preview server
mkdocs serve

# Visit http://localhost:8000
# Changes auto-reload
```

---

## Custom Styling

Red Hat themed CSS in `docs-site/stylesheets/redhat.css`:

```css
:root {
  --md-primary-fg-color: #EE0000;        /* Red Hat Red */
  --md-primary-fg-color--light: #92001E;
  --md-primary-fg-color--dark: #A30000;
}

/* Additional custom styles... */
```

---

## Common Tasks

### Update Homepage

```bash
vi docs-site/index.md
```

### Add New Section

1. Create directory: `mkdir -p docs-site/new-section`
2. Add index: `vi docs-site/new-section/index.md`
3. Update navigation in `mkdocs.yml`

### Update Theme

```yaml
# mkdocs.yml
theme:
  name: material
  palette:
    primary: red
    accent: red
```

### Add Extension

```yaml
# mkdocs.yml
markdown_extensions:
  - your_new_extension
```

Then:
```bash
pip install your-extension-package
```

---

## Troubleshooting

### Build Fails

```bash
# Check for syntax errors
mkdocs build --strict

# Common issues:
# - Missing files referenced in nav
# - Invalid YAML in mkdocs.yml
# - Markdown syntax errors
```

### Site Not Updating

```bash
# Check GitLab CI/CD pipeline
# https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines

# Verify pages deployment
# https://gitlab.cee.redhat.com/jbyrd/taminator/-/pages

# Clear Cloudflare cache
# Cloudflare Dashboard → Caching → Purge Everything
```

### SSL Certificate Issues

```bash
# Wait 10-15 minutes after domain setup
# GitLab Pages provisions Let's Encrypt certificates automatically

# Check certificate status
curl -vI https://taminator.dev 2>&1 | grep -i cert

# Force SSL renewal (if needed)
# Remove and re-add custom domain in GitLab Pages settings
```

---

## Production Checklist

Before major documentation updates:

- [ ] Test locally with `mkdocs serve`
- [ ] Check all links work
- [ ] Verify code blocks have correct syntax highlighting
- [ ] Review navigation structure
- [ ] Check mobile responsiveness
- [ ] Commit and push to main branch
- [ ] Monitor GitLab CI/CD pipeline
- [ ] Verify deployment at https://taminator.dev
- [ ] Clear Cloudflare cache if needed

---

## Maintenance

### Update Dependencies

```bash
# Update MkDocs and plugins
pip install --upgrade mkdocs-material mkdocs-minify-plugin mkdocs-git-revision-date-localized-plugin

# Update mkdocs.yml if needed for new features
```

### Backup Documentation

```bash
# Documentation is version-controlled in Git
# Additional backup via GitLab

# Export built site
cd /home/jbyrd/TAMINATOR
mkdocs build
tar -czf taminator-docs-$(date +%Y%m%d).tar.gz site/
```

---

## Resources

- **MkDocs**: https://www.mkdocs.org/
- **Material Theme**: https://squidfunk.github.io/mkdocs-material/
- **GitLab Pages**: https://docs.gitlab.com/ee/user/project/pages/
- **Cloudflare**: https://dash.cloudflare.com/

---

**Next Steps:**

1. Add domain to Cloudflare ✅
2. Configure DNS records
3. Set up GitLab Pages custom domain
4. Push documentation updates
5. Monitor deployment
6. Visit https://taminator.dev 🎉

