# Taminator Releases

Official release artifacts for Taminator Intelligence.

## Current Release: v2.0.0

**Release Date:** 2025-10-29  
**Type:** Major Release - AI Intelligence Integration

### Download

**Linux x86_64:**
- [Taminator-2.0.0.AppImage](v2.0.0/linux/x86_64/Taminator-2.0.0.AppImage) (179 MB)
- [taminator-gui_2.0.0_amd64.deb](v2.0.0/linux/x86_64/taminator-gui_2.0.0_amd64.deb) (142 MB)

**Checksums:** [v2.0.0-checksums.txt](checksums/v2.0.0-checksums.txt)

### What's New in v2.0.0

🤖 **AI-Augmented Intelligence:**
- Email analysis and case classification
- Automatic urgency detection
- Contact extraction
- Recommended actions
- SQLite-based intelligence database

🐳 **Container-First Deployment:**
- Podman/Docker support
- Systemd service integration
- Execution Environment philosophy (AAP-aligned)

🏗️ **Self-Hosted CI/CD:**
- MiracleMax GitLab runner integration
- Automatic x86_64 + ARM64 builds
- Automated release creation

📊 **Intelligence Features:**
- Case history tracking
- Accuracy metrics
- Feedback loop for learning
- Pattern recognition

### Installation

**AppImage (Recommended):**
```bash
# Download
wget https://github.com/thebyrdman-git/taminator-staging/releases/download/v2.0.0/Taminator-2.0.0.AppImage

# Make executable
chmod +x Taminator-2.0.0.AppImage

# Run
./Taminator-2.0.0.AppImage
```

**DEB Package:**
```bash
# Download
wget https://github.com/thebyrdman-git/taminator-staging/releases/download/v2.0.0/taminator-gui_2.0.0_amd64.deb

# Install
sudo dpkg -i taminator-gui_2.0.0_amd64.deb
sudo apt-get install -f  # Fix dependencies if needed

# Run
taminator
```

**Container (Linux):**
```bash
# Pull and run
podman run -d \
  --name taminator-intelligence \
  --restart=unless-stopped \
  -v ~/.taminator:/root/.taminator \
  -p 8080:8080 \
  registry.gitlab.cee.redhat.com/jbyrd/taminator:v2.0.0
```

### Verify Checksums

```bash
# Download checksums
wget https://github.com/thebyrdman-git/taminator-staging/releases/download/v2.0.0/v2.0.0-checksums.txt

# Verify AppImage
sha256sum -c v2.0.0-checksums.txt --ignore-missing
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

- [Getting Started Guide](../GETTING-STARTED.md)
- [Release Workflow](../docs/RELEASE-WORKFLOW.md)
- [Container Deployment](../docs/CONTAINER-DEPLOYMENT.md)
- [Intelligence Features](../docs/EMBEDDED-INTELLIGENCE-COMPLETE.md)
- [Troubleshooting](../TROUBLESHOOTING.md)

### Support

- **Issues:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
- **Discussions:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/discussions
- **Email:** jbyrd@redhat.com

### Previous Releases

- [v1.10.1](../docs/archive/v1.x/RELEASE-NOTES-v1.10.1.md) - Bug fixes
- [v1.10.0](../docs/archive/v1.x/RELEASE-NOTES-v1.10.0.md) - Initial stable release

---

**Built with ❤️ on MiracleMax Infrastructure**  
**Self-hosted CI/CD • Red Hat Compliant • TAM-focused**

