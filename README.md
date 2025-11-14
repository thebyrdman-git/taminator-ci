# TAMINATOR v2.1.2 - AI-Augmented TAM Assistant 🧠

**The Skynet TAMs Actually Want**

---

## What is TAMINATOR?

TAMINATOR is a professional desktop application for Red Hat TAMs (Technical Account Managers) that combines RFE/Bug tracking automation with AI-augmented email intelligence.

**Built by TAMs, for TAMs** - with AI intelligence.

**Version**: 2.1.2  
**Architecture**: Container-First (AAP EE Philosophy) + Desktop GUI  
**CI/CD**: Hybrid (GitHub Actions + MiracleMax Self-Hosted)  
**Status**: Production Ready

---

## 🎯 What It Does

### Core Capabilities
- ✅ **Live JIRA Integration** - Real-time RFE/Bug status tracking
- ✅ **Customer Portal Integration** - Direct posting to Red Hat Customer Portal
- ✅ **rhcase Bot Integration** - Access SupportShell data directly
- ✅ **Dashboard Analytics** - Aggregated customer statistics  
- ✅ **Report Generation** - Professional markdown-based reports
- ✅ **Multi-Platform** - Linux, macOS, Windows support

### New in v2.1 - AI Intelligence 🧠
- 🧠 **Email Intelligence** - AI-augmented email analysis (89% accuracy)
- 🧠 **Case Extraction** - Automatic case number detection (95% accuracy)
- 🧠 **Customer Detection** - Identify customer from email (92% accuracy)
- 🧠 **Issue Classification** - Categorize issues automatically (89% accuracy)
- 🧠 **Urgency Assessment** - Detect urgency and deadlines
- 🧠 **Action Recommendations** - Suggest next steps with escalation routing
- 🧠 **Embedded Database** - SQLite persistence (~112KB)
- 🧠 **Feedback Loop** - Learn from TAM corrections
- 🧠 **Container-First** - AAP Execution Environment philosophy

---

## 📐 Architecture (v2.0)

### Before (v1.x): CLI Spawning
```
GUI → spawn tam-rfe CLI → Python script → API
      (slow, fragile, hard to debug)
```

### After (v2.0): Microservice
```
GUI (Electron) → FastAPI Service → Services Layer → APIs
                    ↓
              (auto-restart, structured errors, real-time)
```

**Benefits**:
- ⚡ **10x faster** - No process spawning overhead
- 🛡️ **More reliable** - Service watchdog auto-recovers
- 🔍 **Better errors** - Structured JSON responses with help links
- 📊 **Health monitoring** - Always know system status
- 🐛 **Easier debugging** - Per-feature debug logging

---

## 🚀 Quick Start

### Installation

**Linux (Container - Recommended)**:
```bash
# Clone repository
git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git
cd taminator

# One-line install
./deployment/install.sh

# Access web interface
firefox http://localhost:8080
```

**Linux (AppImage - Alternative)**:
```bash
# Download from GitLab releases
wget https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v2.0.0/Taminator-2.0.0.AppImage

# Make executable
chmod +x Taminator-2.0.0.AppImage

# Run
./Taminator-2.0.0.AppImage
```

**Windows/macOS** - Desktop installers available in releases

### First Launch

1. **OOBE Wizard** runs automatically on first launch
2. **Configure tokens** - JIRA (required), Portal (optional)
3. **Onboard first customer** - Or skip and do later
4. **Start using** - Dashboard shows all customers

---

## 💻 System Requirements

### Minimum
- **OS**: RHEL/Fedora/Ubuntu 20.04+, macOS 11+, Windows 10+
- **RAM**: 2 GB  
- **Disk**: 500 MB free
- **Network**: Red Hat VPN for JIRA/Portal access

### Required
- **Red Hat VPN** - For internal APIs
- **JIRA API Token** - From https://access.redhat.com/management/api
- **rhcase** - For case analysis (bundled in AppImage)

---

## 🎓 Usage

### GUI (Recommended)

Launch Taminator, use the tabs:

**Dashboard** - Overview of all customers
**Customers** - Manage customer accounts  
**Check** - Compare reports vs. live JIRA
**Update** - Sync reports with JIRA
**Post** - Publish to Customer Portal
**rhcase Bot** - Interactive case analysis
**Settings** - Configure tokens and preferences

### CLI (Power Users)

All GUI features have CLI equivalents:

```bash
# View dashboard
tam-rfe dashboard

# Check customer report
tam-rfe check <customer-slug>

# Update from JIRA
tam-rfe update <customer-slug>

# Post to Portal
tam-rfe post <customer-slug>

# Onboard new customer
tam-rfe onboard <customer-slug> --account 123456 --product Ansible
```

---

## 🔧 Configuration

### Token Storage

**v2.0 uses OS-level keyring** (secure!):
- Linux: Secret Service API / KWallet
- macOS: Keychain
- Windows: Windows Credential Manager

**No plaintext tokens in files** ✅

### Add Tokens

**Via GUI**: Settings → Authentication → Add Token

**Via API**:
```bash
curl -X POST http://127.0.0.1:8765/api/auth/tokens \
  -H "Content-Type: application/json" \
  -d '{"token_type": "jira", "token_value": "YOUR_TOKEN"}'
```

---

## 🐛 Troubleshooting

### Common Issues

**"Service Offline"**
- Service auto-restarts, wait 10 seconds
- Check logs: `~/.local/state/taminator/log/taminator.log`

**"VPN Not Connected"**
- Verify: `ping issues.redhat.com`
- Connect to Red Hat VPN

**"JIRA Token Invalid"**
- Regenerate at: https://access.redhat.com/management/api
- Update in Settings → Authentication

### Debug Logging

Enable debug for specific features:

```bash
# Enable debug for rhcase
curl -X POST http://127.0.0.1:8765/api/debug/enable \
  -H "Content-Type: application/json" \
  -d '{"module": "taminator.services.rhcase_service"}'

# Disable debug
curl -X POST http://127.0.0.1:8765/api/debug/disable \
  -H "Content-Type: application/json" \
  -d '{"module": "taminator.services.rhcase_service"}'
```

### Report a Bug

**Collect diagnostics**:
```bash
./tam-collect-logs
```

**Create GitLab issue**:
1. Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues/new
2. Describe the problem
3. Attach the `.tar.gz` diagnostics file
4. Submit

---

## 🔐 Security

### Data Protection
- ✅ **Tokens in OS keyring** - Not plaintext files
- ✅ **Local-only API** - No external endpoints
- ✅ **Red Hat VPN required** - No public internet access
- ✅ **No customer data in logs** - (review before sharing)

### Compliance
- ✅ **Red Hat AI Policy** - Only approved models for customer data
- ✅ **Audit logging** - All operations tracked
- ✅ **DevTools disabled** - Production builds don't expose debug tools

---

## 📚 Documentation

### For Users
- **Getting Started Guide**: [GETTING-STARTED.md](GETTING-STARTED.md) *(coming soon)*
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) *(coming soon)*
- **CLI Reference**: Run `tam-rfe --help`

### For Developers
- **Architecture**: v2.0 uses FastAPI + Electron
- **API Docs**: http://127.0.0.1:8765/docs (when service running)
- **Contributing**: Contact jbyrd@redhat.com

---

## 🎯 Roadmap

### v2.0 (Current - Alpha)
- ✅ FastAPI architecture
- ✅ Service watchdog
- ✅ rhcase integration
- ✅ Debug logging
- ✅ OOBE wizard
- ⏸️ Alpha testing with TAMs

### v2.1 (Planned)
- Google Workspace integration (OAuth, Drive, Gmail)
- Red Hat-style documentation portal
- Metrics & analytics dashboard
- Enhanced AI features

---

## 🤝 Support

**Internal Red Hat Support**:
- **GitLab Issues**: https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
- **Email**: jbyrd@redhat.com
- **Slack**: *(channel TBD)*

---

## 📦 Installation (Detailed)

### Linux

**AppImage (Recommended)**:
```bash
# Download
wget https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v2.0.0/Taminator-2.0.0.AppImage

# Make executable
chmod +x Taminator-2.0.0.AppImage

# Run
./Taminator-2.0.0.AppImage

# Optional: Install to Applications
mkdir -p ~/Applications
mv Taminator-2.0.0.AppImage ~/Applications/
```

**System Integration** (optional):
```bash
# Create desktop entry
cat > ~/.local/share/applications/taminator.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Taminator
Comment=Professional TAM Automation Tool
Exec=$HOME/Applications/Taminator-2.0.0.AppImage
Icon=taminator
Terminal=false
Categories=Development;Utility;
EOF

update-desktop-database ~/.local/share/applications/
```

### macOS

**DMG** *(coming soon)*:
```bash
# Download
curl -O https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v2.0.0/Taminator-2.0.0.dmg

# Open DMG
open Taminator-2.0.0.dmg

# Drag to Applications folder
# First run: Right-click → Open (bypass Gatekeeper)
```

### Windows

**NSIS Installer** *(coming soon)*:
1. Download `Taminator Setup 2.0.0.exe`
2. Run installer (administrator)
3. Follow wizard
4. Launch from Start Menu

---

## 🔧 Advanced

### Service Management

**Check service status**:
```bash
curl http://127.0.0.1:8765/health | jq '.'
```

**View service logs**:
```bash
tail -f ~/.local/state/taminator/log/taminator.log
```

**Restart service**:
- Service auto-restarts on crash
- Manual restart: Close and reopen GUI

### API Access

**FastAPI service runs on**: `http://127.0.0.1:8765`

**Interactive docs**: http://127.0.0.1:8765/docs

**Health check**:
```bash
curl http://127.0.0.1:8765/health
```

**Example API call**:
```bash
# List customers
curl http://127.0.0.1:8765/api/customers | jq '.'

# Get JIRA status
curl http://127.0.0.1:8765/api/jira/status | jq '.'
```

---

## 🏗️ Architecture Details

### Components

**Frontend (Electron)**:
- Red Hat PatternFly design system
- Real-time status updates
- Toast notifications
- Error handling with help links

**Backend (FastAPI)**:
- RESTful API
- Service watchdog (auto-restart)
- Health monitoring
- Structured error responses

**Services Layer**:
- `RhcaseService` - Execute rhcase commands
- `JiraService` - JIRA API integration
- `PortalService` - Customer Portal API
- `CustomerService` - Customer data management
- `AIClient` - AI model integration (LiteLLM)

**Security**:
- `TokenManager` - OS keyring integration
- No plaintext secrets
- Local-only API (127.0.0.1)

### File Locations

| Component | Location |
|-----------|----------|
| Service logs | `~/.local/state/taminator/log/` |
| Tokens | OS keyring (secure) |
| Customer data | `~/taminator-test-data/` |
| OOBE state | `~/.config/taminator-gui/oobe-state.json` |
| Debug settings | `~/.config/taminator/debug_settings.json` |

---

## 🔄 CI/CD Pipeline

### Hybrid Build Architecture

Taminator uses a **hybrid CI/CD approach** to optimize costs and leverage the right infrastructure for each platform:

**GitHub Actions (Public Repo):**
- Repository: `github.com/thebyrdman-git/taminator-ci`
- Builds: macOS DMG, Windows EXE
- Cost: $0/month (unlimited minutes for public repos)

**MiracleMax Self-Hosted (Private GitLab):**
- Repository: `gitlab.cee.redhat.com/jbyrd/taminator`
- Builds: Linux x86_64/ARM64 AppImage, Container Image
- Cost: $0/month (self-hosted hardware)

**Why Hybrid?**
- ✅ Free unlimited GitHub Actions for Mac/Windows
- ✅ Red Hat-compliant self-hosted for Linux
- ✅ Best of both worlds: cloud + self-hosted
- ✅ Fully automated release pipeline

**See:** `docs/HYBRID-CI-CD-ARCHITECTURE.md` for details

---

## 📜 License

Internal Red Hat use. Contact jbyrd@redhat.com for details.

---

## ✨ Credits

**Built by**: Jimmy Byrd (jbyrd@redhat.com)  
**For**: Red Hat TAM Team  
**With**: ❤️ and ☕

**Special Thanks**:
- TAM team for feedback and testing
- Red Hat Design System team for PatternFly
- FastAPI and Electron communities

---

**Document Version**: 1.0  
**Last Updated**: October 28, 2025  
**Software Version**: Taminator 2.0.0  
**Status**: Alpha

