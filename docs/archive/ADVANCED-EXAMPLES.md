# Taminator Advanced Examples

**Product:** Taminator v1.10.0  
**Document Type:** Real-World Usage Examples  
**Audience:** Experienced TAMs, Automation Engineers  
**Last Updated:** October 25, 2025

---

## Table of Contents

1. [Complete CLI Output Examples](#complete-cli-output-examples)
2. [Real-World Customer Scenarios](#real-world-customer-scenarios)
3. [Error Scenarios & Recovery](#error-scenarios--recovery)
4. [Automation Recipes](#automation-recipes)
5. [Edge Cases](#edge-cases)
6. [Troubleshooting Decision Trees](#troubleshooting-decision-trees)

---

## Complete CLI Output Examples

### Example 1: Dashboard Command (Full Output)

```bash
$ tam-rfe dashboard

┏━━━━━━━━━━━━━━━━━━━━━┓
┃  Customer Dashboard ┃
┗━━━━━━━━━━━━━━━━━━━━━┛

🔍 Loading customer data...
📡 Querying JIRA for live statistics...

┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━┳━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Customer           ┃ Account ┃ Product    ┃ RFEs ┃ Bugs ┃ Total ┃ Source   ┃ Last Modified    ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━╇━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ JPMorgan Chase     │ 334224  │ Ansible    │    8 │    4 │    12 │ 🟢 Live  │ 2025-10-25 09:30 │
│ ACME Inc           │ 540155  │ RHEL       │    3 │    1 │     4 │ 🟢 Live  │ 2025-10-25 09:31 │
│ Red Hat Internal   │ 540155  │ OpenShift  │    5 │    2 │     7 │ 🟢 Live  │ 2025-10-25 09:31 │
│ Legacy Customer    │ 123456  │ Satellite  │    0 │    0 │     0 │ 📄 Report│ 2025-10-20 14:00 │
└────────────────────┴─────────┴────────────┴──────┴──────┴───────┴──────────┴──────────────────┘

┏━━━━━━━━━━━━━┓
┃   Summary   ┃
┗━━━━━━━━━━━━━┛

  Total Customers: 4
  Open RFEs: 16
  Open Bugs: 7
  Total Issues: 23
  
  🟢 Live JIRA: 3 customers
  📄 Report fallback: 1 customer

✅ Dashboard loaded successfully
```

---

### Example 2: Check Command (With Status Changes)

```bash
$ tam-rfe check jpmc

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Checking Customer: JPMorgan Chase    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🔍 Checking JIRA for account 334224 (Ansible)...
📡 Endpoint: https://issues.redhat.com/rest/api/2/search
🔎 JQL Query:
   project in (AAP, AAPRFE) 
   AND "Red Hat Account" = 334224 
   AND "SBR Group" = "SBR Ansible" 
   AND status != Closed 
   AND status != Done

⏱️  Query executed in 2.3 seconds
✅ Found 12 open issues (8 RFEs, 4 Bugs)

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Comparison: Report vs Live JIRA      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

✅ 3 status changes detected

┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Issue Key   ┃ Summary                 ┃ Old Status  ┃ New     ┃ Support Case   ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ AAP-12345   │ RFE: Add workflow...    │ In Progress │ Post    │ 03891234       │
│ AAP-67890   │ BUG: API timeout...     │ Backlog     │ In Prog │ 03892345       │
│ AAP-11111   │ RFE: Custom fields...   │ New         │ Refine  │ (no case link) │
└─────────────┴─────────────────────────┴─────────────┴─────────┴────────────────┘

⚠️  Recommendation: Run 'tam-rfe update jpmc' to sync report

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Case Linkage Summary                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  Issues with case links: 10 / 12 (83%)
  Missing case links: 2
    - AAP-11111 (RFE)
    - AAP-99999 (Bug)

💡 Tip: Contact customer to link cases for better tracking
```

---

### Example 3: Update Command (Full Sync)

```bash
$ tam-rfe update jpmc --yes

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Updating Customer: JPMorgan Chase    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🔍 Step 1: Loading current report...
   📄 File: ~/taminator-test-data/jpmc.md
   ✅ Report loaded (Last updated: 2025-10-20 14:00)

🔍 Step 2: Querying live JIRA data...
   📡 Endpoint: https://issues.redhat.com/rest/api/2/search
   ⏱️  Query executed in 2.1 seconds
   ✅ Found 12 open issues

🔍 Step 3: Creating backup...
   💾 Backup: ~/taminator-test-data/jpmc.md.backup
   ✅ Backup created

🔍 Step 4: Updating report with live data...
   ✏️  Updating RFE section (8 issues)
   ✏️  Updating Bug section (4 issues)
   ✏️  Updating metadata (account, product, timestamp)
   ✅ Report updated

🔍 Step 5: Saving changes...
   💾 File: ~/taminator-test-data/jpmc.md
   ✅ Saved successfully

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Update Summary                       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  Status changes applied: 3
  New issues added: 0
  Closed issues removed: 1
  Total issues in report: 12
  
  Backup: ~/taminator-test-data/jpmc.md.backup
  Updated: 2025-10-25 10:45

✅ Report successfully synchronized with JIRA

💡 Next step: tam-rfe post jpmc (publish to Portal)
```

---

### Example 4: Post Command (Portal Publishing)

```bash
$ tam-rfe post jpmc

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Post to Customer Portal              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🔍 Step 1: Loading report...
   📄 File: ~/taminator-test-data/jpmc.md
   ✅ Report loaded (12 issues)

🔍 Step 2: Validating Portal token...
   🔑 Token source: ~/.config/taminator/tokens.json
   ✅ Token valid

🔍 Step 3: Preparing content...
   ✏️  Formatting markdown
   ✏️  Adding metadata
   ✅ Content prepared (2,340 characters)

Enter Customer Portal Group ID: 1234567

🔍 Step 4: Publishing to Portal...
   📡 Endpoint: https://api.access.redhat.com/rs/groups/1234567/discussions
   📤 Posting...
   ⏱️  Request completed in 1.8 seconds
   ✅ Post successful

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Publication Details                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  Customer: JPMorgan Chase
  Account: 334224
  Product: Ansible Automation Platform
  Issues: 12 (8 RFEs, 4 Bugs)
  
  Portal URL:
  https://access.redhat.com/groups/1234567/discussions/7891011
  
  Published: 2025-10-25 10:50

✅ Report successfully posted to Customer Portal

💡 Tip: Bookmark Portal URL for easy access
```

---

## Real-World Customer Scenarios

### Scenario 1: New Customer Onboarding (JPMorgan Chase)

**Context:** New TAM assignment, need to start tracking RFEs/Bugs for JPMorgan Chase.

**Step-by-Step:**

```bash
# Step 1: Gather customer information
# Account: 334224
# Product: Ansible Automation Platform
# TAM Email: jbyrd@redhat.com

# Step 2: Onboard customer
$ tam-rfe onboard jpmc \
  --email jbyrd@redhat.com \
  --display-name "JPMorgan Chase" \
  --account 334224 \
  --product Ansible \
  --non-interactive

🔍 Onboarding Customer: JPMorgan Chase
📋 Customer slug: jpmc
📧 TAM email: jbyrd@redhat.com
🏢 Account: 334224
📦 Product: Ansible Automation Platform

🔍 Querying JIRA for existing RFEs/Bugs...
📡 JQL: project in (AAP, AAPRFE) AND "Red Hat Account" = 334224...
✅ Found 12 open issues (8 RFEs, 4 Bugs)

🔍 Generating report template...
✏️  Creating: ~/taminator-test-data/jpmc.md
✅ Report created

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Onboarding Complete                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  Customer: JPMorgan Chase (jpmc)
  Account: 334224
  Product: Ansible
  Open RFEs: 8
  Open Bugs: 4
  
  Report: ~/taminator-test-data/jpmc.md

✅ Customer 'jpmc' onboarded successfully

💡 Next steps:
  1. Review report: cat ~/taminator-test-data/jpmc.md
  2. Check status: tam-rfe check jpmc
  3. Post to Portal: tam-rfe post jpmc

# Step 3: Review generated report
$ cat ~/taminator-test-data/jpmc.md | head -30

# RFE and Bug Report: JPMorgan Chase

**Account:** 334224  
**Product:** Ansible Automation Platform  
**TAM:** jbyrd@redhat.com  
**Last Updated:** 2025-10-25 10:00  

## Summary

- **Open RFEs:** 8
- **Open Bugs:** 4
- **Total Issues:** 12

## Open RFEs

### AAP-12345: Add workflow templates for CI/CD
**Status:** In Progress  
**Priority:** High  
**Support Case:** 03891234  
**Summary:** Customer requests pre-built workflow templates for common CI/CD patterns...

[... continues with all issues ...]

# Step 4: Post initial report to Portal
$ tam-rfe post jpmc
# (Interactive prompt for Group ID)
# Result: Published to Customer Portal
```

**Outcome:** Customer fully onboarded in < 5 minutes, initial report published to Portal.

---

### Scenario 2: Weekly Update Workflow (Multiple Customers)

**Context:** Friday afternoon, need to update all customer reports before end of week.

**Workflow:**

```bash
# Step 1: Check dashboard for all customers
$ tam-rfe dashboard

# Identified: 3 customers need updates (status changes detected)

# Step 2: Check each customer individually
$ tam-rfe check jpmc
✅ 3 status changes detected

$ tam-rfe check acme
✅ 1 status change detected

$ tam-rfe check redhat-internal
✅ No changes detected (skip update)

# Step 3: Update customers with changes
$ tam-rfe update jpmc --yes
✅ Report synchronized

$ tam-rfe update acme --yes
✅ Report synchronized

# Step 4: Post updates to Portal
$ tam-rfe post jpmc
✅ Posted to Portal

$ tam-rfe post acme
✅ Posted to Portal

# Step 5: Send summary email to customers
# (Manual step: reference Portal URLs from output)
```

**Time Saved:** 
- Manual process: ~2 hours
- Automated with Taminator: ~15 minutes
- **Savings: 1 hour 45 minutes**

---

### Scenario 3: Escalation - Critical Bug Status Change

**Context:** Critical bug for customer moved to "Post" status, need to notify immediately.

**Detection:**

```bash
$ tam-rfe check jpmc

⚠️  [BUG] AAP-55555: Critical authentication failure
    Status change: In Progress → Post
    Priority: Blocker
    Support Case: 03899999
    
🚨 CRITICAL: Blocker bug now in Post status!
```

**Action Steps:**

```bash
# 1. Update report immediately
$ tam-rfe update jpmc --yes

# 2. Extract bug details for email
$ grep -A 10 "AAP-55555" ~/taminator-test-data/jpmc.md

### AAP-55555: Critical authentication failure
**Status:** Post  
**Priority:** Blocker  
**Support Case:** 03899999  
**Summary:** Authentication fails for LDAP users after upgrade to AAP 2.5...
**Impact:** All LDAP users unable to log in (200+ users affected)
**Workaround:** Revert to AAP 2.4 or use local auth temporarily
**ETA:** Fix targeted for AAP 2.5.1 (next week)

# 3. Post urgent update to Portal
$ tam-rfe post jpmc

# 4. Send email to customer:
# Subject: [URGENT] AAP-55555 Status Update - Fix in Post
# Body: [Include details from report + Portal URL]
```

**Result:** Customer notified within 10 minutes of status change detection.

---

## Error Scenarios & Recovery

### Error 1: JIRA API Timeout

**Symptom:**
```bash
$ tam-rfe check jpmc

🔍 Checking JIRA for account 334224 (Ansible)...
📡 Endpoint: https://issues.redhat.com/rest/api/2/search

❌ Error: Connection timeout after 30 seconds
❌ JIRA query failed

Possible causes:
  1. VPN not connected
  2. JIRA API temporarily unavailable
  3. Network firewall blocking HTTPS (port 443)
```

**Recovery:**

```bash
# Check 1: Verify VPN connection
$ ping issues.redhat.com
PING issues.redhat.com (10.8.0.100): 56 data bytes
64 bytes from 10.8.0.100: icmp_seq=0 ttl=64 time=25.3 ms

# If ping fails: Reconnect VPN
$ sudo openvpn --config /etc/openvpn/redhat.ovpn

# Check 2: Increase timeout (if VPN is slow)
# Settings → Advanced → JIRA Timeout → 60 seconds

# Check 3: Retry with increased timeout
$ JIRA_TIMEOUT=60 tam-rfe check jpmc
✅ Query executed in 45.2 seconds
✅ Found 12 open issues
```

---

### Error 2: Invalid Account Number

**Symptom:**
```bash
$ tam-rfe onboard test --account INVALID --product Ansible

❌ Error: Invalid account number format
❌ Account numbers must be numeric (e.g., 334224)

Provided: INVALID
Expected format: 6-digit number
```

**Recovery:**

```bash
# Find correct account number:
# 1. Check Red Hat account database
# 2. Search Salesforce for customer
# 3. Ask customer success manager

# Retry with correct account
$ tam-rfe onboard test --account 334224 --product Ansible
✅ Customer onboarded successfully
```

---

### Error 3: Missing Portal Token

**Symptom:**
```bash
$ tam-rfe post jpmc

❌ Error: Portal API token not configured

To post to Customer Portal, you need a Portal API token.

Generate token at:
  https://access.redhat.com/management/api

Then add to Taminator:
  tam-rfe config --add-token
  (Select: Red Hat Customer Portal API Token)
```

**Recovery:**

```bash
# Step 1: Generate token at access.redhat.com/management/api
# Step 2: Add token to Taminator
$ tam-rfe config --add-token
Select token type:
  1. JIRA API Token
  2. Red Hat Customer Portal API Token

Enter choice [1-2]: 2

Enter token value: eyJhbGciOiJSUzI1NiIsIn...

💾 Saving token...
✅ Red Hat Customer Portal API Token saved

🧪 Testing token...
✅ Token valid

# Step 3: Retry post
$ tam-rfe post jpmc
✅ Posted to Portal
```

---

## Automation Recipes

### Recipe 1: Daily Dashboard Email

**Goal:** Email dashboard summary to team every morning.

**Script:** (`/usr/local/bin/tam-daily-report.sh`)

```bash
#!/bin/bash
# Taminator Daily Report Generator

DATE=$(date +"%Y-%m-%d")
REPORT_FILE="/tmp/tam-dashboard-$DATE.txt"
RECIPIENTS="tam-team@redhat.com"

# Generate dashboard
tam-rfe dashboard > "$REPORT_FILE"

# Email report
mail -s "TAM Dashboard - $DATE" "$RECIPIENTS" < "$REPORT_FILE"

# Cleanup
rm "$REPORT_FILE"
```

**Cron Entry:**
```cron
0 8 * * 1-5 /usr/local/bin/tam-daily-report.sh
```

---

### Recipe 2: Auto-Update on Status Changes

**Goal:** Automatically update reports when JIRA changes detected.

**Script:** (`/usr/local/bin/tam-auto-update.sh`)

```bash
#!/bin/bash
# Auto-update customer reports if changes detected

CUSTOMERS="jpmc acme redhat-internal"
CHANGED_CUSTOMERS=""

for customer in $CUSTOMERS; do
  # Check for changes
  tam-rfe check $customer --json > /tmp/check-$customer.json
  
  # Parse JSON for status_changes count
  changes=$(jq '.status_changes | length' /tmp/check-$customer.json)
  
  if [ "$changes" -gt 0 ]; then
    echo "Changes detected for $customer ($changes issues)"
    CHANGED_CUSTOMERS="$CHANGED_CUSTOMERS $customer"
    
    # Auto-update
    tam-rfe update $customer --yes --non-interactive
  fi
done

# Email summary if any changes
if [ -n "$CHANGED_CUSTOMERS" ]; then
  echo "Updated customers:$CHANGED_CUSTOMERS" | \
    mail -s "Taminator Auto-Update Summary" tam-team@redhat.com
fi
```

**Systemd Timer:** (Runs every 4 hours)
```ini
[Unit]
Description=Taminator Auto-Update Timer

[Timer]
OnCalendar=*-*-* 00/4:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

---

### Recipe 3: Weekly Portal Posting

**Goal:** Automatically post updates to Portal every Friday.

**Script:** (`/usr/local/bin/tam-weekly-post.sh`)

```bash
#!/bin/bash
# Weekly Portal posting for all customers

CUSTOMERS="jpmc acme redhat-internal"
PORTAL_GROUPS="1234567 2345678 3456789"  # Corresponding group IDs

# Arrays must match (customer → group ID)
customer_array=($CUSTOMERS)
group_array=($PORTAL_GROUPS)

for i in "${!customer_array[@]}"; do
  customer="${customer_array[$i]}"
  group="${group_array[$i]}"
  
  echo "Posting $customer to Portal group $group..."
  
  # Post (non-interactive with group ID in env var)
  PORTAL_GROUP_ID="$group" tam-rfe post $customer --yes --non-interactive
  
  if [ $? -eq 0 ]; then
    echo "✅ $customer posted successfully"
  else
    echo "❌ $customer post failed"
  fi
done
```

**Cron Entry:** (Every Friday at 4 PM)
```cron
0 16 * * 5 /usr/local/bin/tam-weekly-post.sh
```

---

## Edge Cases

### Edge Case 1: Customer with No Open Issues

**Scenario:** JIRA query returns 0 results (customer has no open RFEs/Bugs).

**Example:**

```bash
$ tam-rfe check legacy-customer

🔍 Checking JIRA for account 123456 (Satellite)...
✅ Query successful
ℹ️  Found 0 open issues

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  No Open Issues                       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  Customer: Legacy Customer
  Account: 123456
  Product: Satellite
  
  🎉 Great news! No open RFEs or Bugs for this customer.

💡 Tip: This could mean:
  - Customer satisfied with current product
  - Issues resolved recently
  - Customer not actively filing RFEs/Bugs

$ tam-rfe update legacy-customer --yes
ℹ️  Report updated (0 issues)
✅ Report synchronized
```

**Handling:** Taminator gracefully handles 0-issue scenarios, updating report with empty state.

---

### Edge Case 2: JIRA API Rate Limiting

**Scenario:** Too many API calls in short period, JIRA returns 429 (rate limit).

**Example:**

```bash
$ for c in customer-{1..50}; do tam-rfe check $c; done

# After ~20 iterations:
❌ Error: HTTP 429 - Too Many Requests
❌ JIRA API rate limit exceeded

Rate limit details:
  Limit: 20 requests per minute
  Reset: 45 seconds
  
⏱️  Retrying in 60 seconds...
```

**Mitigation:**

1. **Add delays between requests:**
```bash
for c in customer-{1..50}; do
  tam-rfe check $c
  sleep 5  # 5-second delay
done
```

2. **Use dashboard instead of individual checks:**
```bash
# Single API call for all customers
tam-rfe dashboard
```

3. **Implement exponential backoff** (future enhancement).

---

### Edge Case 3: Report File Corruption

**Scenario:** Customer report file corrupted or manually edited with invalid markdown.

**Example:**

```bash
$ tam-rfe update jpmc --yes

❌ Error: Failed to parse report file
❌ File: ~/taminator-test-data/jpmc.md

Parsing error at line 45:
  Expected: ## Open RFEs
  Found: ## Open RF[s (malformed heading)

Recovery options:
  1. Restore from backup: jpmc.md.backup
  2. Re-onboard customer (overwrites file)
  3. Manually fix markdown
```

**Recovery:**

```bash
# Option 1: Restore from backup
$ cp ~/taminator-test-data/jpmc.md.backup ~/taminator-test-data/jpmc.md
$ tam-rfe update jpmc --yes
✅ Report synchronized

# Option 2: Re-onboard (nuclear option)
$ mv ~/taminator-test-data/jpmc.md ~/taminator-test-data/jpmc.md.corrupt
$ tam-rfe onboard jpmc --account 334224 --product Ansible --email jbyrd@redhat.com --non-interactive
✅ Customer re-onboarded

# Option 3: Manual fix
$ vi ~/taminator-test-data/jpmc.md
# Fix line 45: ## Open RF[s → ## Open RFEs
$ tam-rfe update jpmc --yes
✅ Report synchronized
```

---

## Troubleshooting Decision Trees

### Decision Tree 1: "Command Not Found" Error

```
START: tam-rfe: command not found
│
├─ Is Taminator installed?
│  ├─ NO → Install: wget ... && chmod +x ...
│  └─ YES
│     │
│     ├─ Is /usr/local/bin in PATH?
│     │  ├─ NO → Add to PATH: export PATH=$PATH:/usr/local/bin
│     │  └─ YES
│     │     │
│     │     ├─ Does /usr/local/bin/tam-rfe exist?
│     │     │  ├─ NO → Create symlink: ln -s ... /usr/local/bin/tam-rfe
│     │     │  └─ YES
│     │     │     │
│     │     │     ├─ Is it executable?
│     │     │     │  ├─ NO → chmod +x /usr/local/bin/tam-rfe
│     │     │     │  └─ YES → Check for Python: which python3
│     │     │     │     │
│     │     │     │     ├─ Python not found → Install Python 3.9+
│     │     │     │     └─ Python found → Check shebang in script
│     │     │     │        │
│     │     │     │        └─ Fix shebang: #!/usr/bin/env python3
│     │     │     │
│     │     │     └─ RESOLVED: tam-rfe now works
```

---

### Decision Tree 2: "JIRA Token Not Configured" Error

```
START: ❌ JIRA token not configured
│
├─ Check environment variable
│  ├─ echo $JIRA_TOKEN_API_TOKEN
│  │  ├─ Empty → Set: export JIRA_TOKEN_API_TOKEN="..."
│  │  └─ Has value
│  │     │
│  │     ├─ Test token: tam-rfe config --test-tokens
│  │     │  ├─ Invalid → Regenerate at access.redhat.com/management/api
│  │     │  └─ Valid → Check file permissions
│  │     │     │
│  │     │     └─ ls -la ~/.config/taminator/tokens.json
│  │     │        ├─ File doesn't exist → tam-rfe config --add-token
│  │     │        ├─ Wrong permissions → chmod 600 tokens.json
│  │     │        └─ File corrupt → rm tokens.json && tam-rfe config --add-token
│  │     │
│  │     └─ RESOLVED: Token configured
│  │
│  └─ Check config file
│     ├─ cat ~/.config/taminator/tokens.json
│     │  ├─ File doesn't exist → tam-rfe config --add-token
│     │  ├─ Invalid JSON → rm tokens.json && tam-rfe config --add-token
│     │  └─ Missing jira-token key → tam-rfe config --add-token
│     │
│     └─ RESOLVED: Token configured
```

---

### Decision Tree 3: "Connection Timeout" Error

```
START: ❌ Connection timeout
│
├─ Check VPN
│  ├─ ping issues.redhat.com
│  │  ├─ Fails → Connect VPN: sudo openvpn --config ...
│  │  │  ├─ VPN connects → Retry command
│  │  │  └─ VPN fails → Check VPN config / contact IT
│  │  │
│  │  └─ Success
│  │     │
│  │     ├─ Check DNS
│  │     │  ├─ nslookup issues.redhat.com
│  │     │  │  ├─ Fails → Fix DNS: /etc/resolv.conf
│  │     │  │  └─ Success
│  │     │  │     │
│  │     │  │     ├─ Check firewall
│  │     │  │     │  ├─ telnet issues.redhat.com 443
│  │     │  │     │  │  ├─ Fails → Open port 443: sudo firewall-cmd ...
│  │     │  │     │  │  └─ Success
│  │     │  │     │  │     │
│  │     │  │     │  │     ├─ Increase timeout
│  │     │  │     │  │     │  └─ Settings → JIRA Timeout → 60s
│  │     │  │     │  │     │
│  │     │  │     │  │     └─ Check JIRA status
│  │     │  │     │  │        └─ https://status.redhat.com
│  │     │  │     │  │           ├─ Outage → Wait for resolution
│  │     │  │     │  │           └─ Operational → Contact support
│  │     │  │     │  │
│  │     │  │     │  └─ RESOLVED: Connection working
```

---

## Performance Optimization Examples

### Optimizing Dashboard Load Time

**Problem:** Dashboard takes 30+ seconds to load with 20 customers.

**Solution 1: Parallel JIRA Queries** (Future Enhancement)

```python
# Current: Sequential queries (slow)
for customer in customers:
    query_jira(customer)  # 2 seconds each = 40 seconds total

# Future: Parallel queries (fast)
import concurrent.futures

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(query_jira, c) for c in customers]
    results = [f.result() for f in futures]  # 8 seconds total (5 parallel batches)
```

**Solution 2: Caching** (Current Workaround)

```bash
# Cache dashboard results for 5 minutes
tam-rfe dashboard --json > /tmp/dashboard-cache.json

# Use cached results
cat /tmp/dashboard-cache.json | jq .

# Auto-refresh cache (cron every 5 minutes)
*/5 * * * * tam-rfe dashboard --json > /tmp/dashboard-cache.json
```

---

**Document Version:** 1.0  
**Last Updated:** October 25, 2025  
**Examples:** 20+ real-world scenarios  
**Status:** Complete

