# Error Handling Patterns for TAMINATOR

**Best practices for error handling in JavaScript/Electron**

---

## 🎯 Core Principles

1. **Always catch errors** - No unhandled rejections
2. **User-friendly messages** - Show what happened and what to do
3. **Log for debugging** - `console.error` with context
4. **Clean up resources** - Use `finally` blocks
5. **Fail gracefully** - Don't crash the app

---

## 📋 Pattern Catalog

### Pattern 1: Async Function with User Feedback

**Use when:** Any async operation that affects the UI

```javascript
async function fetchData() {
  try {
    const result = await apiCall();
    return result;
  } catch (error) {
    console.error('[ModuleName] Operation failed:', error);
    
    // Show user-friendly error
    if (window.errorHandler) {
      window.errorHandler.showError(
        'Failed to load data',
        error.message,
        'https://docs.link',
        () => fetchData() // Retry callback
      );
    }
    
    // Re-throw if caller needs to handle it
    throw error;
  }
}
```

**Key points:**
- ✅ Log with module prefix
- ✅ Show user-friendly message
- ✅ Provide help link
- ✅ Offer retry option
- ✅ Re-throw for caller

---

### Pattern 2: Cleanup with Finally

**Use when:** Resources need cleanup (timers, listeners, connections)

```javascript
async function operationWithCleanup() {
  const timer = setTimeout(() => {}, 5000);
  
  try {
    const result = await doWork();
    return result;
  } catch (error) {
    console.error('[Module] Error:', error);
    throw error;
  } finally {
    // ALWAYS clean up, even on error
    clearTimeout(timer);
    removeEventListeners();
    closeConnections();
  }
}
```

**Key points:**
- ✅ `finally` runs on success AND error
- ✅ Clear timeouts
- ✅ Remove listeners
- ✅ Close connections

---

### Pattern 3: Promise Executor (Correct)

**Use when:** Creating custom promises

```javascript
// ✅ CORRECT: No return in executor
new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve('done');
  }, 1000);
});

// ❌ WRONG: Don't return in executor
new Promise((resolve, reject) => {
  return setTimeout(() => {  // This return is ignored!
    resolve('done');
  }, 1000);
});
```

**Key points:**
- ✅ Don't use `return` in executor function
- ✅ ESLint rule: `no-promise-executor-return`
- ✅ The return value is ignored anyway

---

### Pattern 4: Debounced Operations

**Use when:** User types or triggers rapid events

```javascript
class SearchComponent {
  constructor() {
    this.searchTimeout = null;
  }
  
  onSearchInput(query) {
    // Clear previous timeout
    clearTimeout(this.searchTimeout);
    
    // Set new timeout
    this.searchTimeout = setTimeout(() => {
      this.performSearch(query);
    }, 300); // 300ms debounce
  }
  
  cleanup() {
    // Always clear on cleanup
    clearTimeout(this.searchTimeout);
  }
}
```

**Key points:**
- ✅ Clear previous timeout
- ✅ Clean up in destructor
- ✅ Prevents memory leaks

---

### Pattern 5: IPC Error Handling (Electron)

**Use when:** Renderer ↔ Main process communication

```javascript
// Renderer process
async function callBackend(channel, data) {
  try {
    const result = await window.electron.invoke(channel, data);
    
    // Check for error response
    if (result.error) {
      throw new Error(result.error);
    }
    
    return result.data;
  } catch (error) {
    console.error(`[IPC] ${channel} failed:`, error);
    
    window.errorHandler.showError(
      'Backend communication failed',
      error.message,
      'https://docs.link/ipc-errors',
      () => callBackend(channel, data)
    );
    
    throw error;
  }
}
```

**Key points:**
- ✅ Handle both network and app errors
- ✅ Provide context (channel name)
- ✅ Offer retry
- ✅ Check for error in response

---

### Pattern 6: Service Health Check

**Use when:** Polling service status

```javascript
async function waitForServiceHealthy(timeout = 30000) {
  const startTime = Date.now();
  const pollInterval = 1000;
  
  while (Date.now() - startTime < timeout) {
    try {
      const healthy = await checkHealth();
      if (healthy) {
        return true;
      }
    } catch (error) {
      // Log but don't throw - we'll retry
      console.warn('[Health] Check failed, retrying...', error);
    }
    
    // Wait before next check (no return!)
    await new Promise(resolve => {
      setTimeout(resolve, pollInterval);
    });
  }
  
  throw new Error('Service failed to become healthy');
}
```

**Key points:**
- ✅ Timeout to prevent infinite loops
- ✅ Log warnings, not errors (retries expected)
- ✅ No `return` in promise executor
- ✅ Clear timeout condition

---

### Pattern 7: Unused Variables

**Use when:** Variable is intentionally unused

```javascript
// ❌ BAD: Unused variable
async function handleEvent(event, data) {
  console.log('Event received');
  // 'event' and 'data' are never used
}

// ✅ GOOD: Prefix with underscore
async function handleEvent(_event, _data) {
  console.log('Event received');
  // ESLint knows these are intentionally unused
}

// ✅ GOOD: Destructure only what you need
async function handleEvent({ type, timestamp }) {
  console.log(`Event: ${type} at ${timestamp}`);
  // Only extract what you use
}
```

**Key points:**
- ✅ Prefix unused args with `_`
- ✅ Or destructure only needed fields
- ✅ ESLint rule: `no-unused-vars`

---

### Pattern 8: Const vs Let

**Use when:** Declaring variables

```javascript
// ❌ BAD: Using 'let' when not reassigning
let apiClient = new APIClient();
let maxRetries = 3;

// ✅ GOOD: Use 'const' by default
const apiClient = new APIClient();
const maxRetries = 3;

// ✅ GOOD: Use 'let' only when reassigning
let retryCount = 0;
retryCount++; // Will be reassigned
```

**Key points:**
- ✅ Always use `const` by default
- ✅ Only use `let` if value will change
- ✅ Never use `var`
- ✅ ESLint rule: `prefer-const`

---

### Pattern 9: Async Without Await

**Use when:** Function doesn't need to be async

```javascript
// ❌ BAD: Async but no await
async function getData() {
  return fetch('/api/data');
}

// ✅ GOOD: Remove async
function getData() {
  return fetch('/api/data');
}

// ✅ GOOD: Or use await
async function getData() {
  return await fetch('/api/data');
}
```

**Key points:**
- ✅ Only use `async` if you use `await`
- ✅ Or if you want to implicitly return a Promise
- ✅ ESLint rule: `require-await`

---

### Pattern 10: Error Boundary (React/Electron)

**Use when:** Preventing app crashes from component errors

```javascript
class ErrorBoundary {
  constructor() {
    this.setupGlobalHandlers();
  }
  
  setupGlobalHandlers() {
    // Catch unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
      console.error('[Global] Unhandled promise rejection:', event.reason);
      this.handleError(event.reason);
      event.preventDefault();
    });
    
    // Catch synchronous errors
    window.addEventListener('error', (event) => {
      console.error('[Global] Unhandled error:', event.error);
      this.handleError(event.error);
      event.preventDefault();
    });
  }
  
  handleError(error) {
    // Show user-friendly error dialog
    if (window.errorHandler) {
      window.errorHandler.showError(
        'Unexpected Error',
        error.message,
        'https://docs.link/errors',
        () => window.location.reload() // Offer reload
      );
    }
  }
}
```

**Key points:**
- ✅ Catch all unhandled errors
- ✅ Prevent app crash
- ✅ Show user-friendly message
- ✅ Log for debugging

---

## 🚫 Anti-Patterns (Don't Do This!)

### ❌ Swallowing Errors

```javascript
// BAD: Error is caught but ignored
try {
  await riskyOperation();
} catch (error) {
  // Nothing here - error is lost!
}

// GOOD: At minimum, log it
try {
  await riskyOperation();
} catch (error) {
  console.error('[Module] Operation failed:', error);
  // Decide: re-throw, show to user, or handle
}
```

### ❌ Generic Error Messages

```javascript
// BAD: Not helpful
catch (error) {
  alert('Error!');
}

// GOOD: Specific and actionable
catch (error) {
  window.errorHandler.showError(
    'Failed to save customer data',
    'Network connection lost. Check your VPN.',
    'https://docs.link/network-errors',
    () => saveCustomerData()
  );
}
```

### ❌ Memory Leaks

```javascript
// BAD: Timeout never cleared
function startPolling() {
  setInterval(() => {
    checkStatus();
  }, 1000);
}

// GOOD: Store and clear
class StatusPoller {
  start() {
    this.interval = setInterval(() => {
      this.checkStatus();
    }, 1000);
  }
  
  stop() {
    clearInterval(this.interval);
  }
}
```

### ❌ Constant Conditions

```javascript
// BAD: Dead code
if (true) {
  doSomething();
} else {
  neverExecuted(); // This never runs!
}

// GOOD: Remove the condition
doSomething();

// Or if it's temporary for debugging:
// eslint-disable-next-line no-constant-condition
if (true) {
  doSomething(); // TODO: Remove after testing
}
```

---

## ✅ Checklist Before Committing

Use this checklist for all new code:

### Error Handling
- [ ] All async functions have try-catch
- [ ] All promises handle rejection
- [ ] Error messages are user-friendly
- [ ] Errors are logged with context
- [ ] Help links are provided

### Resource Cleanup
- [ ] Timeouts are cleared in `finally`
- [ ] Event listeners are removed
- [ ] Connections are closed
- [ ] No memory leaks

### Code Quality
- [ ] ESLint passes (`npm run lint`)
- [ ] No unused variables
- [ ] Use `const` unless reassigning
- [ ] Async functions use `await`
- [ ] No `return` in promise executors

### User Experience
- [ ] Loading states shown
- [ ] Errors don't crash app
- [ ] Retry options provided
- [ ] Progress indicators work

---

## 🔧 Testing Error Handling

### Manual Testing

```javascript
// Test error recovery
async function testErrorHandling() {
  try {
    // Force an error
    await fetch('http://invalid-url');
  } catch (error) {
    // Did error handler show?
    // Can user retry?
    // Is app still responsive?
  }
}
```

### Automated Testing (Jest)

```javascript
describe('Error Handling', () => {
  it('should show error dialog on API failure', async () => {
    // Mock API to fail
    mockAPI.reject(new Error('Network error'));
    
    // Trigger operation
    await expect(fetchData()).rejects.toThrow();
    
    // Verify error handler was called
    expect(window.errorHandler.showError).toHaveBeenCalled();
  });
  
  it('should clean up resources on error', async () => {
    const clearTimeoutSpy = jest.spyOn(global, 'clearTimeout');
    
    try {
      await operationThatFails();
    } catch (error) {
      // Verify cleanup happened
      expect(clearTimeoutSpy).toHaveBeenCalled();
    }
  });
});
```

---

## 📚 References

**ESLint Rules:**
- [`no-async-promise-executor`](https://eslint.org/docs/latest/rules/no-async-promise-executor)
- [`no-promise-executor-return`](https://eslint.org/docs/latest/rules/no-promise-executor-return)
- [`no-unused-vars`](https://eslint.org/docs/latest/rules/no-unused-vars)
- [`prefer-const`](https://eslint.org/docs/latest/rules/prefer-const)
- [`require-await`](https://eslint.org/docs/latest/rules/require-await)

**JavaScript Best Practices:**
- [MDN: Error Handling](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Control_flow_and_error_handling)
- [MDN: Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
- [Electron: Error Handling](https://www.electronjs.org/docs/latest/tutorial/errors)

**TAMINATOR Docs:**
- `ESLINT-REPORT.md` - Current code quality status
- `FINAL-RECOMMENDATIONS.md` - Technical debt roadmap
- `ALL-BUGS-FIXED-SUMMARY.md` - What was fixed

---

## 🎯 Summary

**Core Rules:**
1. Always catch errors
2. Always clean up resources
3. Always show user-friendly messages
4. Always log for debugging
5. Always provide help/retry options

**Quick Wins:**
- Run `npm run lint` before committing
- Use pre-commit hooks
- Prefix unused args with `_`
- Use `const` by default
- Remove `async` if no `await`

**Technical Debt Prevented:**
- No unhandled promise rejections
- No memory leaks from uncleaned resources
- No dead code from constant conditions
- No confusing error messages for users

---

**Last Updated:** November 11, 2025  
**Version:** 1.0  
**Status:** Production Ready

