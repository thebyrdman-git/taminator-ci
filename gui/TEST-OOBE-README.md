# 🧪 OOBE Automated Testing System

**Two testing modes available:**
1. **Automated Simulator** - Runs tests automatically, no Electron launch
2. **Interactive Runner** - Guides you through manual testing with Electron

---

## 🤖 Automated Simulator

**What it does:**
- Tests OOBE state management
- Validates file operations
- Checks logic without launching UI
- Fast feedback (runs in ~5 seconds)

**Run it:**
```bash
cd /home/jbyrd/TAMINATOR/gui
node test-oobe-simulator.js
```

**Sample output:**
```
🤖 OOBE Automated Test Simulator
Testing Taminator OOBE Wizard Implementation

═══════════════════════════════════════════════════════
Test 1: First Run Detection
═══════════════════════════════════════════════════════
🗑️  Cleared OOBE state file
✅ PASS: OOBE state file cleared successfully
✅ PASS: First run detected correctly

📋 Expected behavior:
   - App should launch OOBE wizard (not main dashboard)
   - Welcome screen should appear
   - Progress bar should show 0-20%

[... more tests ...]

═══════════════════════════════════════════════════════
TEST SUMMARY
═══════════════════════════════════════════════════════

Total Tests: 45
✅ Passed: 45
❌ Failed: 0
⏭️  Skipped: 0

Success Rate: 100.0%

🎉 All tests passed!
═══════════════════════════════════════════════════════
```

**Tests included:**
1. ✅ First run detection
2. ✅ OOBE state creation
3. ✅ State persistence (screen navigation)
4. ✅ Auth method selection (Vault/Manual)
5. ✅ Step completion tracking
6. ✅ OOBE completion
7. ✅ Skip setup flow
8. ✅ Factory reset
9. ✅ Progress calculation
10. ✅ Error recovery (corrupted state)
11. ✅ Vault configuration validation
12. ✅ Token storage simulation

---

## 🎮 Interactive Test Runner

**What it does:**
- Launches Electron app for you
- Provides step-by-step test scenarios
- Guides manual verification
- Interactive menu system

**Run it:**
```bash
cd /home/jbyrd/TAMINATOR/gui
node test-oobe-interactive.js
```

**Sample output:**
```
═══════════════════════════════════════════════════════
OOBE Interactive Test Runner
═══════════════════════════════════════════════════════

Available Test Scenarios:

  1. First Run Experience
  2. Vault Authentication Path
  3. Manual Token Path
  4. State Persistence (Exit & Resume)
  5. Factory Reset
  6. Skip Setup Flow
  7. Progress Bar Verification
  8. Back Button Navigation
  9. Error Recovery
 10. View Current OOBE State

  0. Exit

Select test scenario (0-10): _
```

**Example workflow:**
1. Select scenario (e.g., "2. Vault Authentication Path")
2. Script clears OOBE state
3. Script launches Electron app
4. Script shows step-by-step instructions
5. You manually verify each step
6. Return to menu for next scenario

---

## 🚀 Quick Start

### Run both tests:
```bash
cd /home/jbyrd/TAMINATOR/gui

# 1. Automated tests (fast)
node test-oobe-simulator.js

# 2. Interactive tests (manual verification)
node test-oobe-interactive.js
```

### Or use npm scripts:
```bash
# Automated tests
npm run test:oobe

# Interactive tests
npm run test:oobe:interactive
```

---

## 📊 Test Coverage

### What's Tested Automatically
- ✅ State file creation/deletion
- ✅ JSON serialization/deserialization
- ✅ Screen navigation logic
- ✅ Progress calculation
- ✅ Auth method storage
- ✅ Step completion tracking
- ✅ Factory reset behavior
- ✅ Error recovery (corrupted files)
- ✅ URL validation
- ✅ Token storage mechanism

### What Requires Manual Testing
- ⚠️ UI rendering (screens appear correctly)
- ⚠️ Button clicks and interactions
- ⚠️ Form validation messages
- ⚠️ Network requests (Vault/JIRA/Portal APIs)
- ⚠️ Visual design and layout
- ⚠️ Animation and transitions
- ⚠️ Keyboard navigation
- ⚠️ Error message clarity

---

## 🎯 Testing Strategy

**Recommended flow:**

1. **Start with automated tests**
   ```bash
   node test-oobe-simulator.js
   ```
   - Fast feedback on logic
   - Verify state management works
   - ~5 seconds

2. **Run interactive scenarios**
   ```bash
   node test-oobe-interactive.js
   ```
   - Launch app for each scenario
   - Verify UI behavior
   - ~15 minutes total

3. **Full end-to-end test**
   ```bash
   # Clear state and run app manually
   rm -f ~/.config/taminator-gui/oobe-state.json
   npm run start
   ```
   - Complete OOBE flow fully
   - Test with real tokens (if available)
   - ~10 minutes

---

## 🔍 Debugging Test Failures

### Automated test fails
```bash
# Run with verbose output
DEBUG=1 node test-oobe-simulator.js

# Check OOBE state file manually
cat ~/.config/taminator-gui/oobe-state.json | jq
```

### Interactive test issues
```bash
# View current OOBE state (option 10 in menu)
node test-oobe-interactive.js
# Select: 10

# Or manually:
cat ~/.config/taminator-gui/oobe-state.json
```

### App won't launch
```bash
# Verify dependencies installed
cd /home/jbyrd/TAMINATOR/gui
npm install

# Check Electron is available
npx electron --version

# Run with dev mode
npm run dev
```

---

## 📝 Adding New Tests

### To add automated test:

Edit `test-oobe-simulator.js`:

```javascript
// Add new test method
async testMyNewFeature() {
  this.printTestHeader(13, 'My New Feature');
  
  // Test logic here
  const result = someTestLogic();
  this.printTestResult(result === expected, 'Feature works correctly');
}

// Add to runAllTests():
async runAllTests() {
  // ... existing tests ...
  await this.testMyNewFeature();
  // ...
}
```

### To add interactive scenario:

Edit `test-oobe-interactive.js`:

```javascript
// Add new case in runTestScenario():
case 11:
  printHeader('Test Scenario 11: My New Test');
  console.log('📋 Steps:');
  console.log('  1. Do something');
  console.log('  2. Verify something\n');
  
  await question('Press Enter to launch...');
  clearOOBEState();
  launchElectron();
  
  console.log('\n✅ App launched. Follow these steps:');
  console.log('   - Step 1');
  console.log('   - Step 2');
  break;
```

---

## 🎨 Test Output Examples

### All tests pass:
```
═══════════════════════════════════════════════════════
TEST SUMMARY
═══════════════════════════════════════════════════════

Total Tests: 45
✅ Passed: 45
❌ Failed: 0
⏭️  Skipped: 0

Success Rate: 100.0%

🎉 All tests passed!
═══════════════════════════════════════════════════════
```

### Some tests fail:
```
═══════════════════════════════════════════════════════
Test 3: State Persistence
═══════════════════════════════════════════════════════
✅ PASS: State persisted for screen: welcome
✅ PASS: State persisted for screen: auth-choice
❌ FAIL: State persisted for screen: vault-setup
✅ PASS: State persisted for screen: manual-setup
...

═══════════════════════════════════════════════════════
TEST SUMMARY
═══════════════════════════════════════════════════════

Total Tests: 45
✅ Passed: 42
❌ Failed: 3
⏭️  Skipped: 0

Success Rate: 93.3%

⚠️  Some tests failed. Review output above.
═══════════════════════════════════════════════════════
```

---

## 🔧 Troubleshooting

### "Cannot find module"
```bash
cd /home/jbyrd/TAMINATOR/gui
npm install
```

### "ENOENT: no such file or directory"
```bash
# Create config directory
mkdir -p ~/.config/taminator-gui
```

### "Permission denied"
```bash
# Make scripts executable
chmod +x test-oobe-simulator.js test-oobe-interactive.js
```

### State file locked/corrupted
```bash
# Force delete and recreate
rm -f ~/.config/taminator-gui/oobe-state.json
rm -rf ~/.config/taminator-gui
mkdir -p ~/.config/taminator-gui
```

---

## 📚 Additional Resources

- **Full OOBE Testing Guide:** `../OOBE-COMPLETE-SUMMARY.md`
- **OOBE Design Spec:** `../FIRST-TIME-EXPERIENCE-DESIGN.md`
- **Implementation Status:** `../OOBE-V1.10.0-WIP.md`
- **Main README:** `../README.md`

---

## 🎯 Success Criteria

**Tests pass when:**
- ✅ Automated simulator: 100% pass rate
- ✅ Interactive tests: All scenarios verified manually
- ✅ Full end-to-end: Complete OOBE without errors
- ✅ Factory reset: Returns to first-run state
- ✅ State persistence: Resumes correctly after exit

**Ready for release when:**
- ✅ All automated tests pass
- ✅ All interactive scenarios verified
- ✅ No console errors in browser DevTools
- ✅ Vault and Manual paths both work
- ✅ Factory reset works correctly

---

**Created:** October 24, 2025  
**Version:** 1.0  
**For:** Taminator v1.10.0 OOBE Testing

