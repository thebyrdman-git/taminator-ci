# Taminator JavaScript Bugs & Issues Tracker

## 🔴 Critical Bugs

### 1. ❌ Hardcoded Version Number in Error Dialog
**File**: `gui/public/js/error-dialog.js:261`  
**Issue**: Version is hardcoded as `'2.0.0'` instead of dynamically loaded from `package.json`

```javascript
const taminatorVersion = '2.0.0'; // TODO: Get from package.json
```

**Impact**: Bug reports show wrong version after updates  
**Priority**: Medium  
**Effort**: Low

**Solution**:
```javascript
// In main.js, pass version via IPC
ipcMain.handle('get-version', () => {
  const packageJson = require('./package.json');
  return packageJson.version;
});

// In error-dialog.js
const taminatorVersion = await window.ipcRenderer?.invoke('get-version') || '2.0.0';
```

---

### 2. ❌ Missing Token Configuration Modal
**File**: `gui/public/js/error-handler.js:226`  
**Issue**: TODO placeholder for showing modal to configure tokens

```javascript
_promptTokenSetup(tokenType) {
    // TODO: Show modal to configure token
    console.log(`Token setup needed for: ${tokenType}`);
```

**Impact**: Poor UX - users see toast but no direct way to fix  
**Priority**: High  
**Effort**: Medium

**Solution**:
Create proper modal that:
- Opens Settings tab automatically
- Focuses on token input field
- Shows instructions for getting token
- Pre-fills token type (JIRA/Portal)

---

## 🟡 Warnings & Improvements

### 3. ⚠️ Console Error Override May Hide Important Errors
**File**: `gui/public/js/error-dialog.js:363-390`  
**Issue**: Overriding `console.error` globally could hide or double-log errors

```javascript
// Override console.error to show dialog for critical errors
const originalConsoleError = console.error;
console.error = function(...args) {
  originalConsoleError.apply(console, args);
  
  // Shows dialog for every console.error
  if (firstArg instanceof Error || ...) {
    window.errorDialog.show({...});
  }
};
```

**Impact**: 
- Users may see error dialogs for non-critical errors
- Could create UI spam
- May interfere with debugging

**Priority**: Medium  
**Effort**: Low

**Solution**:
```javascript
// Only override in production mode
if (!process.env.DEV_MODE && !window.location.href.includes('--dev')) {
  console.error = function(...args) {
    originalConsoleError.apply(console, args);
    
    // Only show dialog for critical errors
    const isCritical = args.some(arg => 
      arg instanceof Error && !ignoredErrors.some(ignored => arg.message.includes(ignored))
    );
    
    if (isCritical) {
      window.errorDialog.show({...});
    }
  };
}
```

---

### 4. ⚠️ Unhandled Promise Rejection in Intelligence Client
**File**: `gui/public/js/intelligence-client.js:23-76`  
**Issue**: Async functions don't have proper error handling

```javascript
async analyzeEmail(emailText, tags = ['all']) {
  // ...
  const intelligence = await this.ipcRenderer.invoke('analyze-email', emailText, tags);
  // No try-catch - errors will be unhandled rejections
}
```

**Impact**: Errors bubble up as unhandled promise rejections  
**Priority**: Medium  
**Effort**: Low

**Solution**:
```javascript
async analyzeEmail(emailText, tags = ['all']) {
  try {
    if (!this.ipcRenderer) {
      throw new Error('IPC not available (browser mode)');
    }
    
    const intelligence = await this.ipcRenderer.invoke('analyze-email', emailText, tags);
    return intelligence;
    
  } catch (error) {
    console.error('[Intelligence Client] Analysis failed:', error);
    
    // Show user-friendly error
    if (window.errorHandler) {
      window.errorHandler.showError(
        'AI analysis failed',
        error.message,
        { text: 'Retry', action: () => this.analyzeEmail(emailText, tags) }
      );
    }
    
    throw error;
  }
}
```

---

### 5. ⚠️ Race Condition in Service Health Checks
**File**: `gui/main.js` (service manager integration)  
**Issue**: Multiple concurrent health checks can cause status flapping

**Observed in logs**:
```
[ServiceManager] Health check: healthy
[ServiceManager] Health check: unhealthy
[ServiceManager] Health check: healthy
```

**Impact**: Status bar flickers, confusing UX  
**Priority**: Low  
**Effort**: Low

**Solution**:
```javascript
// Debounce health checks
let healthCheckTimeout;
function scheduleHealthCheck() {
  clearTimeout(healthCheckTimeout);
  healthCheckTimeout = setTimeout(async () => {
    await checkServiceHealth();
  }, 1000); // Wait 1s before checking
}
```

---

### 6. ⚠️ Memory Leak: Toast Notifications Not Fully Cleaned
**File**: `gui/public/js/error-handler.js:317-332`  
**Issue**: `activeToasts` Map may not clear if DOM removal fails

```javascript
_removeToast(toastId) {
  const toast = this.activeToasts.get(toastId);
  if (!toast) return;
  
  // ... animation ...
  
  setTimeout(() => {
    if (toast.parentNode) {
      toast.parentNode.removeChild(toast);
    }
    this.activeToasts.delete(toastId);  // May not run if error above
  }, 300);
}
```

**Impact**: Long-running sessions accumulate dead toast references  
**Priority**: Low  
**Effort**: Low

**Solution**:
```javascript
_removeToast(toastId) {
  const toast = this.activeToasts.get(toastId);
  if (!toast) return;
  
  toast.classList.remove('toast-show');
  toast.classList.add('toast-hide');
  
  setTimeout(() => {
    try {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    } catch (error) {
      console.warn('[ErrorHandler] Failed to remove toast DOM:', error);
    } finally {
      // Always clean up Map entry
      this.activeToasts.delete(toastId);
    }
  }, 300);
}
```

---

### 7. ⚠️ Loading States Not Cleaned on Error
**File**: `gui/public/js/loading-states.js:22`  
**Issue**: Warning logged but loading spinner may stick if container missing

```javascript
if (!container) {
  console.warn(`[LoadingStates] Container not found: ${containerId}`);
  return; // Spinner never cleared!
}
```

**Impact**: Stuck spinners if DOM elements removed during loading  
**Priority**: Medium  
**Effort**: Low

**Solution**:
```javascript
hide(containerId) {
  const container = document.getElementById(containerId);
  if (!container) {
    console.warn(`[LoadingStates] Container not found: ${containerId}`);
    // Clean up tracking even if container missing
    this._activeSpinners.delete(containerId);
    return;
  }
  
  // ... existing code ...
}
```

---

## 🟢 Enhancements (Not Bugs)

### 8. 💡 Improve Error Context in API Client
**File**: `gui/public/js/api-client.js:64`  
**Issue**: Generic error logging, no request details

```javascript
console.error(`[API] ❌ ${endpoint} failed:`, error.message);
```

**Improvement**:
```javascript
console.error(`[API] ❌ ${method} ${endpoint} failed:`, {
  message: error.message,
  requestBody: body,
  timestamp: new Date().toISOString(),
  stack: error.stack
});
```

---

### 9. 💡 Add Retry Logic to Service Manager
**File**: `gui/service-manager.js:290`  
**Issue**: Service restart logged but no exponential backoff

**Improvement**:
Implement exponential backoff with jitter:
```javascript
const delay = Math.min(1000 * Math.pow(2, attempt) + Math.random() * 1000, 30000);
await new Promise(resolve => setTimeout(resolve, delay));
```

---

### 10. 💡 Add TypeScript Type Definitions
**Status**: No TypeScript, only vanilla JS  
**Issue**: No type safety, easy to make mistakes

**Improvement**:
Add JSDoc comments for IDE autocomplete:
```javascript
/**
 * @typedef {Object} ErrorDialogOptions
 * @property {string} title - Error title
 * @property {string} message - User-friendly message
 * @property {string} [technicalDetails] - Technical error details
 * @property {string} [stack] - Stack trace
 * @property {string} [context] - Additional context
 */

/**
 * Show error dialog
 * @param {ErrorDialogOptions} options - Error dialog options
 * @returns {void}
 */
show(options) {
  // ...
}
```

---

## 📋 Testing Checklist

Use `tam-dev` to test fixes:

```bash
# 1. Check code quality
tam-dev lint

# 2. Check service health
tam-dev health

# 3. Interactive debugging
tam-dev debug

# 4. Watch logs while testing
tam-dev logs
```

---

## 🎯 Priority Roadmap

### Phase 1: Critical Fixes (Week 1)
- [ ] #2: Implement token configuration modal ⚡
- [ ] #4: Add try-catch to all async intelligence functions
- [ ] #7: Fix loading states cleanup

### Phase 2: Quality Improvements (Week 2)
- [ ] #1: Dynamic version loading
- [ ] #3: Improve console.error override logic
- [ ] #6: Fix toast memory leak

### Phase 3: Enhancements (Week 3+)
- [ ] #5: Debounce health checks
- [ ] #8: Better API error context
- [ ] #9: Exponential backoff for retries
- [ ] #10: Add JSDoc type annotations

---

## 🔧 How to Fix These Bugs

### Using tam-dev Development Tools

1. **Start development environment**:
   ```bash
   cd /home/jbyrd/TAMINATOR
   tam-dev setup  # First time only
   ```

2. **Open interactive debugger** to test fixes:
   ```bash
   tam-dev debug
   ```

3. **Watch logs** while making changes:
   ```bash
   tam-dev logs
   ```

4. **Test each fix**:
   ```bash
   tam-dev health    # Check service
   tam-dev lint      # Check code quality
   tam-dev test      # Run tests (when available)
   ```

### Example: Fixing Bug #1 (Hardcoded Version)

```bash
# 1. Edit files
nano gui/main.js  # Add IPC handler
nano gui/public/js/error-dialog.js  # Update to use IPC

# 2. Test in debug mode
tam-dev debug
>>> # Test IPC handler
>>> window.ipcRenderer?.invoke('get-version')

# 3. Check for errors
tam-dev errors

# 4. Verify in GUI
# Trigger error dialog, check version number
```

---

## 📊 Bug Statistics

| Severity | Count |
|----------|-------|
| 🔴 Critical | 2 |
| 🟡 Warning | 5 |
| 🟢 Enhancement | 3 |
| **Total** | **10** |

| Effort | Count |
|--------|-------|
| Low | 8 |
| Medium | 2 |
| High | 0 |

**Estimated Total Effort**: 2-3 days

---

## 📝 Contributing

When fixing bugs:

1. **Create branch**: `git checkout -b fix/bug-<number>-<description>`
2. **Fix bug**: Make changes, test with `tam-dev`
3. **Test thoroughly**: Use all tam-dev workflows
4. **Lint code**: `tam-dev lint`
5. **Commit**: `git commit -m "Fix #<number>: <description>"`
6. **Push**: `git push origin fix/bug-<number>`
7. **Create MR**: Link to this tracker

---

**Last Updated**: 2025-11-01  
**Taminator Version**: 2.0.0  
**Status**: Active tracking


