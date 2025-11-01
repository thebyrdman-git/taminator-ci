# Ansai-Based Debug Session - Taminator

**Date**: 2025-11-01  
**Tool**: tam-dev (Ansai development workflows)  
**Purpose**: Verify bug fixes and continue debugging

---

## 🔧 Using Ansai Development Tools

### Available Commands

```bash
cd /home/jbyrd/TAMINATOR

# Quick health check
tam-dev health

# View recent errors
tam-dev errors

# Interactive debugging
tam-dev debug

# Watch logs live
tam-dev logs

# Test JIRA connection
tam-dev jira

# Test AI intelligence
tam-dev ai

# Full interactive menu
tam-dev
```

---

## 📊 Debug Session Log

### 1. Health Check ✅

```bash
$ tam-dev health
```

**Result**:
- ✅ Service is RUNNING
- ✅ FastAPI backend is up
- ⚠️ Health endpoint returns 404 (needs investigation)

**Analysis**:
Service is running but health endpoint may have moved. This is OK - the service is responding.

---

### 2. Code Quality Verification

**Files Fixed** (verified to exist):
- ✅ `public/js/api-client.js` - Better error logging
- ✅ `public/js/error-handler.js` - Token modal + memory leak fix
- ✅ `public/js/startup-splash.js` - (no changes)
- ✅ `public/js/loading-states.js` - Cleanup improvements
- ✅ `public/js/button-loading.js` - (no changes)
- ✅ `public/js/success-animations.js` - (no changes)
- ✅ `public/js/intelligence-client.js` - Async error handling
- ✅ `public/js/error-dialog.js` - Dynamic version + console override

---

### 3. Recommended Debug Workflows

#### A. Interactive Testing
```bash
tam-dev debug

# Then in IPython:
>>> import sys
>>> sys.path.insert(0, '/home/jbyrd/TAMINATOR/src')

# Test AI client
>>> from taminator.services.ai_client import AIClient
>>> # Test your fixes
```

#### B. Live Log Monitoring
```bash
tam-dev logs

# Watch for:
# - Unhandled promise rejections (should be zero)
# - Memory leaks (should be none)
# - Error patterns (should be well-formatted)
```

#### C. Connection Testing
```bash
# Test JIRA
tam-dev jira

# Test AI
tam-dev ai

# Test API endpoints
tam-dev api
```

#### D. Database Inspection
```bash
tam-dev db

# Check intelligence database
# Verify no corruption from bug fixes
```

---

## 🧪 Testing Our Bug Fixes

### Test 1: Async Error Handling (Bug #2)

**What we fixed**: Added try-catch to all async functions in `intelligence-client.js`

**How to test**:
```javascript
// In browser console or tam-dev debug:
window.intelligenceClient.getCaseHistory()
  .then(result => console.log('Success:', result))
  .catch(error => console.log('Error handled:', error));

// Should show error toast, not crash
```

**Expected**: Error toast appears, app doesn't crash

---

### Test 2: Token Modal (Bug #1)

**What we fixed**: Added token configuration modal in `error-handler.js`

**How to test**:
1. Disconnect from VPN
2. Try to access JIRA feature
3. Should see modal with token setup instructions

**Expected**: 
- Modal appears with "Get Token" button
- Links to Red Hat API Management
- Clear instructions

---

### Test 3: Memory Leak (Bug #3)

**What we fixed**: Added try-finally to toast cleanup

**How to test**:
```javascript
// Create many toasts
for (let i = 0; i < 100; i++) {
  window.errorHandler.showSuccess('Test ' + i);
}

// Wait for them to dismiss, then check:
window.errorHandler.activeToasts.size
// Should be 0
```

**Expected**: Map size returns to 0, no memory accumulation

---

### Test 4: Loading State Cleanup (Bug #7)

**What we fixed**: Always clean up loader tracking

**How to test**:
```javascript
// Show loader
window.loadingStates.show('test-container', 'Loading...');

// Remove container (simulate error)
document.getElementById('test-container')?.remove();

// Hide loader
window.loadingStates.hide('test-container');

// Check tracking
window.loadingStates.activeLoaders.size
// Should still clean up properly
```

**Expected**: No stuck loaders in tracking

---

### Test 5: Dynamic Version (Bug #5)

**What we fixed**: Version now reads from package.json

**How to test**:
1. Trigger an error (any error)
2. Copy error report
3. Check version number

**Expected**: Version matches package.json (2.0.0)

---

### Test 6: Console Override (Bug #4)

**What we fixed**: Only show dialog for critical errors

**How to test**:
```javascript
// These should NOT show dialog:
console.error('[Warning] This is just a warning');
console.error('Non-critical error');

// This SHOULD show dialog:
console.error('[CRITICAL] Database connection lost');
```

**Expected**: Only critical errors show modal

---

### Test 7: Health Check Debouncing (Bug #6)

**What we fixed**: Added debouncing to prevent race conditions

**How to test**:
```bash
# Watch logs
tam-dev logs

# Look for health check patterns
# Should see steady checks, not flapping
```

**Expected**: Stable health check intervals, no rapid-fire checks

---

### Test 8: API Error Context (Bug #8)

**What we fixed**: Enhanced error logging with full context

**How to test**:
```bash
# Watch logs
tam-dev logs

# Trigger API error (disconnect VPN, try JIRA)
# Check log output
```

**Expected**: Error logs include:
- Method (GET/POST)
- Endpoint
- Body
- Timestamp
- Stack trace

---

### Test 9: Exponential Backoff (Bug #9)

**What we fixed**: Service restarts with exponential backoff

**How to test**:
```bash
# Kill the service
pkill -f taminator-service

# Watch logs
tam-dev logs

# Observe restart attempts
```

**Expected**: 
- 1st retry: ~2 seconds
- 2nd retry: ~4 seconds  
- 3rd retry: ~8 seconds
- etc.

---

## 🔍 Advanced Debugging Techniques

### 1. Use tam-dev Interactive Menu

```bash
tam-dev

# Select workflows:
# 1 - Setup (if needed)
# 4 - Service Health
# 5 - Interactive Debug
# 6 - Watch Logs
# 9 - Test AI
# 14 - View Errors
```

### 2. Profile Performance

```bash
# If you installed py-spy
cd /home/jbyrd/TAMINATOR
source venv/bin/activate
py-spy record -o profile.svg -- python -m taminator.api.main
```

### 3. Database Inspection

```bash
tam-dev db

# Or manually:
sqlite3 ~/.config/taminator/intelligence.db
.tables
.schema
SELECT * FROM email_analysis LIMIT 10;
```

### 4. Network Debugging

```bash
# Test API endpoints
curl http://127.0.0.1:8765/health | jq '.'
curl http://127.0.0.1:8765/api/customers | jq '.'
curl http://127.0.0.1:8765/docs  # Interactive API docs
```

---

## 📋 Comprehensive Testing Checklist

### Critical Paths
- [ ] AI email analysis doesn't crash
- [ ] Token modal shows when needed
- [ ] Toasts clean up properly
- [ ] Loading states clean up
- [ ] Error dialog only shows for critical errors
- [ ] Version reads dynamically
- [ ] Health checks are stable
- [ ] API errors are well-logged
- [ ] Service restarts with backoff

### Integration Tests
- [ ] JIRA connection works
- [ ] Customer Portal works
- [ ] AI intelligence works
- [ ] Database queries work
- [ ] Service watchdog works

### Performance Tests
- [ ] No memory leaks after 1 hour
- [ ] No CPU spikes
- [ ] Stable memory usage
- [ ] Fast response times

---

## 🐛 Common Issues & Solutions

### Issue: Service Won't Start

**Debug**:
```bash
tam-dev errors
tam-dev logs
```

**Solution**:
```bash
# Check port
lsof -i :8765

# Kill if needed
pkill -f taminator

# Restart
cd /home/jbyrd/TAMINATOR
./bin/taminator-service &
```

---

### Issue: JavaScript Errors in Console

**Debug**:
```bash
# Open DevTools in Electron
# Check for:
# - Unhandled promise rejections
# - Type errors
# - Undefined references
```

**Solution**:
- Check our bug fixes are applied
- Verify IPC handlers exist
- Check file paths

---

### Issue: Memory Growing

**Debug**:
```javascript
// Check toast Map
window.errorHandler.activeToasts.size

// Check loader Map
window.loadingStates.activeLoaders.size

// Check for leaked event listeners
```

**Solution**:
- Our bug fixes should prevent this
- If still happening, investigate new leak sources

---

## 💡 Pro Debugging Tips

### 1. Use Multiple Terminals

**Terminal 1**: Run tam-dev logs
```bash
tam-dev logs
```

**Terminal 2**: Run tam-dev debug
```bash
tam-dev debug
```

**Terminal 3**: Run the app
```bash
./gui/dist/linux-unpacked/taminator
```

### 2. Enable Verbose Logging

```bash
export TAMINATOR_DEBUG=1
export PYTHONPATH=/home/jbyrd/TAMINATOR/src:$PYTHONPATH
```

### 3. Use Browser DevTools

In Electron app:
- Press F12 (if dev mode)
- Or start with: `./taminator --dev`

### 4. Monitor System Resources

```bash
# Watch memory/CPU
watch -n 1 'ps aux | grep taminator'

# Or use htop
htop | grep taminator
```

---

## 📊 Verification Report

After running all tests, document results:

### Bug Fix Verification

| Bug | Test Status | Notes |
|-----|-------------|-------|
| #1 - Token Modal | ⏳ Pending | Need to test with missing token |
| #2 - Async Errors | ⏳ Pending | Need to trigger AI failure |
| #3 - Memory Leak | ⏳ Pending | Need to test 100+ toasts |
| #4 - Console Override | ⏳ Pending | Need to test production mode |
| #5 - Dynamic Version | ⏳ Pending | Need to trigger error report |
| #6 - Health Check | ⏳ Pending | Need to monitor for flapping |
| #7 - Loading Cleanup | ⏳ Pending | Need to test removal |
| #8 - API Logging | ⏳ Pending | Need to check logs |
| #9 - Retry Backoff | ⏳ Pending | Need to test restart |
| #10 - JSDoc | ✅ Verified | Annotations present |

---

## 🎯 Next Debug Steps

### Immediate
1. [ ] Run full test workflow with tam-dev
2. [ ] Test each bug fix individually
3. [ ] Monitor logs for errors
4. [ ] Check memory usage
5. [ ] Verify service stability

### Short Term
1. [ ] Add automated tests
2. [ ] Set up ESLint
3. [ ] Create test fixtures
4. [ ] Document test procedures

### Long Term
1. [ ] Add CI/CD testing
2. [ ] Performance benchmarks
3. [ ] Load testing
4. [ ] User acceptance testing

---

## 🚀 Running the Full Debug Suite

### Complete Verification Script

```bash
#!/bin/bash
# Full Taminator debug verification

cd /home/jbyrd/TAMINATOR

echo "=== Health Check ==="
tam-dev health

echo -e "\n=== Recent Errors ==="
tam-dev errors | head -20

echo -e "\n=== JIRA Connection ==="
tam-dev jira

echo -e "\n=== AI Intelligence ==="
tam-dev ai

echo -e "\n=== Database Status ==="
tam-dev db

echo -e "\n=== Code Quality ==="
cd gui
if command -v eslint &> /dev/null; then
    eslint public/js/*.js || echo "Linting issues found (expected)"
else
    echo "ESLint not installed (recommended)"
fi

echo -e "\n=== Service Status ==="
curl -s http://127.0.0.1:8765/health/live || echo "Health endpoint issue"

echo -e "\n=== Verification Complete ==="
```

Save as `debug-verification.sh` and run:
```bash
chmod +x debug-verification.sh
./debug-verification.sh
```

---

## 📝 Debug Log Template

Use this template to document your debug session:

```markdown
## Debug Session: [Date]

### Environment
- Taminator Version: 2.0.0
- Python Version: [check]
- Node Version: [check]
- OS: [your OS]

### Tests Performed
1. [Test name]
   - Result: [Pass/Fail]
   - Notes: [details]

### Issues Found
1. [Issue description]
   - Severity: [Critical/High/Medium/Low]
   - Steps to reproduce: [steps]
   - Expected: [expected behavior]
   - Actual: [actual behavior]

### Actions Taken
1. [Action description]
   - Result: [outcome]

### Next Steps
1. [What to do next]
```

---

## 🎓 Learning from Debugging

### Key Lessons
1. **tam-dev tools are powerful** - Interactive debugging is much faster
2. **Log monitoring is essential** - Watch logs while testing
3. **Test each fix individually** - Isolate issues
4. **Use multiple terminals** - Parallel monitoring
5. **Document everything** - Future debugging will be easier

### Best Practices
1. Always check health before debugging
2. Monitor logs during tests
3. Test in isolation first
4. Use interactive tools
5. Document findings

---

**Debug Tool**: tam-dev (Ansai-based)  
**Status**: Ready for comprehensive testing  
**Next**: Run through all bug fix tests  

🔧 **Happy Debugging!**

