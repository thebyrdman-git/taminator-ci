# Getting Started with Taminator

**Product:** Taminator - RFE and Bug Tracking Automation Tool  
**Version:** 1.10.0  
**Audience:** Red Hat Technical Account Managers (TAMs)  
**Time to Complete:** 15 minutes

---

## Overview

This guide provides step-by-step instructions for installing, configuring, and using Taminator for the first time. By the end of this guide, you will have:

- ✅ Installed Taminator on your workstation
- ✅ Configured authentication credentials
- ✅ Onboarded your first customer
- ✅ Generated your first RFE/Bug report

---

## Prerequisites

Before beginning installation, verify you have:

| Requirement | Description | Verification |
|-------------|-------------|--------------|
| **Red Hat VPN** | Active VPN connection | `ping issues.redhat.com` |
| **Red Hat Account** | Valid SSO credentials | Login to access.redhat.com |
| **JIRA API Token** | Personal access token | Generated at access.redhat.com/management/api |
| **Customer Data** | Account number and product | Obtain from customer relationship records |

---

## Step 1: Installation

### 1.1 Download Taminator

**Linux (x86_64):**
```bash
wget https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v1.10.1/Taminator-1.10.1.AppImage
```

**Linux (ARM64 - Apple Silicon Macs):**
```bash
wget https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v1.10.1/Taminator-1.10.1-arm64.AppImage
```

**macOS:**
```bash
curl -O https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v1.10.1/Taminator-1.10.1.dmg
```

**Windows:**
Download `Taminator-Setup-1.10.0.exe` from GitLab releases page.

---

### 1.2 Install Application

**Linux:**
```bash
# Make executable
chmod +x Taminator-1.10.0-*.AppImage

# Run directly (no installation required)
./Taminator-1.10.0-*.AppImage
```

**Optional - System Integration:**
```bash
# Install to Applications directory
mkdir -p ~/Applications
mv Taminator-1.10.0-*.AppImage ~/Applications/

# Create desktop entry for application launcher
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

**macOS:**
```bash
# Mount DMG
open Taminator-1.10.0.dmg

# Drag Taminator.app to Applications folder
# First launch: Right-click → Open (bypass Gatekeeper)
```

**Windows:**
```powershell
# Run installer
.\Taminator-Setup-1.10.0.exe

# Follow installation wizard
# Choose installation directory (default: C:\Program Files\Taminator)
# Select Start Menu integration
# Complete installation
```

---

## Step 2: First Launch (OOBE Wizard)

### 2.1 Welcome Screen

On first launch, Taminator displays an Out-of-Box Experience (OOBE) wizard.

**What to expect:**
- Welcome message with feature overview
- Visual demonstration of tool capabilities
- Progress indicator (20% → 100%)

**Action:** Click **"Next: Set Up Authentication"**

---

### 2.2 Authentication Setup

Choose your token storage method:

#### Option A: Manual Token Setup (Recommended for Individual Users)

**Description:** Tokens stored locally in `~/.config/taminator/tokens.json`

**Advantages:**
- ✅ No external dependencies
- ✅ Works offline
- ✅ Simple configuration
- ✅ 5-minute setup

**Disadvantages:**
- ❌ Tokens stored per machine
- ❌ No team sharing

**Action:** Click **"Manual Token Setup"** → Proceed to Step 2.3

#### Option B: HashiCorp Vault (Recommended for Teams)

**Description:** Centralized secrets management with audit logging

**Prerequisites:**
- HashiCorp Vault server (version 1.12.0+)
- Valid Vault token with read/write permissions
- Network connectivity to Vault server

**Configuration:**
```bash
export VAULT_ADDR="http://vault.example.com:8200"
export VAULT_TOKEN="hvs.CAESII..."
```

**Advantages:**
- ✅ Centralized token management
- ✅ Team collaboration
- ✅ Audit logging
- ✅ Multi-machine access

**Disadvantages:**
- ❌ Requires Vault infrastructure
- ❌ Initial setup complexity

**Action:** Click **"Set Up Vault"** → Enter connection details

---

### 2.3 Token Configuration

#### 2.3.1 Obtain JIRA API Token

1. **Navigate to:** https://access.redhat.com/management/api
2. **Click:** "Generate Token" or "Create Personal Access Token"
3. **Copy token:** Format `MTE1NjQyMD...` (long alphanumeric string)
4. **Save securely:** You'll need this in next step

#### 2.3.2 Add Token to Taminator

**In OOBE Wizard:**
1. Paste JIRA token in "JIRA API Token" field
2. (Optional) Paste Portal token in "Portal API Token" field
3. Click **"Test Tokens"** to verify connectivity
4. If successful: ✅ Green checkmark appears
5. If failed: ❌ Red error message with troubleshooting steps
6. Click **"Next: Add Your First Customer"** (or skip)

---

## Step 3: Customer Onboarding

### 3.1 Gather Customer Information

Before onboarding, collect:

| Information | Example | Source |
|-------------|---------|--------|
| **Customer Name** | JPMorgan Chase | Customer relationship records |
| **Account Number** | 334224 | Red Hat account database |
| **Product** | Ansible Automation Platform | Customer subscription |
| **Your Email** | jbyrd@redhat.com | Your Red Hat email |

---

### 3.2 Add Customer via OOBE

**In OOBE Wizard:**
1. **Customer Name:** Enter display name (e.g., "JPMorgan Chase")
2. **Short Name (Slug):** Enter lowercase identifier (e.g., "jpmc")
3. **Your Email:** Enter your Red Hat email
4. **Account Number:** Enter customer account number (required)
5. **Product:** Select from dropdown (Ansible, RHEL, OpenShift, etc.)
6. Click **"✅ Add Customer"**

**System Actions:**
- Queries JIRA for open RFEs and Bugs
- Filters by account number and product (SBR group)
- Generates initial report template
- Saves to `~/taminator-test-data/<slug>.md`

**Expected Result:**
```
✅ Customer Added Successfully!
Found 12 open RFEs and Bugs for JPMorgan Chase (Account: 334224, Product: Ansible)
Report saved to: ~/taminator-test-data/jpmc.md
```

---

### 3.3 Complete OOBE

Click **"Finish"** to exit wizard and enter main application.

**Post-OOBE:**
- Dashboard loads automatically
- Customer appears in customer list
- Live JIRA stats displayed (if token configured)

---

## Step 4: Using Taminator

### 4.1 Dashboard Overview

**Navigation:** Dashboard tab (home icon)

**Features:**
- **Summary Cards:** Total customers, RFEs, Bugs, Total Issues
- **Customer Table:** Detailed view with account, product, counts
- **Data Source:** 🟢 Live JIRA or 📄 Report fallback
- **Last Modified:** Report update timestamp

**Actions:**
- **Refresh Dashboard:** Updates all customer stats from JIRA
- **Add Customer:** Launch customer onboarding wizard
- **Manage Tokens:** Navigate to token management

---

### 4.2 Check Report Status

**Purpose:** Compare saved report against current JIRA data

**Navigation:** Check tab → Select customer → Click "Compare Report vs. Live JIRA"

**Output:**
```
Checking JIRA for account 334224 (Ansible)...
Found 12 open RFEs and Bugs

✅ 3 status changes detected
⚠️  [RFE] AAP-12345: In Progress → Post
└─ Linked to case 03891234
⚠️  [BUG] AAP-67890: Backlog → In Progress
└─ Linked to case 03892345
⚠️  [RFE] AAP-11111: New → Refinement
└─ Linked to case 03893456
```

**Interpretation:**
- **Green ✅:** Changes detected, update recommended
- **Yellow ⚠️:** Specific issues with status changes
- **Red ❌:** Errors or failures

---

### 4.3 Update Report

**Purpose:** Synchronize saved report with latest JIRA data

**Navigation:** Update tab → Select customer → Click "Update from JIRA"

**Process:**
1. System fetches current JIRA data
2. Compares with saved report
3. Creates backup (`.backup` extension)
4. Updates report with new statuses
5. Adds "Last Updated" timestamp

**Safety Features:**
- ✅ Automatic backup before updating
- ✅ Preserves custom formatting
- ✅ Rollback available (restore from `.backup`)

---

### 4.4 Post to Customer Portal

**Purpose:** Publish report to Red Hat Customer Portal group

**Prerequisites:**
- Portal API token configured
- Customer Portal Group ID
- Red Hat VPN connection

**Navigation:** Post tab → Select customer → Click "Post to Portal"

**Workflow:**
1. Enter Customer Portal Group ID
2. (Optional) Preview report before posting
3. Click "Publish"
4. Verify success message with Portal URL

**Example:**
```
✅ Posted to Customer Portal
→ https://access.redhat.com/groups/1234567/discussions/7891011
```

---

## Step 5: Command-Line Usage

### 5.1 CLI Access

**Linux/macOS:**
```bash
# Add to PATH (one-time setup)
ln -s ~/Applications/Taminator-1.10.0-x86_64.AppImage /usr/local/bin/tam-rfe

# Verify installation
tam-rfe --help
```

**Windows:**
```powershell
# CLI automatically added to PATH during installation
tam-rfe --help
```

---

### 5.2 Common CLI Operations

**View Dashboard:**
```bash
tam-rfe dashboard
```

**Check Customer:**
```bash
tam-rfe check jpmc
```

**Update Report:**
```bash
tam-rfe update jpmc --yes
```

**Post to Portal:**
```bash
tam-rfe post jpmc
```

**Onboard New Customer:**
```bash
tam-rfe onboard <customer-slug> \
  --email jbyrd@redhat.com \
  --display-name "Customer Name" \
  --account 123456 \
  --product Ansible \
  --non-interactive
```

---

## Troubleshooting

### Issue: OOBE doesn't appear on first launch

**Cause:** OOBE state file exists from previous installation

**Resolution:**
```bash
# Remove OOBE state
rm ~/.config/taminator-gui/oobe-state.json

# Relaunch Taminator
./Taminator-1.10.0-*.AppImage
```

---

### Issue: "JIRA token not configured" error

**Cause:** Token not saved or invalid token format

**Resolution:**
1. Navigate to Settings → Vault → Add Token
2. Service name: `jira-token`
3. Paste token from https://access.redhat.com/management/api
4. Click "Save"
5. Click "Test Token" to verify

---

### Issue: "Connection timeout" when checking JIRA

**Cause:** VPN not connected or firewall blocking

**Resolution:**
1. Verify VPN connection:
   ```bash
   ping issues.redhat.com
   ```
2. Verify firewall rules allow HTTPS (port 443)
3. Increase timeout: Settings → Advanced → JIRA Timeout → 60 seconds

---

### Issue: Dashboard shows "No customers yet"

**Cause:** No customer reports exist

**Resolution:**
1. Onboard at least one customer:
   ```bash
   tam-rfe onboard test-customer --account 123456 --product Ansible
   ```
2. Verify report created:
   ```bash
   ls ~/taminator-test-data/
   ```

---

## Next Steps

### Explore Features
- ✅ **Dashboard:** Monitor all customers at once
- ✅ **Check:** Verify report accuracy
- ✅ **Update:** Keep reports current
- ✅ **Post:** Automate Portal communication
- ✅ **Help Tab:** In-app documentation

### Customize Experience
- **Themes:** Settings → Theme Gallery (7 themes available)
- **Focus Mode:** Settings → Toggle for professional mode
- **Notifications:** Settings → Enable desktop notifications

### Automation
- **Weekly Updates:** Schedule cron job for automatic updates
- **Dashboard Monitoring:** Daily JIRA checks
- **Report Distribution:** Automate Portal posting

---

## Additional Resources

### Documentation
- **User Guide:** [README.md](README.md)
- **Release Notes:** [RELEASE-NOTES-v1.10.0.md](RELEASE-NOTES-v1.10.0.md)
- **CLI Reference:** Run `tam-rfe --help`

### Support
- **GitLab Issues:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
- **Slack:** `#tam-automation` (internal)
- **Email:** jbyrd@redhat.com

### Training
- **In-App Help:** Help tab (comprehensive documentation)
- **Video Tutorials:** Coming in v1.11.0
- **Team Training:** Contact jbyrd@redhat.com

---

## Summary

You have successfully:
- ✅ Installed Taminator v1.10.0
- ✅ Completed OOBE wizard
- ✅ Configured authentication
- ✅ Onboarded first customer
- ✅ Learned basic workflows

**Estimated Time Saved:** 2-3 hours per week per customer

**Next Milestone:** Automate weekly update workflow with cron

---

**Document Version:** 1.0  
**Last Updated:** October 25, 2025  
**Software Version:** Taminator 1.10.0  
**Status:** General Availability (GA)
