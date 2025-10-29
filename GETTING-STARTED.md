# Getting Started with Taminator v2.0

**From zero to productive in 10 minutes**

---

## Prerequisites

Before you begin, ensure you have:

- ✅ **Red Hat VPN access** - Required for JIRA and Customer Portal APIs
- ✅ **Red Hat SSO account** - Your `@redhat.com` email
- ✅ **JIRA API token** - Generate at https://access.redhat.com/management/api
- ✅ **Customer account numbers** - For customers you want to track

---

## Step 1: Installation (2 minutes)

### Linux (Recommended: Container)

**Option A: One-Line Install (Easiest)**
```bash
# Install with systemd service (auto-starts on boot)
curl -fsSL https://raw.githubusercontent.com/thebyrdman-git/taminator-staging/main/deployment/install.sh | bash

# Access web interface
firefox http://localhost:8080
```

**Option B: Manual Container**
```bash
# Run with Podman/Docker
podman run -d \
  --name taminator-intelligence \
  --restart=unless-stopped \
  -v ~/.taminator:/root/.taminator \
  -p 8080:8080 \
  registry.gitlab.cee.redhat.com/jbyrd/taminator:v2.0.0

# Access at http://localhost:8080
```

**Option C: AppImage (Desktop App)**
```bash
# Download AppImage
wget https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v2.0.0/Taminator-2.0.0.AppImage

# Make executable
chmod +x Taminator-2.0.0.AppImage

# Run
./Taminator-2.0.0.AppImage
```

### macOS

```bash
# Download DMG (when available)
# Or use container method above
```

### Windows

```bash
# Download EXE installer (when available)
# Or use WSL2 + container method
```

---

## Step 2: First Launch - OOBE Wizard (3 minutes)

When you first launch Taminator, the **Out-of-Box Experience (OOBE) wizard** guides you through setup.

### OOBE Steps

#### 1. Welcome Screen
- Overview of Taminator features
- Architecture explanation (v2.0 improvements)
- Click **"Get Started"**

#### 2. Authentication Setup
**Choose your token management method**:

**Option A: OS Keyring** (Recommended for individual use)
- Tokens stored in system keyring (Secret Service, KWallet, Keychain)
- Most secure for single-user
- Select **"Use OS Keyring"** → **"Continue"**

**Option B: HashiCorp Vault** (Recommended for teams)
- Centralized token management
- Requires Vault server
- Enter Vault URL and token → **"Continue"**

#### 3. Add JIRA Token (Required)

**Get your JIRA token**:
1. Open https://access.redhat.com/management/api
2. Click **"Generate Token"** or **"Create Personal Access Token"**
3. Copy the token (looks like `MTE1NjQyMD...`)

**In Taminator**:
1. Paste token in **"JIRA API Token"** field
2. Click **"Test Token"** (verifies it works)
3. ✅ Green checkmark = success
4. Click **"Continue"**

**Troubleshooting**:
- ❌ "Connection failed" → Check VPN connection
- ❌ "Invalid token" → Regenerate at https://access.redhat.com/management/api
- ❌ "Timeout" → Verify `ping issues.redhat.com` works

#### 4. Add Portal Token (Optional)

**If you post reports to Customer Portal**:
1. Generate token at https://access.redhat.com/management/api
2. Paste in **"Portal API Token"** field
3. Click **"Test Token"**
4. Click **"Continue"**

**Skip if you don't need it**:
- Click **"Skip"** → You can add later in Settings

#### 5. Onboard First Customer (Optional)

**Add your first customer** (or skip and do later):

**Customer details**:
- **Name**: Display name (e.g., "JPMorgan Chase")
- **Slug**: Short ID (e.g., "jpmc") - lowercase, no spaces
- **Your Email**: Your `@redhat.com` email
- **Account Number**: Customer's Red Hat account number (required)
- **Product**: Primary product (e.g., "Ansible", "OpenShift", "RHEL")

**Click "Onboard Customer"** → Taminator will:
1. Query JIRA for RFEs and Bugs
2. Generate initial report
3. Save to `~/taminator-test-data/<slug>.md`

**Or click "Skip"** to add customers later.

#### 6. Completion
- ✅ Setup complete!
- Dashboard loads automatically
- You're ready to use Taminator

---

## Step 3: Using Taminator (5 minutes)

### Dashboard Tab

**What it shows**:
- All customers at a glance
- Live JIRA statistics (RFEs, Bugs, Total Issues)
- Service health status

**Actions**:
- Click **"🔄 Refresh"** → Update from JIRA
- Click customer row → Opens customer details

**Status Bar** (bottom of window):
- **Service**: Backend health (should be green)
- **AI**: LiteLLM models available (optional)
- **Tokens**: JIRA/Portal tokens configured
- **VPN**: Red Hat VPN connection status
- **Last Sync**: When data was last refreshed

### Customers Tab

**Manage customer accounts**:
- Click **"+ Add Customer"** → Onboard new customer
- Click **"Edit"** → Modify customer details
- Click **"Delete"** → Remove customer (keeps report file)

### Check Tab

**Compare saved report vs. live JIRA**:
1. Select customer from dropdown
2. Click **"Compare Report vs. Live JIRA"**
3. Review differences
4. If changes detected → Use **Update** tab to sync

### Update Tab

**Sync report with current JIRA status**:
1. Select customer
2. Click **"Update from JIRA"**
3. Report updated with latest JIRA data
4. Backup created automatically (`.backup` file)

### Post Tab

**Publish report to Customer Portal**:
1. Select customer
2. Click **"Preview"** → See what will be posted
3. Enter **Customer Portal Group ID**
   - Find in Customer Portal URL: `.../groups/<group-id>`
4. Click **"Post to Portal"**
5. ✅ Success message appears

**Prerequisites**:
- Portal token must be configured
- Red Hat VPN must be connected

### rhcase Bot Tab

**Interactive case analysis** (uses `rhcase` CLI):

**Commands**:
```bash
# List cases for account
rhcase list <account-number>

# Get case details
rhcase show <case-number>

# Search cases
rhcase search <keyword>
```

**Example**:
```bash
rhcase list 1234567 --months 1
```

**Output**: Terminal-style display of case data

### Settings Tab

**Configure Taminator**:

**Authentication**:
- Add/update JIRA token
- Add/update Portal token
- Test tokens

**Debug Logging**:
- Enable debug for specific features
- View log level per module
- Download diagnostic logs

**About**:
- Version information
- Service status
- API documentation link

---

## Common Workflows

### Workflow 1: Weekly RFE/Bug Report Update

**Before your weekly TAM call**:

```bash
# 1. Check for changes
tam-rfe check <customer-slug>

# 2. Update report (if changes detected)
tam-rfe update <customer-slug> --yes

# 3. Post to Portal
tam-rfe post <customer-slug>
```

**Or use GUI**:
1. Open Taminator
2. Check tab → Select customer → Compare
3. Update tab → Update from JIRA
4. Post tab → Preview → Post

**Time**: 5 minutes per customer (vs 30 minutes manual)

### Workflow 2: Onboarding New Customer

**When you get a new customer**:

```bash
tam-rfe onboard <customer-slug> \
  --email your.email@redhat.com \
  --display-name "Customer Name" \
  --account 1234567 \
  --product "Ansible"
```

**Or use GUI**:
1. Customers tab → **"+ Add Customer"**
2. Fill in details
3. Click **"Onboard"**
4. Report generated automatically

**Time**: 2 minutes (vs 45 minutes manual)

### Workflow 3: Case Analysis

**Before customer call**:

```bash
# In rhcase Bot tab:
rhcase list 1234567 --months 1

# Review recent cases
rhcase show 03742156

# Check case severity
rhcase list 1234567 --severity 1-2
```

**Time**: 3 minutes (vs 10 minutes in SupportShell)

---

## Pro Tips

### 1. Use Keyboard Shortcuts

- **Ctrl+R** / **Cmd+R** - Refresh dashboard
- **Ctrl+,** / **Cmd+,** - Open settings
- **Ctrl+Q** / **Cmd+Q** - Quit

### 2. Enable Debug Logging (when things go wrong)

**In Settings → Debug Logging**:
- Enable debug for `taminator.services.rhcase_service`
- Enable debug for `taminator.services.jira_service`
- Reproduce issue
- Download logs
- Attach to GitLab issue

### 3. Check Service Health

**Status Bar (bottom)**:
- 🟢 Green = Healthy
- 🟡 Yellow = Warning (partial functionality)
- 🔴 Red = Error (needs attention)

**Hover over status** → Tooltip shows details

### 4. Automate with Cron

**Daily dashboard check** (8 AM Monday-Friday):
```cron
0 8 * * 1-5 /home/$USER/Applications/Taminator-2.0.0.AppImage --cli dashboard --json > /tmp/taminator-daily.json
```

**Weekly update** (Friday 4 PM):
```cron
0 16 * * 5 /home/$USER/Applications/Taminator-2.0.0.AppImage --cli update --all --yes
```

---

## Troubleshooting

### Issue: "Service Offline"

**Cause**: Backend service crashed or starting up

**Solution**:
1. Wait 10 seconds (service auto-restarts)
2. Check logs: `~/.local/state/taminator/log/taminator.log`
3. If persists, restart Taminator

### Issue: "VPN Not Connected"

**Cause**: Red Hat VPN not active

**Solution**:
```bash
# Test VPN
ping issues.redhat.com

# If fails, connect to VPN
# Then refresh Taminator
```

### Issue: "JIRA Token Invalid"

**Cause**: Token expired or incorrect

**Solution**:
1. Regenerate at https://access.redhat.com/management/api
2. Settings → Authentication → Update JIRA Token
3. Test token

### Issue: "rhcase Command Not Found"

**Cause**: `rhcase` not bundled or not in PATH

**Solution**:
- v2.0 bundles `rhcase` automatically
- If missing, download from: https://gitlab.cee.redhat.com/gvaughn/hatter-pai
- Place in `~/.local/bin/rhcase`

### Issue: "Customer Not Found"

**Cause**: Customer not onboarded yet

**Solution**:
1. Customers tab → **"+ Add Customer"**
2. Fill in account number
3. Onboard

---

## Next Steps

### 1. Customize Your Setup

**Settings → Preferences**:
- Set default email
- Configure auto-update frequency
- Choose report format (Markdown/HTML/PDF)

### 2. Add More Customers

**Onboard all your customers**:
```bash
tam-rfe onboard customer1 --account 111111 --product Ansible
tam-rfe onboard customer2 --account 222222 --product OpenShift
tam-rfe onboard customer3 --account 333333 --product RHEL
```

**Or use GUI**: Customers tab → **"+ Add Customer"** (repeat)

### 3. Set Up Automation

**Weekly report automation**:
1. Create script: `~/bin/weekly-taminator-update.sh`
2. Add to crontab
3. Reports update automatically before TAM calls

### 4. Explore Advanced Features

- **API access**: http://127.0.0.1:8765/docs
- **CLI scripting**: `tam-rfe --help`
- **Debug logging**: Settings → Debug
- **Metrics**: Dashboard → Analytics (coming soon)

---

## Getting Help

### Documentation
- **README**: Overview and quick reference
- **TROUBLESHOOTING**: Common issues and solutions
- **API Docs**: http://127.0.0.1:8765/docs (when service running)

### Support
- **GitLab Issues**: https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
- **Email**: jbyrd@redhat.com
- **Slack**: *(channel TBD)*

### Report a Bug

**Collect diagnostics**:
```bash
# In Settings → Debug Logging
# Click "Download Diagnostics"
# Attach .tar.gz to GitLab issue
```

**Or manually**:
```bash
./tam-collect-logs
```

**Create issue**:
1. Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues/new
2. Describe problem
3. Attach diagnostics file
4. Tag with `bug` label

---

## FAQ

### Q: How do I update Taminator?

**A**: Download new AppImage from GitLab releases. Your configuration and data are preserved.

### Q: Where is my data stored?

**A**: 
- Tokens: OS keyring (secure)
- Customer reports: `~/taminator-test-data/`
- Logs: `~/.local/state/taminator/log/`
- Config: `~/.config/taminator/`

### Q: Can I use Taminator without VPN?

**A**: No. JIRA and Customer Portal APIs require Red Hat VPN.

### Q: Is my data secure?

**A**: Yes. Tokens in OS keyring, local-only API, no external services.

### Q: Can I customize reports?

**A**: Yes. Edit templates in `~/.config/taminator/templates/` (coming soon).

### Q: Does Taminator work on Windows?

**A**: Windows build coming soon. Use Linux VM for now.

### Q: Can I run multiple instances?

**A**: No. One instance per user (service runs on fixed port 8765).

---

## Success Checklist

After following this guide, you should be able to:

- ✅ Launch Taminator
- ✅ See dashboard with service status
- ✅ Have JIRA token configured (green checkmark)
- ✅ Onboard at least one customer
- ✅ Run a "Check" to compare report vs. JIRA
- ✅ Update a report from JIRA
- ✅ (Optional) Post a report to Customer Portal
- ✅ (Optional) Run `rhcase` commands

**If any of these failed**, see **Troubleshooting** section or contact jbyrd@redhat.com.

---

## You're Ready! 🎉

**Congratulations!** You've completed Taminator setup.

**What's next?**:
1. Add all your customers
2. Set up weekly automation
3. Share feedback in GitLab issues

**Enjoy saving 2+ hours per week!** ⏱️ → ☕

---

**Document Version**: 1.0  
**Last Updated**: October 28, 2025  
**Software Version**: Taminator 2.0.0  
**Status**: Alpha
