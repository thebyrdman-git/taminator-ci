# Quick Fix Guide - Taminator JavaScript Bugs

## 🚀 Getting Started

```bash
cd /home/jbyrd/TAMINATOR

# Launch development tools
tam-dev

# Or use full playbook
ansible-playbook ansible/playbooks/taminator-dev.yml
```

## 🐛 Top 3 Bugs to Fix First

### Bug #1: Token Configuration Modal (HIGH PRIORITY)

**Location**: `gui/public/js/error-handler.js:226`

**Current Code** (broken):
```javascript
_promptTokenSetup(tokenType) {
    // TODO: Show modal to configure token
    console.log(`Token setup needed for: ${tokenType}`);
```

**Fixed Code**:
```javascript
_promptTokenSetup(tokenType) {
    // Open settings and focus on token section
    this._openSettings(tokenType.toLowerCase());
    
    // Show helpful modal
    const modal = document.createElement('div');
    modal.className = 'token-setup-modal-overlay';
    modal.innerHTML = `
        <div class="token-setup-modal">
            <div class="modal-header">
                <h3>🔐 ${tokenType} Token Required</h3>
                <button class="modal-close">×</button>
            </div>
            <div class="modal-content">
                <p>To use ${tokenType} features, you need to configure your API token.</p>
                
                <h4>Steps:</h4>
                <ol>
                    <li>Visit <a href="https://access.redhat.com/management/api" target="_blank">
                        Red Hat API Management</a></li>
                    <li>Click "Generate Token"</li>
                    <li>Copy the token</li>
                    <li>Paste it in Settings → Authentication</li>
                </ol>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" onclick="this.closest('.token-setup-modal-overlay').remove()">
                    Later
                </button>
                <button class="btn btn-primary" onclick="this.closest('.token-setup-modal-overlay').remove(); 
                    window.open('https://access.redhat.com/management/api', '_blank')">
                    Get Token
                </button>
            </div>
        </div>
    `;
    
    modal.querySelector('.modal-close').onclick = () => modal.remove();
    modal.onclick = (e) => { if (e.target === modal) modal.remove(); };
    
    document.body.appendChild(modal);
}
```

**Test**:
```bash
# 1. Watch logs
tam-dev logs

# 2. In another terminal, test the fix
tam-dev debug

# In IPython:
>>> # Trigger the function
>>> # Check modal appears correctly
```

---

### Bug #2: Async Error Handling in Intelligence Client (CRITICAL)

**Location**: `gui/public/js/intelligence-client.js:23-76`

**Files to update**:
- `analyzeEmail()`
- `getCaseHistory()`
- `recordFeedback()`
- `getStatistics()`

**Pattern to apply to ALL async functions**:

```javascript
// BEFORE (broken):
async analyzeEmail(emailText, tags = ['all']) {
  const intelligence = await this.ipcRenderer.invoke('analyze-email', emailText, tags);
  return intelligence;
}

// AFTER (fixed):
async analyzeEmail(emailText, tags = ['all']) {
  try {
    if (!this.ipcRenderer) {
      throw new Error('IPC not available - running in browser mode');
    }
    
    const intelligence = await this.ipcRenderer.invoke('analyze-email', emailText, tags);
    return intelligence;
    
  } catch (error) {
    console.error('[Intelligence Client] Email analysis failed:', error);
    
    // Show user-friendly error with retry
    if (window.errorHandler) {
      window.errorHandler.showError(
        'AI analysis failed',
        error.message,
        null,
        () => this.analyzeEmail(emailText, tags)
      );
    }
    
    // Re-throw so caller can handle
    throw error;
  }
}
```

**Apply this pattern to**:
1. `analyzeEmail()` ✓
2. `getCaseHistory()` ✓
3. `recordFeedback()` ✓
4. `getStatistics()` ✓

**Test each function**:
```bash
tam-dev debug

# Test with invalid input
>>> intelligenceClient.analyzeEmail("test", ["invalid"])
# Should show error toast, not crash
```

---

### Bug #3: Memory Leak in Toast Cleanup (MEDIUM PRIORITY)

**Location**: `gui/public/js/error-handler.js:317-332`

**Current Code** (leak):
```javascript
_removeToast(toastId) {
  const toast = this.activeToasts.get(toastId);
  if (!toast) return;
  
  toast.classList.remove('toast-show');
  toast.classList.add('toast-hide');
  
  setTimeout(() => {
    if (toast.parentNode) {
      toast.parentNode.removeChild(toast);  // May throw
    }
    this.activeToasts.delete(toastId);  // Never runs if error above!
  }, 300);
}
```

**Fixed Code**:
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
      console.warn('[ErrorHandler] Failed to remove toast from DOM:', error);
    } finally {
      // ALWAYS clean up Map entry, even if DOM removal failed
      this.activeToasts.delete(toastId);
    }
  }, 300);
}
```

**Test**:
```bash
tam-dev debug

# Create many toasts
>>> for (let i = 0; i < 50; i++) {
...   window.errorHandler.showSuccess('Test ' + i);
... }

# Check memory
>>> window.errorHandler.activeToasts.size
# Should be 0 after toasts dismiss
```

---

## 🔧 Development Workflow

### Step 1: Setup Environment

```bash
# First time setup
tam-dev setup

# Installs:
# - pytest, black, flake8
# - ipython, ipdb
# - Development dependencies
```

### Step 2: Make Changes

```bash
# Edit JavaScript files
nano gui/public/js/error-handler.js

# Format code
cd /home/jbyrd/TAMINATOR/gui
npx prettier --write public/js/*.js
```

### Step 3: Test Changes

```bash
# Check service health
tam-dev health

# Interactive testing
tam-dev debug

# Watch logs while testing
tam-dev logs

# Check for errors
tam-dev errors
```

### Step 4: Validate

```bash
# Lint JavaScript (if eslint configured)
cd gui
npm run lint

# Or use generic linter
tam-dev lint
```

### Step 5: Test in GUI

```bash
# Run Taminator
./gui/dist/linux-unpacked/taminator

# Or from source
cd gui
npm start
```

---

## 📋 Complete Fix Checklist

### Phase 1: Critical Fixes
- [ ] **Bug #2**: Add try-catch to all 4 async intelligence functions
  - [ ] `analyzeEmail()`
  - [ ] `getCaseHistory()`
  - [ ] `recordFeedback()`
  - [ ] `getStatistics()`
- [ ] **Bug #1**: Implement token configuration modal
- [ ] **Bug #3**: Fix toast memory leak
- [ ] **Bug #7**: Fix loading states cleanup

### Phase 2: Quality Improvements
- [ ] **Bug #4**: Improve console.error override
- [ ] **Bug #5**: Dynamic version loading
- [ ] **Bug #6**: Debounce health checks

### Phase 3: Enhancements
- [ ] **Bug #8**: Better API error context
- [ ] **Bug #9**: Exponential backoff
- [ ] **Bug #10**: Add JSDoc annotations

---

## 🧪 Testing Each Fix

### Test Template

```bash
# 1. Start fresh
tam-dev health

# 2. Clear cache
tam-dev
# Select: 11 (Clear Cache)

# 3. Watch logs
tam-dev logs

# 4. Test the fix
# (Interact with GUI or use debug console)

# 5. Check for errors
tam-dev errors

# 6. Verify fix works
# (No errors, feature works as expected)
```

---

## 💡 Pro Tips

### Tip 1: Use Browser DevTools

For Electron GUI debugging:
```bash
# Enable DevTools in development
export ELECTRON_ENABLE_LOGGING=1
npm start

# Press F12 to open DevTools
```

### Tip 2: Test Error Scenarios

```bash
tam-dev debug

# Simulate errors
>>> window.errorHandler.showError('Test error', 'Details', null, () => console.log('Retry!'))

>>> intelligenceClient.analyzeEmail(null)  # Should handle gracefully

>>> # Disconnect VPN and test network errors
```

### Tip 3: Monitor Memory

```bash
tam-dev debug

# Check active toasts
>>> window.errorHandler.activeToasts.size

# Check service manager state
>>> # (if accessible via window object)
```

### Tip 4: Use Git Branches

```bash
# Create branch for each bug
git checkout -b fix/bug-2-async-error-handling

# Make changes, test, commit
git add gui/public/js/intelligence-client.js
git commit -m "Fix #2: Add try-catch to all async intelligence functions"

# Push for review
git push origin fix/bug-2-async-error-handling
```

---

## 📊 Estimated Time

| Bug | Complexity | Time |
|-----|-----------|------|
| #2 Async errors | Low | 30 min |
| #1 Token modal | Medium | 1 hour |
| #3 Memory leak | Low | 15 min |
| #7 Loading cleanup | Low | 15 min |
| **Phase 1 Total** | | **2 hours** |

---

## 🎯 Success Criteria

### Bug #2 (Async) Fixed When:
- ✅ No unhandled promise rejections in console
- ✅ Error toasts show for failed operations
- ✅ Retry button works
- ✅ App doesn't crash on AI failures

### Bug #1 (Modal) Fixed When:
- ✅ Modal shows when token missing
- ✅ "Get Token" button opens Red Hat API page
- ✅ Settings page opens with token field focused
- ✅ User can dismiss modal

### Bug #3 (Memory) Fixed When:
- ✅ `activeToasts.size` returns to 0 after toasts dismiss
- ✅ Memory doesn't grow after 100+ toasts
- ✅ No console warnings about failed DOM removal

---

## 🆘 Getting Help

If stuck:

```bash
# View recent errors
tam-dev errors

# Check service status
tam-dev health

# Test specific features
tam-dev jira      # Test JIRA
tam-dev ai        # Test AI

# Full debug
tam-dev debug
```

**Need more help?**
- See `JAVASCRIPT-BUGS-TRACKER.md` for detailed bug info
- See `DEBUGGING-WITH-ANSAI-TOOLS.md` for debugging guide
- Ask in Taminator GitLab issues

---

**Last Updated**: 2025-11-01  
**Target**: Fix Phase 1 (2 hours of work)  
**Status**: Ready to implement





