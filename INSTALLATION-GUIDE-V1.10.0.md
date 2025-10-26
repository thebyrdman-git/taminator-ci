# Installation Guide - Taminator v1.10.0

**Product:** Taminator - RFE and Bug Tracking Automation Tool  
**Version:** 1.10.0  
**Release Date:** October 25, 2025  
**Document Version:** 1.0

---

## Document Purpose

This guide provides comprehensive installation instructions for Taminator v1.10.0 across all supported platforms. System administrators and end users will find detailed procedures for deployment, configuration, and verification.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Pre-Installation Tasks](#pre-installation-tasks)
3. [Installation Procedures](#installation-procedures)
4. [Post-Installation Configuration](#post-installation-configuration)
5. [Verification Steps](#verification-steps)
6. [Troubleshooting](#troubleshooting)
7. [Appendix](#appendix)

---

## System Requirements

### Minimum Hardware Requirements

| Component | Requirement |
|-----------|-------------|
| **Processor** | x86_64 or ARM64 (64-bit) |
| **Memory** | 2 GB RAM |
| **Disk Space** | 500 MB free space |
| **Display** | 1280x720 resolution |
| **Network** | Internet connection (Red Hat VPN required) |

### Recommended Hardware Configuration

| Component | Recommendation |
|-----------|----------------|
| **Processor** | Multi-core processor (2+ cores) |
| **Memory** | 4 GB RAM or more |
| **Disk Space** | 1 GB free space (for customer data) |
| **Display** | 1920x1080 resolution or higher |
| **Network** | Broadband connection (10+ Mbps) |

---

### Software Requirements

#### Linux Platforms

| Distribution | Versions Supported | Architecture |
|--------------|-------------------|--------------|
| **RHEL** | 8.x, 9.x | x86_64, aarch64 |
| **Fedora** | 38, 39, 40 | x86_64, aarch64 |
| **CentOS Stream** | 8, 9 | x86_64, aarch64 |
| **Ubuntu** | 20.04 LTS, 22.04 LTS, 24.04 LTS | x86_64, aarch64 |

**Required Packages:**
- FUSE 2.x or 3.x (for AppImage execution)
- X11 or Wayland display server
- GTK 3.x (bundled with AppImage)

**Optional Packages:**
- Python 3.9+ (for CLI-only usage)
- Git (for repository access)

#### macOS Platforms

| Version | Codename | Architecture |
|---------|----------|--------------|
| **macOS 11** | Big Sur | Intel, Apple Silicon |
| **macOS 12** | Monterey | Intel, Apple Silicon |
| **macOS 13** | Ventura | Intel, Apple Silicon |
| **macOS 14** | Sonoma | Intel, Apple Silicon |
| **macOS 15** | Sequoia | Intel, Apple Silicon |

#### Windows Platforms

| Version | Architecture | Status |
|---------|--------------|--------|
| **Windows 10** | x64 | ✅ Supported |
| **Windows 11** | x64 | ✅ Supported |
| **Windows Server 2019** | x64 | ✅ Supported |
| **Windows Server 2022** | x64 | ✅ Supported |

---

## Pre-Installation Tasks

### 1. Verify Network Access

**Red Hat VPN Connection:**
```bash
# Test connectivity to JIRA
ping -c 3 issues.redhat.com

# Test connectivity to Customer Portal API
curl -I https://api.access.redhat.com

# Expected: HTTP 401 Unauthorized (requires authentication)
```

### 2. Obtain API Credentials

#### JIRA API Token (Required)

1. Navigate to: https://access.redhat.com/management/api
2. Authenticate with Red Hat SSO credentials
3. Click "Generate Token" or "Create Personal Access Token"
4. Copy token value (format: `MTE1NjQyMD...`)
5. Store securely (will be needed during configuration)

#### Customer Portal API Token (Optional)

1. Log in to: https://access.redhat.com
2. Navigate to: https://access.redhat.com/management/api
3. Generate offline token
4. Copy token value
5. Store securely

### 3. Download Installation Media

**Access GitLab Repository:**
```bash
# Clone repository (requires Red Hat GitLab access)
git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git
cd taminator
```

**Or download directly:**
- Navigate to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v1.10.0
- Download appropriate package for your platform

---

## Installation Procedures

### Linux Installation (AppImage)

#### Method 1: Manual Installation

**Step 1: Download AppImage**
```bash
# For x86_64 (Intel/AMD)
wget https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v1.10.0/Taminator-1.10.0-x86_64.AppImage

# For ARM64 (Apple Silicon, Graviton)
wget https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v1.10.0/Taminator-1.10.0-arm64.AppImage
```

**Step 2: Set Execute Permissions**
```bash
chmod +x Taminator-1.10.0-*.AppImage
```

**Step 3: Run Application**
```bash
./Taminator-1.10.0-*.AppImage
```

#### Method 2: System-Wide Installation

**Step 1: Install to System Directory**
```bash
sudo mkdir -p /opt/taminator
sudo cp Taminator-1.10.0-*.AppImage /opt/taminator/
sudo chmod +x /opt/taminator/Taminator-1.10.0-*.AppImage
```

**Step 2: Create Desktop Entry**
```bash
sudo tee /usr/share/applications/taminator.desktop > /dev/null << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Taminator
Comment=RFE and Bug Tracking Tool for Red Hat TAMs
Exec=/opt/taminator/Taminator-1.10.0-x86_64.AppImage
Icon=taminator
Terminal=false
Categories=Development;Utility;
StartupWMClass=Taminator
EOF
```

**Step 3: Update Desktop Database**
```bash
sudo update-desktop-database /usr/share/applications/
```

**Step 4: Create Symbolic Link (Optional - CLI Access)**
```bash
sudo ln -s /opt/taminator/Taminator-1.10.0-*.AppImage /usr/local/bin/tam-rfe
```

#### Method 3: Per-User Installation

**Step 1: Install to User Directory**
```bash
mkdir -p ~/Applications
cp Taminator-1.10.0-*.AppImage ~/Applications/
chmod +x ~/Applications/Taminator-1.10.0-*.AppImage
```

**Step 2: Create User Desktop Entry**
```bash
mkdir -p ~/.local/share/applications
tee ~/.local/share/applications/taminator.desktop > /dev/null << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Taminator
Comment=RFE and Bug Tracking Tool for Red Hat TAMs
Exec=/home/$USER/Applications/Taminator-1.10.0-x86_64.AppImage
Icon=taminator
Terminal=false
Categories=Development;Utility;
EOF
```

**Step 3: Update User Desktop Database**
```bash
update-desktop-database ~/.local/share/applications/
```

---

### macOS Installation (DMG)

#### Step 1: Download DMG

```bash
curl -O https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v1.10.0/Taminator-1.10.0.dmg
```

#### Step 2: Mount DMG

```bash
open Taminator-1.10.0.dmg
```

Or double-click `Taminator-1.10.0.dmg` in Finder.

#### Step 3: Install Application

1. In the mounted DMG window, drag **Taminator.app** to **Applications** folder
2. Eject the DMG volume

#### Step 4: First Launch (Gatekeeper)

```bash
# Method 1: Right-click in Finder
# Right-click Taminator.app → Open → Confirm

# Method 2: Command line
xattr -dr com.apple.quarantine /Applications/Taminator.app
open /Applications/Taminator.app
```

#### Step 5: Create CLI Symlink (Optional)

```bash
# For CLI access
sudo ln -s /Applications/Taminator.app/Contents/Resources/app/tam-rfe /usr/local/bin/tam-rfe

# Verify
tam-rfe --help
```

---

### Windows Installation (NSIS Installer)

#### Step 1: Download Installer

Download `Taminator-Setup-1.10.0.exe` from GitLab releases page.

#### Step 2: Run Installer

1. Double-click `Taminator-Setup-1.10.0.exe`
2. If User Account Control (UAC) prompts, click **"Yes"**

#### Step 3: Installation Wizard

**Page 1: Welcome**
- Click **"Next"**

**Page 2: License Agreement**
- Review license terms
- Click **"I Agree"**

**Page 3: Installation Location**
- Default: `C:\Program Files\Taminator`
- Click **"Next"** (or **"Browse"** to change)

**Page 4: Start Menu Folder**
- Default: `Taminator`
- Click **"Next"**

**Page 5: Additional Tasks**
- ☑ Create Desktop Shortcut (recommended)
- ☑ Add to PATH for CLI access (recommended)
- Click **"Next"**

**Page 6: Ready to Install**
- Review settings
- Click **"Install"**

**Page 7: Completion**
- ☑ Launch Taminator
- Click **"Finish"**

#### Step 4: Verify CLI Access (Optional)

```powershell
# Open PowerShell or Command Prompt
tam-rfe --help
```

---

## Post-Installation Configuration

### Step 1: Launch Application

**Linux:**
```bash
# From terminal
./Taminator-1.10.0-*.AppImage

# Or from application launcher
# Search for "Taminator" in your desktop environment
```

**macOS:**
```bash
# From terminal
open /Applications/Taminator.app

# Or from Launchpad/Applications folder
```

**Windows:**
```powershell
# From Start Menu
# Search for "Taminator" and click icon

# Or from Desktop shortcut
```

---

### Step 2: Complete OOBE Wizard

First launch triggers the Out-of-Box Experience (OOBE) wizard.

#### Screen 1: Welcome
- Review feature overview
- Click **"Next: Set Up Authentication"**

#### Screen 2: Authentication Method
Choose between:
- **Manual Token Setup** (local storage, recommended for individuals)
- **HashiCorp Vault** (centralized, recommended for teams)

Click your choice.

#### Screen 3: Token Configuration

**For Manual Setup:**
1. Paste JIRA API token
2. (Optional) Paste Portal API token
3. Click **"Test Tokens"**
4. Verify ✅ green checkmark
5. Click **"Next: Add Your First Customer"**

**For Vault Setup:**
1. Enter Vault URL
2. Enter Vault Token
3. Enter mount point (default: `secret`)
4. Enter path (default: `taminator/tokens`)
5. Click **"Test Connection"**
6. Click **"Save Vault Config"**
7. Click **"Next: Add Your First Customer"**

#### Screen 4: Customer Onboarding (Optional)

1. Enter customer details:
   - Customer Name (display name)
   - Short Name/Slug (lowercase identifier)
   - Your Email
   - **Account Number** (required)
   - **Product** (required - dropdown selection)
2. Click **"✅ Add Customer"** or **"⏭️ Skip This Step"**

#### Screen 5: Completion
- Review summary
- Click **"Finish"**

---

### Step 3: Verify Installation

**Test 1: Application Launch**
```bash
# Application should start without errors
# Dashboard tab should be visible
```

**Test 2: Token Configuration**
```bash
# CLI verification
tam-rfe config

# Expected output:
# ✅ JIRA API Token: Configured
```

**Test 3: JIRA Connectivity**
```bash
# Test JIRA query
tam-rfe dashboard

# Expected: Customer list or "No customers yet" message
```

---

## Verification Steps

### Functional Verification

#### Test 1: Dashboard Load
1. Launch Taminator
2. Navigate to Dashboard tab
3. Verify: Summary cards visible
4. Verify: No JavaScript errors in console

#### Test 2: Customer Onboarding
```bash
tam-rfe onboard test-customer \
  --email your-email@redhat.com \
  --display-name "Test Customer" \
  --account 123456 \
  --product Ansible \
  --non-interactive
```

**Expected Output:**
```
✅ Customer 'test-customer' onboarded successfully
Report created: ~/taminator-test-data/test-customer.md
```

#### Test 3: JIRA Query
```bash
tam-rfe check test-customer
```

**Expected:** JIRA query executes (may return 0 results if account/product have no issues)

#### Test 4: CLI Access
```bash
# Verify tam-rfe command available
which tam-rfe

# Test help output
tam-rfe --help
```

### Performance Verification

#### Test 1: Application Startup Time
- Launch Taminator
- Measure time to Dashboard display
- **Expected:** < 5 seconds on recommended hardware

#### Test 2: JIRA Query Response
```bash
time tam-rfe dashboard
```
- **Expected:** < 10 seconds for typical customer load (5-10 customers)

---

## Troubleshooting

### Installation Issues

#### Issue: "Permission denied" when running AppImage

**Symptom:**
```bash
./Taminator-1.10.0-*.AppImage
bash: ./Taminator-1.10.0-x86_64.AppImage: Permission denied
```

**Cause:** Execute permission not set

**Resolution:**
```bash
chmod +x Taminator-1.10.0-*.AppImage
./Taminator-1.10.0-*.AppImage
```

---

#### Issue: "AppImage cannot be opened" on macOS

**Symptom:** Double-click DMG results in error

**Cause:** Gatekeeper security restriction

**Resolution:**
```bash
# Remove quarantine attribute
xattr -dr com.apple.quarantine /Applications/Taminator.app

# Launch
open /Applications/Taminator.app
```

---

#### Issue: Windows Installer blocks with SmartScreen

**Symptom:** "Windows protected your PC" message

**Cause:** Unsigned installer triggers SmartScreen

**Resolution:**
1. Click **"More info"**
2. Click **"Run anyway"**
3. Confirm in UAC dialog

---

### Configuration Issues

#### Issue: "JIRA token not configured"

**Symptom:** Dashboard shows error or empty

**Cause:** Token not saved or invalid

**Resolution:**
```bash
# Add token via CLI
tam-rfe config --add-token

# Or via GUI
# Settings → Vault → Add Token → Service: jira-token
```

---

#### Issue: "Vault connection failed"

**Symptom:** OOBE Vault test fails

**Cause:** Incorrect Vault URL or token

**Resolution:**
1. Verify Vault URL: `curl $VAULT_ADDR/v1/sys/health`
2. Verify token: `echo $VAULT_TOKEN`
3. Check network connectivity
4. Verify Vault permissions (read/write on secret path)

---

### Runtime Issues

#### Issue: Application won't start (black screen)

**Symptom:** Window opens but remains black

**Cause:** GPU driver incompatibility

**Resolution (Linux):**
```bash
# Disable GPU acceleration
./Taminator-1.10.0-*.AppImage --disable-gpu
```

---

#### Issue: "Connection timeout" errors

**Symptom:** Dashboard fails to load customer data

**Cause:** VPN not connected or firewall blocking

**Resolution:**
1. Verify VPN: `ping issues.redhat.com`
2. Check firewall rules (allow HTTPS/443)
3. Increase timeout: Settings → Advanced → JIRA Timeout

---

## Appendix

### A. File Locations

| Component | Location |
|-----------|----------|
| **Configuration** | `~/.config/taminator/` |
| **Tokens** | `~/.config/taminator/tokens.json` |
| **Customer Data** | `~/taminator-test-data/` |
| **OOBE State** | `~/.config/taminator-gui/oobe-state.json` |
| **Logs** | `~/.config/taminator/logs/` |

### B. Port Requirements

| Service | Protocol | Port | Purpose |
|---------|----------|------|---------|
| JIRA API | HTTPS | 443 | Issue tracking queries |
| Portal API | HTTPS | 443 | Customer Portal integration |
| Vault (optional) | HTTP/HTTPS | 8200 | Centralized secrets |

### C. Uninstallation Procedures

#### Linux
```bash
# Remove application
rm ~/Applications/Taminator-1.10.0-*.AppImage

# Remove configuration
rm -rf ~/.config/taminator/
rm -rf ~/.config/taminator-gui/

# Remove data (optional)
rm -rf ~/taminator-test-data/

# Remove desktop entry
rm ~/.local/share/applications/taminator.desktop
update-desktop-database ~/.local/share/applications/
```

#### macOS
```bash
# Remove application
rm -rf /Applications/Taminator.app

# Remove configuration
rm -rf ~/.config/taminator/

# Remove data (optional)
rm -rf ~/taminator-test-data/
```

#### Windows
1. Control Panel → Programs and Features
2. Select "Taminator"
3. Click "Uninstall"
4. Follow uninstallation wizard

---

**Document Version:** 1.0  
**Last Updated:** October 25, 2025  
**Software Version:** Taminator 1.10.0  
**Status:** General Availability (GA)

