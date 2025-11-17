# TAMINATOR Releases

Official release artifacts for TAMINATOR.

## Current Release: v2.1.3

**Release Date:** 2025-11-16  
**Type:** Backend Bundling Release - Production Ready

### Download

**Official Release (Red Hat Internal):**
- **GitLab CEE:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases
- Requires Red Hat VPN connection

**Local Artifacts (this repo):**
- [Taminator-2.1.3.AppImage](v2.1.3/Taminator-2.1.3.AppImage) (136 MB) - **Linux x86_64 - Full Functionality**

**Checksums:** [SHA256SUMS](v2.1.3/SHA256SUMS)

### What's New in v2.1.3

✅ **Full Functionality - Production Ready:**
- Backend service (19 MB) now bundled in AppImage
- Backend starts automatically with GUI
- Full JIRA integration functional
- Intelligence engine operational
- No separate installation required

🎯 **This Fixes v2.1.2:**
- v2.1.2: GUI only (backend separate)
- v2.1.3: **Complete application** (backend included)
- Zero configuration needed

📦 **What's Included:**
- Electron GUI (117 MB)
- Python backend service (19 MB)
- All dependencies bundled
- Single executable

**See:** [RELEASE-NOTES-v2.1.3.md](../RELEASE-NOTES-v2.1.3.md) for full details.

### Installation

**Linux (AppImage) - v2.1.3:**
```bash
# Connect to Red Hat VPN first
# Download from GitLab CEE Releases page
# Or use local artifact:
chmod +x Taminator-2.1.3.AppImage
./Taminator-2.1.3.AppImage
```

**macOS & Windows:**
- macOS v2.1.2 (preview): Available at [v2.1.2 release](v2.1.2/)
- macOS v2.1.3: Coming in v2.2.0
- Windows: Coming in v2.2.0

**Note:** v2.1.3 is production-ready with full functionality (backend bundled).

**Download from:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases (requires VPN)

### Verify Checksums

```bash
# Download from GitLab CEE or use local checksums
sha256sum -c SHA256SUMS

# Or verify manually
sha256sum Taminator-2.1.3.AppImage
# Should match: 74a95655963a14147bba44feff75c06e7e84fcd00486928b586fee9498c29586
```

### System Requirements

**Minimum:**
- Linux x86_64 (Ubuntu 20.04+, Fedora 38+, RHEL 8+)
- 4 GB RAM
- 500 MB disk space
- Python 3.8+ (for intelligence features)

**Recommended:**
- 8 GB RAM
- 1 GB disk space
- Python 3.11+
- LiteLLM proxy for AI features

### Documentation

- **Website:** https://taminator.dev
- [Release Notes](../RELEASE-NOTES-v2.1.3.md)
- [Build Strategy](../BUILD-STRATEGY.md)
- [Changelog](../CHANGELOG.md)

### Support

- **Issues:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
- **Discussions:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/discussions
- **Email:** jbyrd@redhat.com

### Previous Releases

- [v2.1.2](v2.1.2/) - CI/CD & Automation (Preview)
- [v2.1.1](../RELEASE-NOTES-v2.1.1.md) - Technical Debt Resolution
- [v2.0.0](v2.0.0/) - AI Intelligence Integration
- [v1.10.x](v1.10.1/) - Earlier releases

---

**Philosophy:** Container-First + Everything-as-Code + Automation-First  
**Distribution:** GitLab CEE (Red Hat Internal)  
**Documentation:** https://taminator.dev  
**CI/CD:** Hybrid (GitLab CEE + GitHub Actions)

🚀 **The Skynet TAMs Actually Want™**

