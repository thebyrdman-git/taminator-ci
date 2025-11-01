# GitHub Actions Workflows

This directory contains CI/CD workflows for Taminator.

## Workflows

### `release.yml` - Automated Release Builds

**Triggers**:
- Tag push: `git push github v*`
- Manual: GitHub Actions UI

**Builds**:
- Linux AppImage
- macOS DMG + ZIP  
- Python backend (optional)

**Output**:
- GitHub Release with all artifacts
- Automatic checksums
- Release notes

## Setup

See `/GITHUB-CI-SETUP.md` for complete instructions.

## Quick Start

```bash
# 1. Create GitHub repository
gh repo create taminator-ci --public

# 2. Add remote
git remote add github git@github.com:YOUR-ORG/taminator-ci.git

# 3. Push code
git push github main

# 4. Push tag to trigger build
git tag v2.0.1
git push github v2.0.1

# 5. Wait ~15 minutes
# 6. Download from GitHub Releases
```

