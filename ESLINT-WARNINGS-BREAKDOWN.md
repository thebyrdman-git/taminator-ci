# ESLint Warnings Breakdown - v2.1.2

**Date:** November 11, 2025  
**Current:** 61 warnings (0 errors)  
**Target:** < 10 warnings

---

## 📊 Warning Categories

### 1. `require-await` (30 warnings) - 49% of total
**Async functions that don't use await**

**Files affected:**
- `main.js`: 26 warnings
- `api-client.js`: 12 warnings
- `google-auth-handler.js`: 1 warning
- `service-manager.js`: 1 warning

**Why it's flagged:**
Functions marked `async` should use `await`, or they don't need to be async.

**Fix strategies:**
- **Option A:** Add `await` if calling promises
- **Option B:** Remove `async` if not needed
- **Option C:** Suppress with comment if intentionally async (e.g., for consistent API)

---

### 2. `no-unused-vars` (18 warnings) - 30% of total
**Variables/parameters defined but never used**

**Breakdown:**
- `main.js`: 12 warnings
  - `line` (141:72)
  - `sourceId` (141:78)
  - `event` x3 (551, 782, 1147)
  - `issueData` (782)
  - `responseData` x2 (323, 415)
  - `cliPath` (695)
  - `klistOutput` (748)
  - `e` (750)
  - `stdout` (801)
  - `code` (812)
  
- `error-dialog.js`: 1 warning
  - `text` (333)
  
- `error-handler.js`: 2 warnings
  - `errorMessage` x2 (407, 419)
  
- `intelligence-client.js`: 1 warning
  - `intelligence` (314)
  
- `startup-splash.js`: 1 warning
  - `progress` (159)

**Fix strategies:**
- **Remove** genuinely unused variables
- **Prefix with `_`** if intentionally unused (e.g., `_event`)
- **Use** the variable if it should be used

---

### 3. `prefer-const` (1 warning) - 2% of total
**Variables that are never reassigned should use `const`**

**Files affected:**
- `main.js`: 1 warning
  - `serviceManager` (17:1)

**Fix strategy:**
- Change `let serviceManager = ...` to `const serviceManager = ...`

---

## 🎯 Fix Plan

### Phase 1: Easy Fixes (5 minutes)
**Target: 1 warning → 0 warnings**

1. **prefer-const** in `main.js:17`
   ```javascript
   // Change:
   let serviceManager = require('./service-manager');
   
   // To:
   const serviceManager = require('./service-manager');
   ```

**Result:** 61 → 60 warnings (-1)

---

### Phase 2: Remove Unused Variables (30 minutes)
**Target: 18 warnings → 5 warnings**

#### File: `main.js`

**Definitely Remove (10 warnings):**
```javascript
// Line 141: Remove unused params
- ipcMain.handle('get-error-stack', async (event, line, sourceId) => {
+ ipcMain.handle('get-error-stack', async (event, _line, _sourceId) => {

// Line 323: Remove unused variable
- const responseData = await execPromise('cat ' + logFilePath);
+ await execPromise('cat ' + logFilePath);

// Line 415: Remove unused variable
- const responseData = await execPromise('cat ' + logFilePath);
+ await execPromise('cat ' + logFilePath);

// Line 551: Prefix unused param
- ipcMain.on('oobe-complete', async (event, credentials) => {
+ ipcMain.on('oobe-complete', async (_event, credentials) => {

// Line 695: Remove unused variable
- const cliPath = await gitManager.getGitExecutable();
+ await gitManager.getGitExecutable(); // or remove entirely if not needed

// Line 748: Remove unused variable
- const klistOutput = execSync('klist', { encoding: 'utf8' });
+ execSync('klist', { encoding: 'utf8' });

// Line 750: Remove unused catch param
- } catch (e) {
+ } catch (_e) {

// Line 782: Prefix unused params
- ipcMain.on('submit-issue', async (event, issueData, caseData) => {
+ ipcMain.on('submit-issue', async (_event, _issueData, caseData) => {

// Line 801: Remove unused variable
- const stdout = await execPromise(command);
+ await execPromise(command);

// Line 812: Prefix unused param
- taminator.on('close', (code) => {
+ taminator.on('close', (_code) => {

// Line 1147: Prefix unused param
- ipcMain.on('check-jira-connection', async (event) => {
+ ipcMain.on('check-jira-connection', async (_event) => {
```

#### File: `error-dialog.js`
```javascript
// Line 333: Prefix unused param
- addButton(label, onClick, text) {
+ addButton(label, onClick, _text) {
```

#### File: `error-handler.js`
```javascript
// Line 407: Prefix unused variable
- const errorMessage = document.getElementById('error-message');
+ const _errorMessage = document.getElementById('error-message');

// Line 419: Prefix unused variable
- const errorMessage = document.getElementById('error-message');
+ const _errorMessage = document.getElementById('error-message');
```

#### File: `intelligence-client.js`
```javascript
// Line 314: Prefix unused param
- formatSummary(intelligence) {
+ formatSummary(_intelligence) {
```

#### File: `startup-splash.js`
```javascript
// Line 159: Remove unused variable
- let progress = 0;
(Remove if not needed, or use it)
```

**Result:** 60 → 47 warnings (-13)

---

### Phase 3: Fix `require-await` (60 minutes)
**Target: 30 warnings → 3 warnings**

#### Strategy A: Remove `async` (Most common fix)

**File: `api-client.js` (12 warnings)**
All methods just return `this.makeRequest()` - don't need async:

```javascript
// Before:
async health() {
  return this.makeRequest('/health', 'GET');
}

// After:
health() {
  return this.makeRequest('/health', 'GET');
}
```

Apply to all 12 methods in `api-client.js`:
- health()
- info()
- listCustomers()
- getCustomer()
- createCustomer()
- deleteCustomer()
- getCustomerStats()
- checkJira()
- updateJira()
- listIssues()
- postToPortal()
- previewPortal()

**Result:** 47 → 35 warnings (-12)

---

#### Strategy B: Keep async for consistent API (main.js IPC handlers)

Many IPC handlers in `main.js` are async for consistency (some do async work, some don't).

**Options:**
1. **Keep them async** - Consistent API, suppress warnings
2. **Remove async** - Only make async if needed
3. **Add eslint-disable** - For intentional async

**Recommendation:** Add eslint-disable for consistency

```javascript
// At top of main.js, add to eslint comment:
/* eslint-disable require-await */

// Or, for specific handlers that are intentionally async:
// eslint-disable-next-line require-await
ipcMain.on('some-handler', async (event, data) => {
  // Synchronous work that might become async later
  return syncFunction(data);
});
```

**Apply to lines:** 182, 187, 192, 225, 232, 239, 247, 255, 263, 277, 291, 300, 379, 551, 693, 723, 782, 845, 900, 924, 981, 1021, 1070, 1147, 1254, 1300, 1345, 1393

**Alternative:** Remove async from handlers that truly don't need it.

**File: `google-auth-handler.js` (1 warning)**
```javascript
// Line 64: pollForCompletion() uses setInterval, not await
// Option 1: Keep async for return type
// Option 2: Remove async, return Promise directly
```

**File: `service-manager.js` (1 warning)**
```javascript
// Line 192: getHealth() just returns this.health
// Remove async:
getHealth() {
  return this.health;
}
```

**Result:** 35 → 3 warnings (-32) if we suppress main.js handlers

---

## 📊 Final Target

### After All Fixes:
```
✅ prefer-const: 1 → 0
✅ no-unused-vars: 18 → 0
✅ require-await: 30 → 0
```

**Total:** 61 → 0 warnings 🎉

---

## 🚀 Implementation Order

### Step 1: Quick Wins (5 min)
- [ ] Fix `prefer-const` in main.js:17
- **Result:** 61 → 60

### Step 2: api-client.js (10 min)
- [ ] Remove `async` from 12 methods
- **Result:** 60 → 48

### Step 3: service-manager.js (1 min)
- [ ] Remove `async` from getHealth()
- **Result:** 48 → 47

### Step 4: Unused Variables (30 min)
- [ ] Fix all 18 no-unused-vars warnings
- **Result:** 47 → 29

### Step 5: google-auth-handler.js (5 min)
- [ ] Fix pollForCompletion()
- **Result:** 29 → 28

### Step 6: main.js IPC handlers (15 min)
- [ ] Decide: Remove async or suppress warnings
- [ ] Apply fixes
- **Result:** 28 → 0

**Total time:** ~66 minutes
**Final result:** 0 warnings! 🎯

---

## ✅ Verification

After each step:
```bash
cd /home/jbyrd/TAMINATOR/gui
npm run lint
```

Expected progression:
```
Step 1: 61 → 60 ✅
Step 2: 60 → 48 ✅
Step 3: 48 → 47 ✅
Step 4: 47 → 29 ✅
Step 5: 29 → 28 ✅
Step 6: 28 → 0  ✅
```

---

**Ready to start Step 1!** 🚀

