# TAMINATOR

**The Skynet TAMs Actually Want** 🤖✅

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } __Get Started in 5 Minutes__

    ---

    Install Taminator and start analyzing cases with AI-powered intelligence

    [:octicons-arrow-right-24: Quick Start](get-started/quickstart.md)

-   :material-brain:{ .lg .middle } __89% Accuracy__

    ---

    AI-augmented email analysis with proven accuracy for case management

    [:octicons-arrow-right-24: How It Works](intelligence/how-it-works.md)

-   :material-docker:{ .lg .middle } __Container-First__

    ---

    AAP Execution Environment philosophy for familiar Red Hat deployment

    [:octicons-arrow-right-24: Deployment Guide](deployment/index.md)

-   :material-shield-check:{ .lg .middle } __Red Hat Compliant__

    ---

    No external APIs, offline capable, customer data stays local

    [:octicons-arrow-right-24: Security](architecture/security.md)

</div>

---

## What is TAMINATOR?

TAMINATOR is an **AI-augmented TAM assistant** that combines RFE/Bug tracking automation with intelligent email analysis. Built by TAMs, for TAMs, with AI intelligence embedded.

### Key Features

!!! info "Feature Status Legend"
    - ✅ **Available Now** - Ready to use in current release
    - 🚧 **Beta** - Available but being refined
    - 📋 **Roadmap** - Planned for future release

<div class="grid" markdown>

:material-email-search:{ .lg .middle } **Email Intelligence** ✅
:   Automatically extract case numbers, customer info, contacts, urgency, and recommended actions from emails. 89% overall accuracy. **Available Now**.

:material-database:{ .lg .middle } **Embedded Database** ✅
:   SQLite persistence for case intelligence, feedback recording, and accuracy tracking. No external services required. **Available Now**.

:material-chart-line:{ .lg .middle } **Dashboard Analytics** ✅
:   Aggregated customer statistics, RFE/Bug tracking, and performance metrics in a modern interface. **Available Now**.

:material-jira:{ .lg .middle } **JIRA Integration** ✅
:   Real-time RFE/Bug status tracking with automated report updates and portal posting. **Available Now**.

:material-robot:{ .lg .middle } **rhcase Bot Integration** ✅
:   Access SupportShell data directly from the GUI with intelligent case analysis. **Available Now**.

:material-update:{ .lg .middle } **Self-Healing** ✅
:   Systemd service integration with automatic restart, health checks, and resource limits. **Available Now**.

</div>

---

## Quick Example

!!! warning "Prerequisites"
    - Red Hat VPN access required
    - GitLab CEE credentials
    - RHEL/Fedora workstation (recommended)

```bash
# Container deployment (Recommended)
# Requires Red Hat VPN connection
git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git
cd taminator
./deployment/install.sh

# Access web interface
firefox http://localhost:8080

# Paste an email, get instant intelligence:
# ✅ Case number extracted
# ✅ Customer identified
# ✅ Contacts mapped
# ✅ Urgency assessed
# ✅ Actions recommended
```

---

## Why Taminator?

### Built for TAMs

<div class="grid" markdown>

**Familiar Architecture**
:   Same concepts as AAP Execution Environments - if you know AAP, you know Taminator

**Time Savings**
:   90%+ time savings per case (10 minutes → 30 seconds for email analysis)

**Consistent Quality**
:   Higher accuracy than manual analysis, with confidence scoring for every prediction

**Offline Capable**
:   Works without internet access, uses local pattern matching instead of external APIs

</div>

### Red Hat Aligned

- ✅ Uses Red Hat UBI9 base image
- ✅ No external API calls (offline capable)
- ✅ Customer data stays local
- ✅ Audit logs in systemd journal
- ✅ SELinux enforcing
- ✅ Non-root containers

---

## Deployment Options

!!! info "Internal Red Hat Tool"
    Taminator is an internal Red Hat TAM tool. All downloads require Red Hat VPN access and are available through **[GitLab CEE](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases)**.

Choose the deployment that fits your workflow:

=== "Container + Systemd"

    **Perfect for:** Linux servers, power users, always-on services
    
    ```bash
    # Clone from GitLab CEE (requires Red Hat VPN)
    git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git
    cd taminator
    
    # One-line install
    ./deployment/install.sh
    
    # Service starts automatically
    systemctl --user status taminator-intelligence
    ```

=== "AppImage"

    **Perfect for:** Linux desktop users, occasional use
    
    ```bash
    # Download from GitLab CEE (requires Red Hat VPN)
    # https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases
    
    chmod +x Taminator-2.0.0.AppImage
    ./Taminator-2.0.0.AppImage
    ```

=== "macOS"

    **Perfect for:** Mac users
    
    ```bash
    # Download DMG from GitLab CEE (requires Red Hat VPN)
    # https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases
    
    open Taminator-2.0.0.dmg
    # Drag to Applications
    ```

=== "Windows"

    **Perfect for:** Windows users
    
    ```bash
    # Download installer from GitLab CEE (requires Red Hat VPN)
    # https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases
    
    # Run installer
    Taminator Setup 2.0.0.exe
    ```

Each option is **first-class** - choose what works for you.

---

## Success Metrics

<div class="grid" markdown>

**95%** Case Number Accuracy
:   Automatically extracts case numbers with 95% accuracy

**92%** Customer Detection
:   Identifies customer from email domain/content with 92% accuracy

**89%** Issue Classification
:   Categorizes issues (licensing, technical, guidance, strategic) with 89% accuracy

**< 1 second** Analysis Time
:   Complete email analysis in under 1 second

</div>

---

## Get Started

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } __Install Taminator__

    ---

    Choose your platform and get started in minutes

    [:octicons-arrow-right-24: Installation Guide](get-started/installation.md)

-   :material-school:{ .lg .middle } __Learn the Basics__

    ---

    Quick tutorial to get you analyzing emails

    [:octicons-arrow-right-24: User Guide](user-guide/index.md)

-   :material-api:{ .lg .middle } __API Reference__

    ---

    Integrate Taminator with your workflows

    [:octicons-arrow-right-24: API Docs](reference/api.md)

-   :material-forum:{ .lg .middle } __Get Help__

    ---

    Join the community and get support

    [:octicons-arrow-right-24: Support](about/support.md)

</div>

---

## Latest Release

**v2.0.0** - AI-Augmented Intelligence System (October 29, 2025)

- ✅ Intelligence engine with 89% accuracy
- ✅ Embedded SQLite database
- ✅ Container-first deployment
- ✅ Systemd integration
- ✅ Cross-platform builds

[:octicons-arrow-right-24: Full Release Notes](about/release-notes.md)

---

## Community

- **GitLab**: [jbyrd/taminator](https://gitlab.cee.redhat.com/jbyrd/taminator)
- **Issues**: [Report a Bug](https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues)
- **Email**: jbyrd@redhat.com
- **Slack**: #taminator-intelligence (coming soon)

---

**Built with the AAP Execution Environment philosophy for Red Hat TAMs.**

*AI-augmented TAM assistant - From email to intelligence in 1 second.*

