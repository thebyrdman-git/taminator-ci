# Taminator - The Skynet TAMs Actually Want 🤖

*Your technical intelligence hub for customer engineering work.*

## Overview

Taminator is the TAM automation platform that actually understands your workflow. Stop juggling JIRA tabs, Customer Portal groups, and scattered reports. Taminator unifies RFE tracking, bug monitoring, and customer communication into one intelligent interface - with enough personality to make your day better.

**Built by TAMs, for TAMs.** Production-ready, professional when you need it, fun when you want it.

**Version:** 1.10.1  
**Release Date:** October 27, 2025  
**Product Status:** General Availability (GA)

---

## Features

### Core Capabilities
- **Live JIRA Integration:** Real-time RFE and Bug status tracking with instant updates
- **Customer Portal Integration:** Direct posting to Red Hat Customer Portal groups with live preview
- **Portal Preview Sandbox:** See exactly how your report will look before posting (no more post-oops-edit cycles)
- **Dashboard Analytics:** Aggregated customer statistics with live data and health indicators
- **Automated Report Generation:** Professional markdown-based customer reports with smart templates
- **Customer Onboarding:** Guided workflow for adding new customer accounts with auto-discovery
- **Multi-Platform Support:** Linux (x64, ARM64), macOS, and Windows - one tool, everywhere

### User Interface Options
- **Graphical Interface:** Electron-based desktop application with Red Hat PatternFly design system
- **Command-Line Tools:** Full CLI parity for automation, scripting, and power users
- **First-Run Experience:** Guided OOBE (Out-of-Box Experience) wizard - zero to productive in 2 minutes
- **Theme System:** 7 beautiful themes from Professional to Matrix hacker green (with Focus Mode for customer demos)
- **Vault Integration:** HashiCorp Vault support for team token management and enterprise deployments

---

## System Requirements

### Minimum Requirements
- **Operating System:** 
  - RHEL/Fedora/CentOS 8+
  - macOS 11+ (Big Sur or later)
  - Windows 10/11 (64-bit)
- **Memory:** 2 GB RAM
- **Disk Space:** 500 MB free space
- **Network:** Red Hat VPN access for internal API endpoints

### Software Dependencies
- **Python:** 3.9 or later (CLI tools)
- **Node.js:** Not required for AppImage/DMG/EXE installations
- **Red Hat Account:** Valid Red Hat SSO credentials
- **API Tokens:** JIRA API token (required), Portal API token (optional)

### Recommended Configuration
- **Memory:** 4 GB RAM or more
- **Disk Space:** 1 GB free space (for customer data and reports)
- **Display:** 1280x720 minimum resolution

---

## Installation

### Supported Platforms

#### Linux (AppImage)

**For Intel/AMD (x86_64):**
```bash
# Download from GitLab releases
wget https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v1.10.0/Taminator-1.10.0-x86_64.AppImage

# Make executable
chmod +x Taminator-1.10.0-x86_64.AppImage

# Run
./Taminator-1.10.0-x86_64.AppImage
```

**For ARM64 (Apple Silicon, Graviton):**
```bash
# Download ARM64 build
wget https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v1.10.0/Taminator-1.10.0-arm64.AppImage

# Make executable
chmod +x Taminator-1.10.0-arm64.AppImage

# Run
./Taminator-1.10.0-arm64.AppImage
```

**System Integration (Optional):**
```bash
# Install to user Applications directory
mkdir -p ~/Applications
cp Taminator-1.10.0-*.AppImage ~/Applications/

# Create desktop entry
cat > ~/.local/share/applications/taminator.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Taminator
Comment=RFE and Bug Tracking Tool
Exec=/home/$USER/Applications/Taminator-1.10.0-x86_64.AppImage
Icon=taminator
Terminal=false
Categories=Development;Utility;
EOF

# Update desktop database
update-desktop-database ~/.local/share/applications/
```

#### macOS (DMG)

```bash
# Download DMG
curl -O https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v1.10.0/Taminator-1.10.0.dmg

# Mount and install
open Taminator-1.10.0.dmg

# In Finder: Drag Taminator to Applications folder
# First run: Right-click → Open (to bypass Gatekeeper)
```

#### Windows (NSIS Installer)

1. Download `Taminator-Setup-1.10.0.exe` from GitLab releases
2. Run installer with administrator privileges
3. Follow installation wizard prompts
4. Launch from Start Menu or Desktop shortcut

---

## Initial Configuration

### First-Run Setup (OOBE Wizard)

Taminator includes a guided Out-of-Box Experience (OOBE) wizard that runs on first launch.

**OOBE Steps:**
1. **Welcome Screen** - Feature overview and introduction
2. **Authentication Setup** - Choose between Vault or Manual token management
3. **Token Configuration** - Add JIRA API token (required)
4. **Customer Onboarding** - Optionally add first customer (optional)
5. **Completion** - Setup complete, ready to use

**To Re-run OOBE:**
Navigate to Settings → Danger Zone → Factory Reset

### Authentication Methods

#### Method 1: Token Storage (Recommended for Individual Users)

Tokens stored locally in: `~/.config/taminator/tokens.json`

**File Permissions:** `chmod 600` (owner read/write only)

**Configuration via CLI:**
```bash
tam-rfe config --add-token
```

**Configuration via GUI:**
Settings → Vault → Add Token

#### Method 2: HashiCorp Vault (Recommended for Teams)

**Prerequisites:**
- HashiCorp Vault server (1.12.0 or later)
- Valid Vault token with read/write permissions

**Configuration:**
```bash
export VAULT_ADDR="http://vault.example.com:8200"
export VAULT_TOKEN="hvs.CAESII..."
export VAULT_MOUNT="secret"
export VAULT_PATH="taminator/tokens"
```

**Persistence (Add to `~/.bashrc` or `~/.zshrc`):**
```bash
echo 'export VAULT_ADDR="http://vault.example.com:8200"' >> ~/.bashrc
echo 'export VAULT_TOKEN="hvs.CAESII..."' >> ~/.bashrc
source ~/.bashrc
```

### Obtaining API Tokens

#### JIRA API Token (Required)

1. Navigate to: https://access.redhat.com/management/api
2. Click "Generate Token" or "Create Personal Access Token"
3. Copy token value (format: `MTE1NjQyMD...`)
4. Add to Taminator via Settings → Vault → Add Token
5. Service name: `jira-token`

#### Customer Portal API Token (Optional)

1. Log in to Red Hat Customer Portal
2. Navigate to: https://access.redhat.com/management/api
3. Generate offline token
4. Add to Taminator: Service name `portal-token`

---

## Usage

### Command-Line Interface

#### Dashboard - View All Customers
```bash
tam-rfe dashboard
```

**JSON Output (for scripting):**
```bash
tam-rfe dashboard --json
```

#### Check - Compare Report vs. Live JIRA
```bash
tam-rfe check <customer-slug>
```

**Example:**
```bash
tam-rfe check jpmc
```

#### Update - Sync Report with JIRA
```bash
tam-rfe update <customer-slug>
```

**Non-interactive mode:**
```bash
tam-rfe update <customer-slug> --yes
```

#### Post - Publish to Customer Portal
```bash
tam-rfe post <customer-slug>
```

**Dry-run (preview without posting):**
```bash
tam-rfe post <customer-slug> --dry-run
```

#### Onboard - Add New Customer
```bash
tam-rfe onboard <customer-slug> \
  --email <your-email> \
  --display-name "Customer Name" \
  --account <account-number> \
  --product <product-name>
```

**Example:**
```bash
tam-rfe onboard jpmc \
  --email jbyrd@redhat.com \
  --display-name "JPMorgan Chase" \
  --account 334224 \
  --product Ansible
```

**Non-interactive mode:**
```bash
tam-rfe onboard jpmc \
  --email jbyrd@redhat.com \
  --display-name "JPMorgan Chase" \
  --account 334224 \
  --product Ansible \
  --non-interactive
```

#### Config - Manage Tokens
```bash
# Show current configuration
tam-rfe config

# Add or update token
tam-rfe config --add-token

# Test all tokens
tam-rfe config --test-tokens
```

#### GUI - Launch Graphical Interface
```bash
tam-rfe gui
```

### Graphical User Interface

#### Dashboard Tab
- **Purpose:** Overview of all customers with live JIRA statistics
- **Features:** 
  - Summary cards (Total Customers, RFEs, Bugs, Total Issues)
  - Customer detail table with account, product, and issue counts
  - Data source indicators (🟢 Live JIRA vs 📄 Report fallback)
  - Refresh button for manual updates

#### Check Tab
- **Purpose:** Compare saved reports against live JIRA data
- **Workflow:**
  1. Select customer from dropdown
  2. Click "Compare Report vs. Live JIRA"
  3. Review differences in terminal-style output
  4. Preview report before updating

#### Update Tab
- **Purpose:** Synchronize saved reports with current JIRA status
- **Workflow:**
  1. Select customer from dropdown
  2. Click "Update from JIRA"
  3. Review update summary
  4. Backup created automatically (`.backup` file)

#### Post Tab
- **Purpose:** Publish reports to Red Hat Customer Portal
- **Workflow:**
  1. Select customer from dropdown
  2. Preview report before posting
  3. Enter Customer Portal Group ID
  4. Click "Post to Portal"
  5. Verify post success

#### Onboard Tab
- **Purpose:** Add new customer accounts
- **Workflow:**
  1. Click "+ Add Customer"
  2. Enter customer details:
     - Name (for display)
     - Slug (lowercase, no spaces)
     - Your email
     - Account number (required)
     - Product (required)
  3. Click "Discover RFEs & Bugs"
  4. Report template generated

#### Help Tab
- **Purpose:** In-application documentation
- **Sections:**
  - Getting Started
  - Command Reference
  - Workflows
  - Authentication
  - Troubleshooting
  - FAQ

#### Settings Tab
- **Purpose:** Application configuration
- **Options:**
  - Default TAM email
  - Auto-update on startup
  - Desktop notifications
  - Report format (Markdown/HTML/PDF)
  - JIRA query timeout
  - Theme selection (7 themes available)
  - Focus Mode toggle
  - Factory Reset (Danger Zone)

---

## Workflows

### Typical TAM Workflow

#### Weekly RFE/Bug Report Update

1. **Check for Changes:**
   ```bash
   tam-rfe check <customer>
   ```

2. **Update Report (if changes detected):**
   ```bash
   tam-rfe update <customer> --yes
   ```

3. **Post to Portal:**
   ```bash
   tam-rfe post <customer>
   ```

#### Onboarding New Customer

1. **Add Customer:**
   ```bash
   tam-rfe onboard <customer-slug> \
     --email <your-email> \
     --display-name "Customer Name" \
     --account <account-number> \
     --product <product>
   ```

2. **Review Generated Report:**
   ```bash
   cat ~/taminator-test-data/<customer-slug>.md
   ```

3. **Post Initial Report:**
   ```bash
   tam-rfe post <customer-slug>
   ```

#### Automation via Cron

**Daily Check (Monday-Friday at 8 AM):**
```cron
0 8 * * 1-5 /usr/local/bin/tam-rfe dashboard --json > /tmp/taminator-daily.json
```

**Weekly Update (Friday at 4 PM):**
```cron
0 16 * * 5 /usr/local/bin/tam-rfe update --all --yes
```

---

## Troubleshooting

### Common Issues

#### Issue: "JIRA token not configured"

**Cause:** Missing or invalid JIRA API token

**Resolution:**
```bash
tam-rfe config --add-token
# Select "JIRA API Token"
# Paste token from https://access.redhat.com/management/api
```

#### Issue: "Connection timeout"

**Cause:** VPN not connected or network issues

**Resolution:**
1. Verify Red Hat VPN connection:
   ```bash
   ping issues.redhat.com
   ```
2. Increase timeout in Settings → Advanced → JIRA Timeout
3. Check firewall rules

#### Issue: "Account number required"

**Cause:** Customer onboarding missing required account number

**Resolution:**
Always specify `--account` flag when onboarding:
```bash
tam-rfe onboard <customer> --account <number> --product <product>
```

#### Issue: "No customers found"

**Cause:** No customer reports in expected directories

**Resolution:**
1. Check data directory:
   ```bash
   ls -la ~/taminator-test-data/
   ```
2. Onboard at least one customer:
   ```bash
   tam-rfe onboard test-customer --account 123456 --product Ansible
   ```

#### Issue: "Failed to parse dashboard data"

**Cause:** Corrupt report file or JSON parsing error

**Resolution:**
1. Verify report files:
   ```bash
   cat ~/taminator-test-data/<customer>.md
   ```
2. Re-onboard customer if file is corrupted

### Logging and Diagnostics

**Enable Debug Mode:**
```bash
export TAMINATOR_DEBUG=1
tam-rfe <command>
```

**View Logs:**
```bash
# Application logs
tail -f ~/.config/taminator/logs/taminator.log

# System journal (if running as systemd service)
journalctl -u taminator -f
```

### Known Issues

#### RPM Package Build Failure
- **Status:** Known issue in v1.10.1
- **Workaround:** Use AppImage or .deb package
- **Resolution:** Planned for v1.11.0

#### Portal Posting Authentication
- **Status:** Requires environment variables
- **Workaround:** Set `REDHAT_PORTAL_USERNAME` and `REDHAT_PORTAL_PASSWORD`
- **Resolution:** Bearer token support planned for v1.11.0

#### JIRA Authentication Username
- **Status:** Uses default username if not configured
- **Workaround:** Set `JIRA_USERNAME` environment variable to your Red Hat email
- **Example:** `export JIRA_USERNAME="yourname@redhat.com"`

---

## Security and Compliance

### Data Protection

**Token Storage:**
- Tokens stored in `~/.config/taminator/tokens.json`
- File permissions: `600` (owner read/write only)
- No tokens transmitted to external services
- Environment variable support for CI/CD

**Customer Data:**
- All data processed locally or via Red Hat internal APIs
- No external API calls for customer information
- Red Hat VPN required for all API access
- Audit logging for all operations

### Red Hat AI Policy Compliance

Taminator adheres to Red Hat AI policies:
- ✅ Customer data processed via Red Hat-approved models only
- ✅ No external AI APIs used for customer data
- ✅ Audit logging enabled for all operations
- ✅ Secure credential management

### Network Security

**Required Network Access:**
- `issues.redhat.com` (JIRA API) - Port 443/HTTPS
- `api.access.redhat.com` (Customer Portal API) - Port 443/HTTPS

**VPN Requirement:**
Red Hat VPN connection required for all internal API endpoints.

---

## Administration

### Multi-User Deployment

**Centralized Token Management (HashiCorp Vault):**
1. Deploy Vault server for team
2. Configure Vault policies for TAM team
3. Distribute `VAULT_ADDR` and `VAULT_TOKEN` to team members
4. All TAMs share tokens from central Vault

**Ansible Deployment:**
```bash
cd ansible/
ansible-playbook -i inventory.yml playbook.yml
```

### Backup and Recovery

**Backup Customer Data:**
```bash
# Backup reports
tar -czf taminator-backup-$(date +%F).tar.gz ~/.config/taminator/ ~/taminator-test-data/
```

**Restore Customer Data:**
```bash
# Restore from backup
tar -xzf taminator-backup-2025-10-25.tar.gz -C ~/
```

### Uninstallation

**Linux:**
```bash
# Remove AppImage
rm ~/Applications/Taminator-1.10.0-*.AppImage

# Remove configuration
rm -rf ~/.config/taminator/
rm -rf ~/.config/taminator-gui/

# Remove data
rm -rf ~/taminator-test-data/

# Remove desktop entry
rm ~/.local/share/applications/taminator.desktop
update-desktop-database ~/.local/share/applications/
```

**macOS:**
```bash
# Remove application
rm -rf /Applications/Taminator.app

# Remove configuration
rm -rf ~/.config/taminator/

# Remove data
rm -rf ~/taminator-test-data/
```

**Windows:**
```powershell
# Uninstall via Control Panel
# Or use Programs and Features
# Configuration stored in: %APPDATA%\taminator
```

---

## Additional Resources

### Documentation
- **Getting Started Guide:** [docs/guides/GETTING-STARTED.md](docs/guides/GETTING-STARTED.md)
- **Installation Guide:** [docs/guides/INSTALLATION-GUIDE-V1.10.0.md](docs/guides/INSTALLATION-GUIDE-V1.10.0.md)
- **Quick Reference:** [docs/guides/QUICK-REFERENCE.md](docs/guides/QUICK-REFERENCE.md)
- **Complete Documentation Index:** [docs/README.md](docs/README.md)

### Support
- **GitLab Issues:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
- **Internal Slack:** `#tam-automation` channel
- **Email:** jbyrd@redhat.com

### Contributing
- **Development:** See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Bug Reports:** Use GitLab Issues
- **Feature Requests:** Submit via GitLab Issues with `enhancement` label

---

## Appendix

### Supported Products

| Product | SBR Group | Status |
|---------|-----------|--------|
| Ansible Automation Platform | SBR Ansible | ✅ Supported |
| Red Hat Enterprise Linux | SBR RHEL | ✅ Supported |
| OpenShift Container Platform | SBR OpenShift | ✅ Supported |
| Satellite | SBR Satellite | ✅ Supported |

### File Locations

| Component | Location |
|-----------|----------|
| Configuration | `~/.config/taminator/` |
| Token Storage | `~/.config/taminator/tokens.json` |
| Customer Reports | `~/taminator-test-data/` |
| OOBE State | `~/.config/taminator-gui/oobe-state.json` |
| Logs | `~/.config/taminator/logs/` |

### Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `VAULT_ADDR` | Vault server address | `http://vault.example.com:8200` |
| `VAULT_TOKEN` | Vault authentication token | `hvs.CAESII...` |
| `VAULT_MOUNT` | Vault secret mount point | `secret` (default) |
| `VAULT_PATH` | Vault secret path | `taminator/tokens` (default) |
| `JIRA_TOKEN_API_TOKEN` | JIRA API token | `MTE1NjQyMD...` |
| `PORTAL_TOKEN_API_TOKEN` | Portal API token | `eyJhbGc...` |
| `TAMINATOR_DEBUG` | Enable debug logging | `1` or `true` |

---

## Legal Notices

### Trademark Information
Red Hat, Red Hat Enterprise Linux, Ansible, and OpenShift are trademarks or registered trademarks of Red Hat, Inc. or its subsidiaries in the United States and other countries.

### License
This software is provided for internal Red Hat use. See repository for license details.

### Contact
For questions or support, contact: jbyrd@redhat.com

---

**Document Version:** 1.0  
**Last Updated:** October 25, 2025  
**Software Version:** Taminator 1.10.0  
**Status:** General Availability (GA)
