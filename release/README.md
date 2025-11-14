# TAMINATOR Releases

Official release artifacts for TAMINATOR.

## Current Release: v2.1.2

**Release Date:** 2025-11-14  
**Type:** CI/CD & Automation Preview Release

### Download

**Official Release (Red Hat Internal):**
- **GitLab CEE:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases
- Requires Red Hat VPN connection

**Local Artifacts (this repo):**
- [Taminator-2.1.2.AppImage](v2.1.2/Taminator-2.1.2.AppImage) (135 MB)
- [Taminator-2.1.2.dmg](v2.1.2/Taminator-2.1.2.dmg) (130 MB)

**Checksums:** [SHA256SUMS](v2.1.2/SHA256SUMS)

### What's New in v2.1.2

🚀 **Complete CI/CD Automation:**
- 5-stage automated pipeline (lint → test → build → deploy → release)
- Multi-platform builds (Linux, macOS, Windows)
- One-command releases (`git push origin v2.1.2`)
- 20-minute automated releases

✨ **Perfect Code Quality:**
- Eliminated ALL 61 ESLint warnings → 0
- Pre-commit hooks enforcing quality
- 100% clean codebase

🧪 **Testing Infrastructure:**
- Jest framework configured
- 30% coverage threshold set
- Automated test execution in CI/CD

⚠️ **Preview Release Notice:**
- Backend service not bundled in AppImage
- GUI works, backend API unavailable
- Fix coming in v2.1.3

**See:** [RELEASE-NOTES-v2.1.2.md](../RELEASE-NOTES-v2.1.2.md) for full details.

### Installation

**Linux (AppImage):**
```bash
# Connect to Red Hat VPN first
# Download from GitLab CEE Releases page
# Or use local artifact:
chmod +x Taminator-2.1.2.AppImage
./Taminator-2.1.2.AppImage
```

**macOS (DMG):**
```bash
# Connect to Red Hat VPN first
# Download from GitLab CEE Releases page
# Or use local artifact:
open Taminator-2.1.2.dmg
# Drag to Applications
# First run: Right-click → Open (bypass Gatekeeper)
```

**Note:** v2.1.2 is a preview release. Backend service not bundled. Wait for v2.1.3 for full functionality.

**Download from:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases (requires VPN)

### Verify Checksums

```bash
# Download from GitLab CEE or use local checksums
sha256sum -c SHA256SUMS

# Or verify manually
sha256sum Taminator-2.1.2.AppImage
# Should match: e4c5073857b1a3d66bc2ee1df7e5f2ebc77d16d21cf9e2448f11aeee859ad844
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
- [Release Notes](../RELEASE-NOTES-v2.1.2.md)
- [Known Issues](../KNOWN-ISSUES-v2.1.2.md)
- [Build Strategy](../BUILD-STRATEGY.md)
- [Changelog](../CHANGELOG.md)

### Support

- **Issues:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
- **Discussions:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/discussions
- **Email:** jbyrd@redhat.com

### Previous Releases

- [v2.1.1](../RELEASE-NOTES-v2.1.1.md) - Technical Debt Resolution
- [v2.0.0](v2.0.0/) - AI Intelligence Integration
- [v1.10.x](v1.10.1/) - Earlier releases

---

**Philosophy:** Container-First + Everything-as-Code + Automation-First  
**Distribution:** GitLab CEE (Red Hat Internal)  
**Documentation:** https://taminator.dev  
**CI/CD:** Hybrid (GitLab CEE + GitHub Actions)

🚀 **The Skynet TAMs Actually Want™**

