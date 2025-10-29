# Taminator v2.0 - Rocky Linux VM Test Plan

**Testing Environment**: Rocky Linux VM on Laptop  
**Date**: October 28, 2025  
**Goal**: Validate installation, OOBE, and workflows on clean system

---

## 🎯 Test Objectives

1. ✅ **Installation validation** - Does AppImage work on Rocky Linux?
2. ✅ **GETTING-STARTED accuracy** - Can user follow guide without help?
3. ✅ **OOBE wizard** - Does first-run experience work?
4. ✅ **Token management** - OS keyring integration on Rocky Linux
5. ✅ **rhcase integration** - Bundled rhcase works correctly
6. ✅ **Real workflows** - Check/Update/Post work end-to-end
7. ✅ **Error handling** - User-friendly errors with help links
8. ✅ **Documentation accuracy** - Troubleshooting guide correct

---

## 📋 Pre-Test Checklist

### VM Requirements
- [ ] Rocky Linux 8 or 9 installed
- [ ] Network connectivity
- [ ] Red Hat VPN configured (or can be configured)
- [ ] Desktop environment (GNOME/KDE)
- [ ] 2+ GB RAM available
- [ ] 1 GB disk space free

### Build Preparation
- [ ] Build AppImage on dev machine
- [ ] Transfer to VM (USB, scp, shared folder)
- [ ] Verify checksum (optional)

### Test Data Preparation
- [ ] JIRA API token ready (real or test)
- [ ] Customer account number (real or test)
- [ ] Portal group ID (if testing Post)

---

## 🚀 Phase 1: Installation Test (10 min)

### 1.1 Download/Transfer AppImage

**On dev machine (current)**:
```bash
cd /home/jbyrd/TAMINATOR

# Build AppImage (if not already built)
npm run build

# AppImage location:
ls -lh gui/dist/*.AppImage
```

**Transfer to VM**:
```bash
# Option A: SCP (if VM has SSH)
scp gui/dist/Taminator-2.0.0.AppImage user@rocky-vm:/home/user/

# Option B: USB drive
# Copy to USB, mount in VM

# Option C: Shared folder (if VM has guest additions)
# Copy to shared folder accessible from VM
```

### 1.2 Install on Rocky Linux VM

**On VM**:
```bash
# Download or copy AppImage to VM
cd ~

# Make executable
chmod +x Taminator-2.0.0.AppImage

# Test launch
./Taminator-2.0.0.AppImage
```

**Expected Result**:
- ✅ AppImage launches
- ✅ OOBE wizard appears
- ✅ No errors in console

**Failure Modes**:
- ❌ "Permission denied" → Check `chmod +x`
- ❌ "Cannot execute binary" → Check architecture (x64 vs ARM64)
- ❌ Missing libs → Check `ldd` output

**Test Log**:
```
[ ] AppImage executed successfully
[ ] No permission errors
[ ] GUI window opened
[ ] OOBE wizard displayed
```

---

## 🎓 Phase 2: OOBE Wizard Test (15 min)

**Follow GETTING-STARTED.md exactly** (pretend you're a new TAM).

### 2.1 Welcome Screen

**Expected**:
- Welcome message
- Feature overview
- "Get Started" button

**Test**:
```
[ ] Welcome screen displays
[ ] Text readable and professional
[ ] "Get Started" button works
```

### 2.2 Authentication Setup

**Expected**:
- Choice: OS Keyring vs Vault
- Clear explanation of each

**Test**:
```
[ ] OS Keyring option visible
[ ] Vault option visible
[ ] Select "OS Keyring"
[ ] "Continue" button enabled
```

**Rocky Linux Keyring**:
- GNOME: Secret Service (gnome-keyring)
- KDE: KWallet

**Verify keyring availability**:
```bash
# On VM
python3 -c "import keyring; print(keyring.get_keyring())"
```

### 2.3 Add JIRA Token

**Test Scenario**: Add real JIRA token

**Steps**:
1. Paste JIRA token
2. Click "Test Token"
3. Wait for validation

**Expected Result**:
- ✅ Green checkmark (if VPN connected)
- ❌ Red X with clear error (if VPN disconnected)

**Test**:
```
[ ] Token field accepts paste
[ ] "Test Token" button works
[ ] Success shows green checkmark
[ ] Error shows actionable message
[ ] "Continue" enabled after success
```

**Error Testing**:
```
Test A: Valid token + VPN → ✅ Success
Test B: Valid token + No VPN → ❌ "Check VPN" error
Test C: Invalid token + VPN → ❌ "Invalid token" error
```

### 2.4 Skip Portal Token

**Test**:
```
[ ] "Skip" button visible
[ ] "Skip" works without error
[ ] Wizard advances to next step
```

### 2.5 Onboard First Customer

**Test Scenario**: Onboard test customer

**Data**:
- Name: Test Customer
- Slug: test-customer
- Email: your.email@redhat.com
- Account: 1234567 (or real account)
- Product: Ansible

**Steps**:
1. Fill in form
2. Click "Onboard Customer"
3. Wait for JIRA query
4. Report generated

**Expected**:
```
[ ] Form accepts all fields
[ ] "Onboard" button enabled
[ ] Loading spinner shows
[ ] JIRA query succeeds (or fails gracefully)
[ ] Report file created: ~/taminator-test-data/test-customer.md
[ ] Success message displays
```

**Error Testing**:
```
Test A: Valid account + VPN → ✅ Report created
Test B: Invalid account + VPN → ❌ "No issues found" (graceful)
Test C: Valid account + No VPN → ❌ "Check VPN" error
```

### 2.6 Completion

**Test**:
```
[ ] Completion screen displays
[ ] "Finish" button works
[ ] Wizard closes
[ ] Main app loads
[ ] Dashboard shows test customer
```

---

## 📊 Phase 3: Dashboard Test (5 min)

### 3.1 Dashboard Display

**Expected**:
- Customer list
- JIRA statistics (if VPN connected)
- Status bar at bottom

**Test**:
```
[ ] Dashboard loads without errors
[ ] Test customer visible in list
[ ] JIRA stats show (or graceful degradation)
[ ] Status bar shows:
    [ ] Service: Healthy (green)
    [ ] AI: Setup Required (yellow) - expected
    [ ] Tokens: All OK (green)
    [ ] VPN: Connected (green) or Disconnected (yellow)
    [ ] Last Sync: timestamp
```

### 3.2 Refresh Test

**Test**:
```
[ ] Click "🔄 Refresh" button
[ ] Loading state shows
[ ] Dashboard updates
[ ] No errors
```

---

## 🔧 Phase 4: Core Workflows (20 min)

### 4.1 Check Workflow

**Test**: Compare report vs live JIRA

**Steps**:
1. Check tab → Select test-customer
2. Click "Compare Report vs. Live JIRA"
3. Review output

**Expected**:
```
[ ] Customer dropdown works
[ ] "Compare" button enabled
[ ] Loading state shows
[ ] Output displays in terminal area
[ ] Differences shown (or "No changes")
[ ] No errors
```

**Error Testing**:
```
Test A: VPN connected → ✅ Comparison succeeds
Test B: VPN disconnected → ❌ "Check VPN" toast
```

### 4.2 Update Workflow

**Test**: Update report from JIRA

**Steps**:
1. Update tab → Select test-customer
2. Click "Update from JIRA"
3. Review changes

**Expected**:
```
[ ] "Update" button works
[ ] Loading state shows
[ ] Report updated
[ ] Backup created (.backup file)
[ ] Success toast shows
[ ] No errors
```

**Verify backup**:
```bash
# On VM
ls ~/taminator-test-data/test-customer.md.backup
```

### 4.3 rhcase Workflow

**Test**: Execute rhcase command

**Steps**:
1. rhcase Bot tab
2. Enter command: `rhcase --version`
3. Execute

**Expected**:
```
[ ] Command input field works
[ ] "Execute" button works
[ ] Output shows rhcase version
[ ] No "command not found" errors
```

**Additional Tests**:
```bash
# Test 1: Version
rhcase --version

# Test 2: List (if have account number)
rhcase list 1234567

# Test 3: Help
rhcase --help
```

**Expected Results**:
```
[ ] rhcase bundled and executable
[ ] Version command works
[ ] Help command works
[ ] List command works (with VPN)
```

---

## 🐛 Phase 5: Error Handling Test (10 min)

### 5.1 VPN Disconnect Test

**Test Scenario**: Disconnect VPN mid-operation

**Steps**:
1. Disconnect Red Hat VPN
2. Try Check workflow
3. Observe error handling

**Expected**:
```
[ ] Status bar shows "VPN: Disconnected" (yellow)
[ ] Check operation fails gracefully
[ ] Toast shows: "🎫 Cannot connect to JIRA. Check VPN connection."
[ ] Help link: "Troubleshoot" → Opens troubleshoot modal
[ ] Retry button works
```

### 5.2 Invalid Token Test

**Test Scenario**: Corrupt JIRA token

**Steps**:
1. Settings → Authentication
2. Update JIRA token to "invalid"
3. Try Check workflow

**Expected**:
```
[ ] Status bar shows "Tokens: Missing" (yellow)
[ ] Check operation fails gracefully
[ ] Toast shows: "🔐 JIRA token expired or invalid"
[ ] Help link: "Update in Settings" → Opens settings
[ ] Clear error message, not cryptic
```

### 5.3 Service Crash Test

**Test Scenario**: Kill backend service

**Steps**:
```bash
# On VM, in terminal
pkill -9 -f "taminator.api.main"
```

**Expected**:
```
[ ] Service auto-restarts within 10 seconds
[ ] Status bar shows "Service: Offline" (red) temporarily
[ ] Status bar recovers to "Service: Healthy" (green)
[ ] Toast: "Service restarted" (or similar)
[ ] No manual intervention needed
```

---

## 📝 Phase 6: Documentation Validation (10 min)

### 6.1 GETTING-STARTED Accuracy

**Test**: Follow guide step-by-step

**Questions**:
```
[ ] Are installation instructions clear?
[ ] Are OOBE steps accurate?
[ ] Are screenshots needed anywhere?
[ ] Are any steps missing?
[ ] Are any steps incorrect?
```

**Document discrepancies** for later fix.

### 6.2 TROUBLESHOOTING Accuracy

**Test**: Simulate common issues, verify fixes

**Issues to Test**:
1. "Service Offline" → Follow troubleshooting steps
2. "VPN Not Connected" → Follow troubleshooting steps
3. "JIRA Token Invalid" → Follow troubleshooting steps

**Questions**:
```
[ ] Are troubleshooting steps correct?
[ ] Are solutions effective?
[ ] Are any common issues missing?
```

---

## 🔍 Phase 7: System Integration (5 min)

### 7.1 Desktop Integration

**Test**: Desktop launcher

**Optional** (follow README):
```bash
# Create desktop entry
cat > ~/.local/share/applications/taminator.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Taminator
Comment=Professional TAM Automation Tool
Exec=/home/user/Taminator-2.0.0.AppImage
Icon=taminator
Terminal=false
Categories=Development;Utility;
EOF

update-desktop-database ~/.local/share/applications/
```

**Test**:
```
[ ] Desktop entry created
[ ] Shows in app launcher
[ ] Icon displays (if available)
[ ] Launches from app menu
```

### 7.2 File Locations

**Verify** files created in correct locations:

```bash
# On VM
ls ~/.local/state/taminator/log/taminator.log  # Service logs
ls ~/taminator-test-data/test-customer.md      # Customer reports
ls ~/.config/taminator-gui/oobe-state.json     # OOBE state

# Check token in keyring
python3 -c "import keyring; print(keyring.get_password('taminator', 'jira-token'))"
```

**Expected**:
```
[ ] Service logs exist
[ ] Customer reports exist
[ ] OOBE state saved
[ ] Tokens in keyring (not plaintext)
```

---

## 📊 Test Results Template

### Summary
- **Platform**: Rocky Linux 8/9
- **Test Date**: [Date]
- **Tester**: [Name]
- **Duration**: [Time]
- **Pass/Fail**: [Overall Result]

### Phase Results

| Phase | Pass/Fail | Notes |
|-------|-----------|-------|
| 1. Installation | [ ] Pass [ ] Fail | |
| 2. OOBE Wizard | [ ] Pass [ ] Fail | |
| 3. Dashboard | [ ] Pass [ ] Fail | |
| 4. Workflows | [ ] Pass [ ] Fail | |
| 5. Error Handling | [ ] Pass [ ] Fail | |
| 6. Documentation | [ ] Pass [ ] Fail | |
| 7. System Integration | [ ] Pass [ ] Fail | |

### Issues Found

1. **[Issue Title]**
   - **Severity**: Critical / High / Medium / Low
   - **Description**: [What happened]
   - **Expected**: [What should happen]
   - **Steps to Reproduce**: [How to trigger]
   - **Workaround**: [Temporary fix, if any]

### Documentation Corrections Needed

- [ ] GETTING-STARTED: [Section] - [Issue]
- [ ] TROUBLESHOOTING: [Section] - [Issue]
- [ ] README: [Section] - [Issue]

### Overall Assessment

**Readiness for Alpha**:
- [ ] Ready to ship
- [ ] Minor fixes needed
- [ ] Major fixes needed

**Confidence Level**: [1-10]

**Recommendation**: [Ship / Fix issues first / Needs major work]

---

## 🎯 Success Criteria

**Alpha Release Ready if**:
- ✅ Installation works without errors
- ✅ OOBE wizard completes successfully
- ✅ At least one workflow (Check/Update) works
- ✅ Error messages are user-friendly
- ✅ Documentation is 90% accurate
- ✅ No critical bugs

**Acceptable Issues**:
- ⚠️ AI features not working (optional in alpha)
- ⚠️ Minor UI polish issues
- ⚠️ Performance not optimal
- ⚠️ Some advanced features not working

**Blocking Issues**:
- ❌ Cannot install/launch
- ❌ OOBE wizard crashes
- ❌ JIRA integration doesn't work
- ❌ Service doesn't auto-restart
- ❌ Critical security issue

---

## 📋 Post-Test Actions

### If Tests Pass
1. ✅ Document test results
2. ✅ Create alpha release notes
3. ✅ Build official AppImage
4. ✅ Distribute to friendly TAMs
5. ✅ Collect feedback

### If Tests Fail
1. ❌ Document all issues in GitLab
2. ❌ Prioritize fixes (Critical → High → Medium)
3. ❌ Fix issues
4. ❌ Re-test
5. ❌ Iterate until pass

---

**Ready to start testing on Rocky Linux VM!** 🚀

