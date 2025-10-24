# Taminator v1.10.0 - OOBE Implementation Handoff

## 🎯 Goal
Implement Out-of-Box Experience (OOBE) wizard for first-time Taminator users.

**Design Reference:** `taminator/FIRST-TIME-EXPERIENCE-DESIGN.md`

---

## ✅ Completed (40% Done)

### 1. Detection & State Management
**Files:**
- `taminator/gui/oobe-state.js` - OOBE state manager with persistence
- `taminator/gui/main.js` - IPC handlers for OOBE operations

**Capabilities:**
- ✅ First-run detection (checks for `.taminator-oobe-complete` file)
- ✅ State persistence across sessions
- ✅ Step completion tracking
- ✅ Factory reset capability

**IPC Handlers Added:**
```javascript
ipcMain.handle('oobe-is-first-run', ...)
ipcMain.handle('oobe-get-state', ...)
ipcMain.handle('oobe-complete-step', ...)
ipcMain.handle('oobe-mark-complete', ...)
ipcMain.handle('oobe-factory-reset', ...)
```

### 2. Welcome Screen (Screen 1)
**File:** `taminator/gui/oobe-wizard.html` (section: `#welcome-screen`)

**Features:**
- ✅ Taminator branding and value proposition
- ✅ Key features listed (auto-extraction, case context, customer onboarding)
- ✅ "Get Started" button navigates to authentication choice

### 3. Authentication Choice Screen (Screen 2)
**File:** `taminator/gui/oobe-wizard.html` (section: `#auth-choice-screen`)

**Features:**
- ✅ Two authentication paths presented:
  - **Recommended:** Vault integration (secure, automated)
  - **Alternative:** Manual token entry (quick setup)
- ✅ Clear pros/cons for each approach
- ✅ Navigation buttons route to appropriate setup flows

### 4. Entry Point Integration
**File:** `taminator/gui/index.html`

**Features:**
- ✅ DOMContentLoaded checks `oobe-is-first-run`
- ✅ Redirects to `oobe-wizard.html` if first run
- ✅ Normal app loads if OOBE complete

---

## 🔲 Remaining Work (60% Remaining)

### 5. Vault Setup Flow (Screen 3a) - **NEXT**
**Goal:** Guide user through Vault integration setup.

**Requirements:**
- Explain Vault benefits (security, automation, rotation)
- Button: "Open Vault Configuration"
- IPC call to `vault-setup` (opens external config)
- After Vault setup, test connection
- On success → Screen 4 (Test Configuration)

**File to Create/Modify:**
- Add `#vault-setup-screen` to `oobe-wizard.html`
- Add IPC call to trigger Vault setup process

### 6. Manual Token Setup Flow (Screen 3b)
**Goal:** Allow manual entry of SupportShell tokens.

**Requirements:**
- Form fields for API tokens:
  - Case API token
  - Customer API token
  - User API token
- "Test Connection" button
- Validation and error handling
- On success → Screen 4 (Test Configuration)

**File to Create/Modify:**
- Add `#manual-token-screen` to `oobe-wizard.html`
- Add form validation logic
- Add IPC handler for token storage

### 7. Test Configuration Screen (Screen 4)
**Goal:** Verify Taminator can connect to SupportShell.

**Requirements:**
- Show connection status indicator
- Test case search API
- Test customer data API
- Display connection results (success/failure)
- On success → Screen 5 (First Customer Onboarding)
- On failure → Back to Screen 2 or 3 to fix

**File to Create/Modify:**
- Add `#test-config-screen` to `oobe-wizard.html`
- Add IPC handlers for API testing

### 8. First Customer Onboarding Screen (Screen 5)
**Goal:** Walk user through onboarding their first customer.

**Requirements:**
- Customer search field (by name or account)
- Display search results
- "Onboard Customer" button
- Success confirmation
- "Finish Setup" button → Mark OOBE complete

**File to Create/Modify:**
- Add `#first-customer-screen` to `oobe-wizard.html`
- Integrate with existing customer onboarding logic

### 9. Factory Reset in Settings
**Goal:** Allow user to re-run OOBE wizard.

**Requirements:**
- Add "Factory Reset" button to Settings screen
- Confirmation dialog: "This will reset Taminator and restart the setup wizard"
- IPC call to `oobe-factory-reset`
- Restart app and show OOBE wizard

**File to Modify:**
- `taminator/gui/settings.html` - Add factory reset button
- Add confirmation dialog logic

### 10. End-to-End Testing
**Goal:** Verify complete OOBE flow works.

**Test Cases:**
- [ ] Fresh install shows OOBE wizard
- [ ] Vault setup path works end-to-end
- [ ] Manual token path works end-to-end
- [ ] Test configuration detects valid/invalid tokens
- [ ] First customer onboarding completes successfully
- [ ] OOBE completion prevents re-showing wizard
- [ ] Factory reset re-triggers OOBE wizard
- [ ] All navigation (back/next buttons) works
- [ ] State persists across app restarts mid-OOBE

---

## 📁 Key Files

### Existing (Modified)
- `taminator/gui/oobe-state.js` - State management ✅
- `taminator/gui/main.js` - IPC handlers ✅
- `taminator/gui/index.html` - Entry point check ✅
- `taminator/gui/oobe-wizard.html` - OOBE screens (partial) ✅

### To Create/Modify
- `taminator/gui/oobe-wizard.html` - Add screens 3a, 3b, 4, 5
- `taminator/gui/settings.html` - Add factory reset button
- `taminator/gui/oobe-wizard.js` - Add navigation and form logic (if needed)

---

## 🎨 Design Principles

1. **Progressive Disclosure:** Show only what's needed at each step
2. **Clear Value Prop:** Explain WHY each step matters
3. **Validation First:** Test configurations before proceeding
4. **Escape Hatches:** Allow skipping non-critical steps (if appropriate)
5. **Visual Feedback:** Show progress, loading states, success/error messages

---

## 🔗 Integration Points

### Vault Integration
- IPC call to trigger: `vault-setup` or similar
- Check Vault status: Use existing Vault detection logic
- Test Vault tokens: Call SupportShell API with Vault-provided tokens

### Manual Token Storage
- Store in: `~/.taminator/tokens.json` (encrypted)
- Format: Same as existing token storage mechanism
- Validate: Test API calls before saving

### Customer Onboarding
- Reuse: Existing customer search and onboarding logic
- IPC handlers: Likely already exist (`customer-search`, `customer-onboard`)

---

## 📊 Progress Tracker

| Component | Status | Completion |
|-----------|--------|------------|
| Detection & State | ✅ Complete | 100% |
| Welcome Screen | ✅ Complete | 100% |
| Auth Choice Screen | ✅ Complete | 100% |
| Vault Setup Flow | 🔲 Pending | 0% |
| Manual Token Flow | 🔲 Pending | 0% |
| Test Configuration | 🔲 Pending | 0% |
| First Customer Onboarding | 🔲 Pending | 0% |
| Factory Reset | 🔲 Pending | 0% |
| End-to-End Testing | 🔲 Pending | 0% |

**Overall:** 40% Complete

---

## 🚀 Next Steps (Priority Order)

1. **Vault Setup Flow (Screen 3a)** - Most TAMs will use this path
2. **Manual Token Flow (Screen 3b)** - Alternative for quick setup
3. **Test Configuration (Screen 4)** - Critical for validation
4. **First Customer Onboarding (Screen 5)** - Complete the OOBE journey
5. **Factory Reset (Settings)** - Support/testing tool
6. **End-to-End Testing** - Validate all paths work

---

## 📝 Notes

- **Version Target:** Taminator v1.10.0
- **Current Version:** v1.9.5 (shipped)
- **Design Doc:** `taminator/FIRST-TIME-EXPERIENCE-DESIGN.md`
- **State File Location:** `~/.taminator/.taminator-oobe-complete`
- **Test Mode:** Consider adding `--oobe` CLI flag to force OOBE wizard for testing

---

**Ready for next session.** Start with Screen 3a (Vault Setup Flow).

