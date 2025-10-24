# 🧪 Taminator v1.10.0 Testing Guide

**Version:** 1.10.0  
**Tester:** Jimmy Byrd  
**Date:** October 24, 2025  
**Build:** `Taminator-1.10.0.AppImage`

---

## 🚀 How to Launch

### **Option 1: Quick Launch Script (Recommended)**
```bash
cd /home/jbyrd/TAMINATOR
./LAUNCH-v1.10.0.sh
```

### **Option 2: Direct Launch**
```bash
/home/jbyrd/TAMINATOR/gui/dist/Taminator-1.10.0.AppImage
```

### **Option 3: From Anywhere**
```bash
# You can run it from any directory:
cd ~
/home/jbyrd/TAMINATOR/gui/dist/Taminator-1.10.0.AppImage
```

**Note:** AppImage works from any location - no installation required!

---

## 📋 Testing Checklist

### ✅ **Test 1: First Launch - OOBE Wizard**

**What to test:** First-run experience

**Steps:**
1. Launch Taminator (if this is your first time)
2. **Expected:** OOBE wizard appears

**OOBE Screens to verify:**
- [ ] **Screen 1: Welcome** - Shows feature overview, has "Get Started" button
- [ ] **Screen 2: Authentication** - Choice between Vault and Manual setup
- [ ] **Screen 3a: Vault Setup** (if selected) - Vault URL and token fields
- [ ] **Screen 3b: Manual Setup** (if selected) - JIRA and Portal token fields
- [ ] **Screen 4: First Customer** (optional) - Customer discovery form
- [ ] **Screen 5: Completion** - Success message, "Launch Taminator" button

**Navigation:**
- [ ] "Back" button works on all screens
- [ ] "Next" button advances to next screen
- [ ] "Skip Setup" closes OOBE and shows main GUI
- [ ] Progress indicator shows current step (1/5, 2/5, etc.)

**Result:** ⬜ Pass / ⬜ Fail  
**Notes:**

---

### ✅ **Test 2: Theme System**

**What to test:** Theme switching and persistence

**Steps:**
1. Go to **Settings** tab (gear icon in sidebar)
2. Scroll down to **🎨 Theme Gallery**
3. You should see 7 theme cards with large icons

**Test each theme:**

#### Theme 1: **🏢 Professional** (Default)
- [ ] Click the Professional card
- [ ] Theme applies instantly
- [ ] Sidebar stays dark (#212427)
- [ ] Background is light gray (#F5F5F5)
- [ ] Red Hat colors (Red #EE0000, Blue #0066CC)
- [ ] ✓ checkmark appears on active card

#### Theme 2: **🌙 Dark Mode**
- [ ] Click Dark Mode card
- [ ] Background turns dark (#1E1E1E)
- [ ] Text turns light (#D4D4D4)
- [ ] Sidebar turns darker (#181818)
- [ ] Easy on the eyes

#### Theme 3: **🪟 Windows XP**
- [ ] Click Windows XP card
- [ ] Background turns beige (#ECE9D8)
- [ ] Sidebar turns blue (#245EDC)
- [ ] Font changes to smaller (11px)
- [ ] Looks nostalgic!

#### Theme 4: **🌊 Solarized Dark**
- [ ] Click Solarized Dark card
- [ ] Background turns dark blue (#002B36)
- [ ] Blue/teal accent colors
- [ ] Developer-friendly

#### Theme 5: **🧛 Dracula**
- [ ] Click Dracula card
- [ ] Background turns purple-dark (#282A36)
- [ ] Pink/cyan accent colors
- [ ] Looks like VSCode Dracula theme

#### Theme 6: **🏔️ Nord**
- [ ] Click Nord card
- [ ] Background turns dark blue-gray (#2E3440)
- [ ] Light blue accents
- [ ] Calm, Arctic aesthetic

#### Theme 7: **🟢 Matrix**
- [ ] Click Matrix card
- [ ] Background turns BLACK (#000000)
- [ ] Text turns GREEN (#00FF00)
- [ ] Terminal/hacker aesthetic
- [ ] Monospace font

**Theme Persistence:**
1. Select **Dark Mode** theme
2. Close Taminator (Ctrl+Q or close window)
3. Reopen Taminator
4. [ ] Dark Mode is still applied (persisted!)

**Result:** ⬜ Pass / ⬜ Fail  
**Notes:**

---

### ✅ **Test 3: Focus Mode**

**What to test:** Professional mode toggle

**Steps:**
1. Go to **Settings** tab
2. Find **🎯 Focus Mode** section (above Theme Gallery)
3. Note how many themes are visible (should be 7)

**Enable Focus Mode:**
1. [ ] Check the **"Enable Focus Mode"** checkbox
2. [ ] Alert appears: "Focus Mode Enabled"
3. [ ] Scroll to Theme Gallery
4. [ ] Only 5 themes visible (Windows XP and Matrix hidden!)
5. [ ] Warning message shows: "Focus Mode is ON"

**Theme Filtering:**
1. [ ] Windows XP card is GONE
2. [ ] Matrix card is GONE
3. [ ] Professional, Dark, Solarized, Dracula, Nord still visible

**Disable Focus Mode:**
1. [ ] Uncheck the checkbox
2. [ ] Alert appears: "Focus Mode Disabled"
3. [ ] Scroll to Theme Gallery
4. [ ] All 7 themes visible again!

**Focus Mode + Theme Conflict:**
1. Select **Windows XP** theme
2. Enable **Focus Mode**
3. [ ] Theme automatically switches to Professional
4. [ ] Alert confirms the switch

**Result:** ⬜ Pass / ⬜ Fail  
**Notes:**

---

### ✅ **Test 4: Portal Preview**

**What to test:** Report preview before posting

**Steps:**
1. Go to **Check** tab (or Update or Post tab)
2. Select any customer from dropdown (e.g., "acme-corp")
3. Click **🖼️ Preview Report** button

**Preview Modal:**
- [ ] Large modal appears (95% of screen)
- [ ] Split-screen view: markdown left, preview right
- [ ] Demo report content appears
- [ ] Close button (×) in top-right corner

**Left Side (Markdown Editor):**
- [ ] Header: "📝 Markdown Source"
- [ ] Textarea with markdown content
- [ ] Monospace font (Courier New)
- [ ] Editable (can type in it)

**Right Side (Portal Preview):**
- [ ] Header: "🖼️ Portal View"
- [ ] Preview inside iframe
- [ ] "Red Hat Customer Portal" header visible
- [ ] Report content rendered with Portal styling

**Live Editing:**
1. In the left markdown editor, change:
   - From: `# acme-corp RFE/Bug Tracker`
   - To: `# MY TEST REPORT`
2. [ ] Right side updates INSTANTLY (no delay!)
3. [ ] Change shows in Portal preview

**JIRA Links:**
1. Look at JIRA IDs in preview (e.g., AAPRFE-762)
2. [ ] They are blue and underlined (clickable links)
3. Click on one
4. [ ] Opens JIRA in new tab (https://issues.redhat.com/browse/AAPRFE-762)

**Case Links:**
1. Look at case numbers (e.g., 03666005)
2. [ ] They are blue and clickable
3. Click on one
4. [ ] Opens Red Hat Support case in new tab

**Desktop/Mobile Toggle:**
1. [ ] Click **📱 Mobile** button
2. [ ] Preview shrinks to mobile width (375px)
3. [ ] Click **💻 Desktop** button
4. [ ] Preview expands to desktop width (1200px)

**Close Preview:**
1. [ ] Click × button in top-right
2. [ ] Modal closes
3. [ ] Returns to Check/Update/Post tab

**Result:** ⬜ Pass / ⬜ Fail  
**Notes:**

---

### ✅ **Test 5: Check Button (CLI Integration)**

**What to test:** CLI output in GUI

**Steps:**
1. Go to **Check** tab
2. Select "acme-corp" from dropdown
3. Click **🔍 Compare Report vs. Live JIRA** button

**Expected Behavior:**
- [ ] Results section appears below
- [ ] Loading spinner shows briefly
- [ ] Terminal-style output appears (dark background, light text)
- [ ] Success or error indicator appears

**Terminal Output:**
- [ ] Background is dark (#1E1E1E)
- [ ] Text is light gray (#D4D4D4)
- [ ] Monospace font (Courier New)
- [ ] CLI output from `tam-rfe check` command

**Result Indicator:**
- [ ] Green box with "✅ Check Complete" OR
- [ ] Red box with "❌ Check Failed"

**Result:** ⬜ Pass / ⬜ Fail  
**Notes:**

---

### ✅ **Test 6: Update Button (CLI Integration)**

**What to test:** Update report from JIRA

**Steps:**
1. Go to **Update** tab
2. Select "acme-corp" from dropdown
3. Click **🔄 Update from JIRA** button

**Expected Behavior:**
- [ ] Results section appears
- [ ] Loading spinner + "Running tam-rfe update..." message
- [ ] May take 30-60 seconds (fetching from JIRA)
- [ ] Terminal output appears
- [ ] Success/error indicator

**Terminal Output:**
- [ ] Shows `tam-rfe update` output
- [ ] Shows backup creation message
- [ ] Shows JIRA updates fetched

**Result:** ⬜ Pass / ⬜ Fail  
**Notes:**

---

### ✅ **Test 7: Post Button (CLI Integration)**

**What to test:** Post to Portal (or show error)

**Steps:**
1. Go to **Post** tab
2. Select "acme-corp" from dropdown
3. Click **📤 Publish to Portal** button

**Expected Behavior (if Portal creds NOT set):**
- [ ] Terminal output appears
- [ ] Error message about missing credentials
- [ ] Instructions to set REDHAT_PORTAL_USERNAME and REDHAT_PORTAL_PASSWORD

**Expected Behavior (if Portal creds ARE set):**
- [ ] Prompts for Group ID
- [ ] Attempts to post
- [ ] Shows success or error in terminal output

**Result:** ⬜ Pass / ⬜ Fail  
**Notes:**

---

### ✅ **Test 8: Settings - General**

**What to test:** Settings page functionality

**Steps:**
1. Go to **Settings** tab
2. Verify all sections are visible:
   - [ ] General Settings
   - [ ] Report Settings
   - [ ] Advanced Settings
   - [ ] Focus Mode
   - [ ] Theme Gallery
   - [ ] Danger Zone

**General Settings:**
- [ ] Email field has default value (jbyrd@redhat.com)
- [ ] Auto-update checkbox works
- [ ] Notifications checkbox works

**Report Settings:**
- [ ] Report format dropdown works
- [ ] Timestamps checkbox works
- [ ] Changelog checkbox works

**Advanced Settings:**
- [ ] Reports directory field (read-only)
- [ ] Browse button visible
- [ ] JIRA timeout field (number input)
- [ ] Debug mode checkbox works

**Result:** ⬜ Pass / ⬜ Fail  
**Notes:**

---

### ✅ **Test 9: Factory Reset**

**What to test:** Reset to OOBE wizard

**Steps:**
1. Go to **Settings** tab
2. Scroll to **⚠️ Danger Zone** (red border)
3. Click **🔄 Factory Reset Taminator** button
4. [ ] Confirmation dialog appears with warning
5. Click "OK" to confirm

**Expected Behavior:**
- [ ] Success alert: "Factory reset complete!"
- [ ] App reloads automatically
- [ ] **OOBE wizard appears again!**
- [ ] All settings cleared
- [ ] Theme reset to Professional

**Verify Reset:**
1. After OOBE completes, go to Settings
2. [ ] Theme is Professional (default)
3. [ ] Focus Mode is OFF
4. [ ] All settings are defaults

**Result:** ⬜ Pass / ⬜ Fail  
**Notes:**

---

### ✅ **Test 10: Dashboard**

**What to test:** Home screen functionality

**Steps:**
1. Go to **Home** tab (first icon in sidebar)

**Verify Display:**
- [ ] Welcome message with user name
- [ ] "📊 Customers" card with demo data
- [ ] "🔐 Auth Status" card (shows auth check results)
- [ ] "📝 Recent Activity" card with demo data

**Auth Status:**
- [ ] Shows loading spinner initially
- [ ] Updates with real auth check results:
  - [ ] JIRA Token status
  - [ ] Portal Token status
  - [ ] VPN status
  - [ ] Kerberos status

**Buttons:**
- [ ] "Check All Reports" button (shows coming soon)
- [ ] "Run Auth Audit" button (refreshes auth status)
- [ ] "View Settings" button (navigates to Settings)

**Result:** ⬜ Pass / ⬜ Fail  
**Notes:**

---

### ✅ **Test 11: Sidebar Navigation**

**What to test:** Navigation between tabs

**Test each nav item:**
- [ ] 🏠 Home → Shows dashboard
- [ ] ✅ Check → Shows verify tab
- [ ] 🔄 Update → Shows update tab
- [ ] 📤 Post → Shows post tab
- [ ] ➕ Onboard → Shows onboard wizard
- [ ] 🔐 Auth → Shows authentication tab
- [ ] ⚙️ Settings → Shows settings page
- [ ] 📎 Clippy → Shows "In Development" message

**Active States:**
- [ ] Active nav item has red left border
- [ ] Active nav item has bold text
- [ ] Page title updates correctly

**Result:** ⬜ Pass / ⬜ Fail  
**Notes:**

---

### ✅ **Test 12: Responsive Behavior**

**What to test:** Window resizing

**Steps:**
1. Resize Taminator window to narrow width
2. [ ] Sidebar stays visible
3. [ ] Content area adjusts
4. [ ] Theme Gallery wraps to fewer columns
5. [ ] No horizontal scrolling (except in Portal Preview)

**Result:** ⬜ Pass / ⬜ Fail  
**Notes:**

---

### ✅ **Test 13: Cross-Theme Functionality**

**What to test:** All features work in all themes

**For EACH theme, verify:**
1. Select theme
2. [ ] Dashboard loads correctly
3. [ ] Check button works
4. [ ] Portal Preview opens and works
5. [ ] Settings page readable
6. [ ] All text is legible (good contrast)

**Critical Themes to Test:**
- [ ] **Professional** - Default, should be perfect
- [ ] **Dark Mode** - Check text contrast
- [ ] **Windows XP** - Check small font readability
- [ ] **Matrix** - Check green text on black is readable

**Result:** ⬜ Pass / ⬜ Fail  
**Notes:**

---

## 🐛 Bug Reporting Template

If you find a bug, record it here:

```
BUG #1
Title: [Short description]
Severity: Critical / High / Medium / Low
Theme: [Which theme was active?]
Steps to Reproduce:
1. 
2. 
3. 
Expected: [What should happen]
Actual: [What actually happened]
Screenshot: [If applicable]
```

---

## ✅ Test Summary

**Total Tests:** 13  
**Passed:** ___  
**Failed:** ___  
**Bugs Found:** ___  

**Overall Assessment:**
⬜ Ready for production  
⬜ Needs minor fixes  
⬜ Needs major fixes  

**Tester Signature:** _______________  
**Date:** _______________  

---

## 🎯 Priority Testing Order

If short on time, test in this order:

1. **OOBE Wizard** - First impressions matter
2. **Theme System** - Core new feature
3. **Portal Preview** - Major productivity feature
4. **Focus Mode** - Professionalism feature
5. **Check/Update buttons** - Core functionality
6. **Factory Reset** - Verify OOBE can restart

---

## 💡 Notes for Tester

### What's Working vs. What's Demo Data

**Working (Real):**
- ✅ Theme switching
- ✅ Focus Mode toggle
- ✅ Portal Preview (with demo report)
- ✅ CLI command execution (Check, Update, Post)
- ✅ OOBE wizard
- ✅ Factory Reset
- ✅ Settings persistence

**Demo/Placeholder Data:**
- 📋 Dashboard customer list (fake data)
- 📋 Recent Activity (fake data)
- 📋 Portal Preview report (demo content)

**Not Yet Implemented:**
- 📎 Clippy tab (shows "In Development")
- 🎮 Easter eggs (not built yet)

### Known Limitations

1. **Portal Posting** requires environment variables:
   ```bash
   export REDHAT_PORTAL_USERNAME='your_username'
   export REDHAT_PORTAL_PASSWORD='your_password'
   ```

2. **RPM package** didn't build (but AppImage and .deb did)

3. **Customer list** is hardcoded demo data (testcustomer, acme-corp, etc.)

---

## 🎉 Happy Testing!

**Remember:** This is v1.10.0 - a MASSIVE release with:
- ~2,050 lines of new code
- 8 major features
- 7 complete themes
- ~10 hours of development

**Enjoy exploring all the new features!** 🚀


