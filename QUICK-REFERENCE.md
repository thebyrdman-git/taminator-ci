# Taminator Quick Reference Card

**Version:** 1.10.0 | **Cheat Sheet for TAMs** | **Print-Friendly Format**

---

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Download & Install
wget https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v1.10.0/Taminator-1.10.0-x86_64.AppImage
chmod +x Taminator-1.10.0-*.AppImage

# 2. Configure Token
tam-rfe config --add-token  # Add JIRA token

# 3. Onboard Customer
tam-rfe onboard jpmc --account 334224 --product Ansible --email you@redhat.com --display-name "JPMorgan Chase"

# 4. Check Status
tam-rfe check jpmc
```

---

## 📋 Essential Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `tam-rfe config` | Show configuration | `tam-rfe config` |
| `tam-rfe config --add-token` | Add API token | Interactive prompt |
| `tam-rfe dashboard` | View all customers | `tam-rfe dashboard` |
| `tam-rfe dashboard --json` | JSON output | For scripting |
| `tam-rfe check <slug>` | Compare vs JIRA | `tam-rfe check jpmc` |
| `tam-rfe update <slug>` | Sync with JIRA | `tam-rfe update jpmc --yes` |
| `tam-rfe post <slug>` | Post to Portal | `tam-rfe post jpmc` |
| `tam-rfe onboard <slug>` | Add customer | See onboarding section |
| `tam-rfe gui` | Launch GUI | Opens desktop app |

---

## 🆕 Customer Onboarding

### Full Command
```bash
tam-rfe onboard <customer-slug> \
  --email <your-email@redhat.com> \
  --display-name "Customer Name" \
  --account <account-number> \
  --product <product-name> \
  --non-interactive
```

### Example
```bash
tam-rfe onboard jpmc \
  --email jbyrd@redhat.com \
  --display-name "JPMorgan Chase" \
  --account 334224 \
  --product Ansible \
  --non-interactive
```

### Required Fields
- **Slug:** Lowercase identifier (no spaces)
- **Account:** Red Hat account number
- **Product:** Ansible, RHEL, OpenShift, Satellite

---

## 🔍 Weekly Workflow

```bash
# Monday Morning: Check all customers
tam-rfe dashboard

# Check specific customer for changes
tam-rfe check jpmc
tam-rfe check acme

# If changes detected: Update report
tam-rfe update jpmc --yes
tam-rfe update acme --yes

# Friday Afternoon: Post updates to Portal
tam-rfe post jpmc
tam-rfe post acme
```

---

## 🔐 Token Management

### Add Token (Interactive)
```bash
tam-rfe config --add-token
# Select: JIRA API Token
# Paste token from: https://access.redhat.com/management/api
```

### Add Token (Non-Interactive)
```bash
export JIRA_TOKEN_API_TOKEN="MTE1NjQyMD..."
export PORTAL_TOKEN_API_TOKEN="eyJhbGc..."
```

### Test Tokens
```bash
tam-rfe config --test-tokens
```

### Token Locations
1. **Environment variables** (checked first)
2. **Config file:** `~/.config/taminator/tokens.json` (chmod 600)

---

## 🎨 GUI Features

### Launch GUI
```bash
tam-rfe gui
# Or: Click Taminator icon in application launcher
```

### Main Tabs
| Tab | Purpose | Shortcut |
|-----|---------|----------|
| **Dashboard** | Customer overview | Home icon |
| **Check** | Compare report vs JIRA | - |
| **Update** | Sync report | - |
| **Post** | Publish to Portal | - |
| **Onboard** | Add customer | - |
| **Help** | Documentation | ? icon |
| **Settings** | Configuration | ⚙️ icon |

### Easter Eggs
- **Clippy:** Type `clippy` or press `Ctrl+Shift+C`
- **SkiFree:** Konami code: `↑↑↓↓←→←→BA`
- **XP Sounds:** Settings → Enable Windows XP Sounds

---

## 🚨 Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| **"JIRA token not configured"** | `tam-rfe config --add-token` |
| **"Connection timeout"** | Check VPN: `ping issues.redhat.com` |
| **"Account number required"** | Add `--account <number>` to onboard command |
| **"No customers found"** | Run `tam-rfe onboard` first |
| **OOBE won't appear** | Delete `~/.config/taminator-gui/oobe-state.json` |

---

## 📁 File Locations

| Path | Purpose |
|------|---------|
| `~/.config/taminator/tokens.json` | API tokens |
| `~/.config/taminator-gui/oobe-state.json` | OOBE state |
| `~/taminator-test-data/<slug>.md` | Customer reports |
| `~/taminator-test-data/<slug>.md.backup` | Auto-backups |

---

## 🔗 Product → SBR Mapping

| Product | SBR Group |
|---------|-----------|
| **Ansible** | SBR Ansible |
| **RHEL** | SBR RHEL |
| **OpenShift** | SBR OpenShift |
| **Satellite** | SBR Satellite |

---

## 📊 Dashboard Output Example

```
┏━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━┳━━━━━━┳━━━━━━━┓
┃ Customer     ┃ Account ┃ Product ┃ RFEs ┃ Bugs ┃ Total ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━╇━━━━━━╇━━━━━━━┩
│ JPMorgan     │ 334224  │ Ansible │    8 │    4 │    12 │
│ ACME Inc     │ 540155  │ RHEL    │    3 │    1 │     4 │
└──────────────┴─────────┴─────────┴──────┴──────┴───────┘
Summary: 2 customers, 11 RFEs, 5 Bugs, 16 total issues
```

---

## 🔄 Check Output Example

```bash
$ tam-rfe check jpmc

Checking JIRA for account 334224 (Ansible)...
Found 12 open RFEs and Bugs

✅ 3 status changes detected
⚠️  [RFE] AAP-12345: In Progress → Post
└─ Linked to case 03891234
⚠️  [BUG] AAP-67890: Backlog → In Progress
└─ Linked to case 03892345
⚠️  [RFE] AAP-11111: New → Refinement
└─ No linked case

Recommendation: Run 'tam-rfe update jpmc' to sync report
```

---

## ⚙️ Advanced Options

### Non-Interactive Mode
```bash
# For automation (cron, scripts)
tam-rfe update jpmc --yes --non-interactive
```

### JSON Output
```bash
# For parsing/scripting
tam-rfe dashboard --json | jq '.customers[0]'
```

### Dry Run
```bash
# Preview without making changes
tam-rfe post jpmc --dry-run
```

---

## 🤖 Automation Examples

### Daily Check (Cron)
```cron
# Check all customers every weekday at 8 AM
0 8 * * 1-5 /usr/local/bin/tam-rfe dashboard --json > /tmp/tam-daily.json
```

### Weekly Update (Cron)
```cron
# Update all reports Friday at 4 PM
0 16 * * 5 /usr/local/bin/tam-rfe update --all --yes
```

### Systemd Timer
```ini
[Unit]
Description=Taminator Daily Check

[Timer]
OnCalendar=Mon-Fri *-*-* 08:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

---

## 🌐 Required Network Access

| Endpoint | Port | Purpose |
|----------|------|---------|
| `issues.redhat.com` | 443 | JIRA queries |
| `api.access.redhat.com` | 443 | Portal API |

**VPN Required:** Red Hat VPN connection mandatory

---

## 🆘 Support

| Channel | Contact |
|---------|---------|
| **GitLab Issues** | https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues |
| **Slack** | `#tam-automation` |
| **Email** | jbyrd@redhat.com |

---

## 📚 Full Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Complete user guide |
| [GETTING-STARTED.md](GETTING-STARTED.md) | 15-minute setup |
| [INSTALLATION-GUIDE-V1.10.0.md](INSTALLATION-GUIDE-V1.10.0.md) | Detailed install |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Technical deep-dive |
| [GLOSSARY.md](GLOSSARY.md) | Terms and definitions |

---

## 🎓 Tips & Tricks

### Tip 1: Alias for Common Commands
```bash
# Add to ~/.bashrc
alias tam-dash='tam-rfe dashboard'
alias tam-check-all='for c in jpmc acme; do tam-rfe check $c; done'
```

### Tip 2: Quick Token Setup
```bash
# One-liner for token configuration
export JIRA_TOKEN_API_TOKEN=$(cat ~/jira-token.txt)
```

### Tip 3: Backup Customer Data
```bash
# Weekly backup
tar -czf taminator-backup-$(date +%F).tar.gz ~/.config/taminator/ ~/taminator-test-data/
```

### Tip 4: Switch Between CLI and GUI
```bash
# Working in CLI, need GUI?
tam-rfe gui

# Working in GUI, need CLI?
# Click "Switch to CLI" widget in OOBE
# Or open terminal and use tam-rfe commands
```

### Tip 5: Batch Operations
```bash
# Check all customers at once
for customer in jpmc acme redhat-internal; do
  echo "=== Checking $customer ==="
  tam-rfe check $customer
done
```

---

## 🎯 TAM Success Metrics

| Metric | Before Taminator | With Taminator | Savings |
|--------|------------------|----------------|---------|
| **Weekly RFE/Bug Check** | 2 hours | 15 minutes | 1.75 hrs |
| **Report Updates** | 1 hour | 5 minutes | 55 min |
| **Portal Posting** | 30 minutes | 2 minutes | 28 min |
| **Total Weekly** | 3.5 hours | 22 minutes | **3+ hours** |

---

## 📈 Version History

| Version | Release Date | Key Features |
|---------|--------------|--------------|
| **1.10.0** | Oct 25, 2025 | Live Dashboard, OOBE, CLI/GUI parity |
| **1.9.5** | Sep 2025 | Vault integration, ARM64 support |
| **1.9.0** | Aug 2025 | Initial GUI, CLI tools |

---

**Quick Reference Card v1.0** | **Taminator 1.10.0** | **Print This Page!** 📄

*"The Skynet TAMs Actually Want"* 🤖

