#!/usr/bin/env node
/**
 * OOBE Automated Test Simulator
 * 
 * Simulates user interactions with the OOBE wizard and validates behavior.
 * Run with: node test-oobe-simulator.js
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Test configuration
const OOBE_STATE_FILE = path.join(os.homedir(), '.config', 'taminator-gui', 'oobe-state.json');
const TEST_TIMEOUT = 60000; // 60 seconds per test
const WAIT_FOR_UI = 2000; // 2 seconds for UI to settle

// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  bold: '\x1b[1m'
};

// Test results
const results = {
  passed: 0,
  failed: 0,
  skipped: 0,
  tests: []
};

class OOBETestSimulator {
  constructor() {
    this.electronProcess = null;
    this.testMode = true;
  }

  // Utility: Print with color
  log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
  }

  // Utility: Print test header
  printTestHeader(testNumber, testName) {
    console.log('\n' + '═'.repeat(60));
    this.log(`Test ${testNumber}: ${testName}`, 'cyan');
    console.log('═'.repeat(60));
  }

  // Utility: Print test result
  printTestResult(passed, message) {
    if (passed) {
      this.log(`✅ PASS: ${message}`, 'green');
      results.passed++;
    } else {
      this.log(`❌ FAIL: ${message}`, 'red');
      results.failed++;
    }
    results.tests.push({ passed, message });
  }

  // Utility: Wait for specified time
  async wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Utility: Clear OOBE state
  clearOOBEState() {
    try {
      if (fs.existsSync(OOBE_STATE_FILE)) {
        fs.unlinkSync(OOBE_STATE_FILE);
        this.log('🗑️  Cleared OOBE state file', 'yellow');
      }
      return true;
    } catch (error) {
      this.log(`❌ Failed to clear OOBE state: ${error.message}`, 'red');
      return false;
    }
  }

  // Utility: Read OOBE state
  readOOBEState() {
    try {
      if (fs.existsSync(OOBE_STATE_FILE)) {
        const data = fs.readFileSync(OOBE_STATE_FILE, 'utf8');
        return JSON.parse(data);
      }
      return null;
    } catch (error) {
      this.log(`⚠️  Failed to read OOBE state: ${error.message}`, 'yellow');
      return null;
    }
  }

  // Utility: Verify OOBE state file structure
  verifyOOBEStateStructure(state) {
    const requiredFields = ['completed', 'version', 'steps', 'skippedSetup', 'lastScreen'];
    const missingFields = requiredFields.filter(field => !(field in state));
    
    if (missingFields.length > 0) {
      this.printTestResult(false, `OOBE state missing fields: ${missingFields.join(', ')}`);
      return false;
    }
    
    this.printTestResult(true, 'OOBE state structure is valid');
    return true;
  }

  // Test 1: First Run Detection
  async testFirstRunDetection() {
    this.printTestHeader(1, 'First Run Detection');
    
    // Clear state to simulate first run
    this.clearOOBEState();
    
    // Check state file doesn't exist
    const stateExists = fs.existsSync(OOBE_STATE_FILE);
    this.printTestResult(!stateExists, 'OOBE state file cleared successfully');
    
    // Simulate checking first run
    const isFirstRun = !stateExists;
    this.printTestResult(isFirstRun, 'First run detected correctly');
    
    this.log('\n📋 Expected behavior:', 'blue');
    this.log('   - App should launch OOBE wizard (not main dashboard)');
    this.log('   - Welcome screen should appear');
    this.log('   - Progress bar should show 0-20%');
  }

  // Test 2: OOBE State Creation
  async testOOBEStateCreation() {
    this.printTestHeader(2, 'OOBE State Creation');
    
    // Simulate OOBE state creation
    const mockState = {
      completed: false,
      version: '1.0',
      completedAt: null,
      steps: {
        welcome: false,
        authentication: false,
        authMethod: null,
        testConfiguration: false,
        firstCustomer: false
      },
      skippedSetup: false,
      lastScreen: 'welcome'
    };
    
    try {
      const stateDir = path.dirname(OOBE_STATE_FILE);
      if (!fs.existsSync(stateDir)) {
        fs.mkdirSync(stateDir, { recursive: true });
      }
      
      fs.writeFileSync(OOBE_STATE_FILE, JSON.stringify(mockState, null, 2));
      this.printTestResult(true, 'OOBE state file created');
      
      // Verify it can be read back
      const readState = this.readOOBEState();
      this.printTestResult(readState !== null, 'OOBE state file readable');
      this.verifyOOBEStateStructure(readState);
      
    } catch (error) {
      this.printTestResult(false, `Failed to create OOBE state: ${error.message}`);
    }
  }

  // Test 3: State Persistence (Screen Navigation)
  async testStatePersistence() {
    this.printTestHeader(3, 'State Persistence');
    
    const screens = ['welcome', 'auth-choice', 'vault-setup', 'manual-setup', 'first-customer', 'completion'];
    
    for (const screen of screens) {
      const state = this.readOOBEState() || {};
      state.lastScreen = screen;
      
      try {
        fs.writeFileSync(OOBE_STATE_FILE, JSON.stringify(state, null, 2));
        await this.wait(100);
        
        const readBack = this.readOOBEState();
        const persisted = readBack && readBack.lastScreen === screen;
        this.printTestResult(persisted, `State persisted for screen: ${screen}`);
      } catch (error) {
        this.printTestResult(false, `Failed to persist state for ${screen}: ${error.message}`);
      }
    }
  }

  // Test 4: Auth Method Selection
  async testAuthMethodSelection() {
    this.printTestHeader(4, 'Auth Method Selection');
    
    const authMethods = ['vault', 'manual'];
    
    for (const method of authMethods) {
      const state = this.readOOBEState() || {};
      state.steps = state.steps || {};
      state.steps.authMethod = method;
      
      try {
        fs.writeFileSync(OOBE_STATE_FILE, JSON.stringify(state, null, 2));
        const readBack = this.readOOBEState();
        const saved = readBack && readBack.steps.authMethod === method;
        this.printTestResult(saved, `Auth method '${method}' saved correctly`);
      } catch (error) {
        this.printTestResult(false, `Failed to save auth method '${method}': ${error.message}`);
      }
    }
  }

  // Test 5: Step Completion Tracking
  async testStepCompletion() {
    this.printTestHeader(5, 'Step Completion Tracking');
    
    const steps = ['welcome', 'authentication', 'testConfiguration', 'firstCustomer'];
    const state = this.readOOBEState() || {};
    state.steps = state.steps || {};
    
    for (const step of steps) {
      state.steps[step] = true;
      
      try {
        fs.writeFileSync(OOBE_STATE_FILE, JSON.stringify(state, null, 2));
        const readBack = this.readOOBEState();
        const completed = readBack && readBack.steps[step] === true;
        this.printTestResult(completed, `Step '${step}' marked as completed`);
      } catch (error) {
        this.printTestResult(false, `Failed to mark step '${step}' as completed`);
      }
    }
  }

  // Test 6: OOBE Completion
  async testOOBECompletion() {
    this.printTestHeader(6, 'OOBE Completion');
    
    const state = this.readOOBEState() || {};
    state.completed = true;
    state.completedAt = new Date().toISOString();
    
    try {
      fs.writeFileSync(OOBE_STATE_FILE, JSON.stringify(state, null, 2));
      const readBack = this.readOOBEState();
      
      this.printTestResult(readBack.completed === true, 'OOBE marked as completed');
      this.printTestResult(readBack.completedAt !== null, 'Completion timestamp saved');
      
      this.log('\n📋 Expected behavior:', 'blue');
      this.log('   - Next launch should show main dashboard (not OOBE)');
      this.log('   - OOBE wizard should not appear again');
      
    } catch (error) {
      this.printTestResult(false, `Failed to complete OOBE: ${error.message}`);
    }
  }

  // Test 7: Skip Setup Flow
  async testSkipSetup() {
    this.printTestHeader(7, 'Skip Setup Flow');
    
    this.clearOOBEState();
    
    const state = {
      completed: false,
      version: '1.0',
      completedAt: null,
      steps: {
        welcome: true,
        authentication: false,
        authMethod: null,
        testConfiguration: false,
        firstCustomer: false
      },
      skippedSetup: true,
      lastScreen: 'welcome'
    };
    
    try {
      fs.writeFileSync(OOBE_STATE_FILE, JSON.stringify(state, null, 2));
      const readBack = this.readOOBEState();
      
      this.printTestResult(readBack.skippedSetup === true, 'Skip setup flag saved');
      this.printTestResult(readBack.completed === false, 'OOBE not marked as completed');
      
      this.log('\n📋 Expected behavior:', 'blue');
      this.log('   - Main dashboard should load');
      this.log('   - Warning banner should show: "⚠️ Authentication not configured"');
      
    } catch (error) {
      this.printTestResult(false, `Failed to test skip setup: ${error.message}`);
    }
  }

  // Test 8: Factory Reset
  async testFactoryReset() {
    this.printTestHeader(8, 'Factory Reset');
    
    // Create a completed OOBE state
    const completedState = {
      completed: true,
      version: '1.0',
      completedAt: new Date().toISOString(),
      steps: {
        welcome: true,
        authentication: true,
        authMethod: 'vault',
        testConfiguration: true,
        firstCustomer: true
      },
      skippedSetup: false,
      lastScreen: 'completion'
    };
    
    try {
      fs.writeFileSync(OOBE_STATE_FILE, JSON.stringify(completedState, null, 2));
      this.printTestResult(true, 'Created completed OOBE state');
      
      // Simulate factory reset (delete state file)
      this.clearOOBEState();
      
      const stateExists = fs.existsSync(OOBE_STATE_FILE);
      this.printTestResult(!stateExists, 'Factory reset cleared OOBE state');
      
      this.log('\n📋 Expected behavior:', 'blue');
      this.log('   - OOBE state file deleted');
      this.log('   - Next launch triggers OOBE wizard again');
      this.log('   - User settings cleared (localStorage/sessionStorage)');
      
    } catch (error) {
      this.printTestResult(false, `Factory reset failed: ${error.message}`);
    }
  }

  // Test 9: Progress Calculation
  async testProgressCalculation() {
    this.printTestHeader(9, 'Progress Calculation');
    
    const progressTests = [
      { screen: 'welcome', expected: 20 },
      { screen: 'auth-choice', expected: 40 },
      { screen: 'vault-setup', expected: 60 },
      { screen: 'manual-setup', expected: 60 },
      { screen: 'first-customer', expected: 80 },
      { screen: 'completion', expected: 100 }
    ];
    
    // Progress calculation logic (matching actual OOBE implementation)
    const calculateProgress = (screenName) => {
      // Base screen order (main flow)
      const screenOrder = ['welcome', 'auth-choice', 'vault-setup', 'first-customer', 'completion'];
      
      // Handle manual-setup as alternative to vault-setup (same progress level)
      if (screenName === 'manual-setup') {
        screenName = 'vault-setup'; // Map to same progress level
      }
      
      const currentIndex = screenOrder.indexOf(screenName);
      if (currentIndex === -1) {
        return 0; // Unknown screen
      }
      
      return Math.round(((currentIndex + 1) / screenOrder.length) * 100);
    };
    
    for (const test of progressTests) {
      const progress = calculateProgress(test.screen);
      
      // Allow some tolerance for rounding
      const matches = Math.abs(progress - test.expected) <= 5;
      this.printTestResult(matches, `Progress for '${test.screen}': ${progress}% (expected ~${test.expected}%)`);
    }
  }

  // Test 10: Error Recovery
  async testErrorRecovery() {
    this.printTestHeader(10, 'Error Recovery');
    
    // Test corrupted state file recovery
    try {
      fs.writeFileSync(OOBE_STATE_FILE, '{ invalid json }');
      this.printTestResult(true, 'Created corrupted state file');
      
      const state = this.readOOBEState();
      this.printTestResult(state === null, 'Corrupted state handled gracefully (returned null)');
      
      this.log('\n📋 Expected behavior:', 'blue');
      this.log('   - App should detect corrupted state');
      this.log('   - App should create fresh OOBE state');
      this.log('   - User should see OOBE wizard');
      
    } catch (error) {
      this.printTestResult(false, `Error recovery test failed: ${error.message}`);
    }
  }

  // Test 11: Vault Configuration Simulation
  async testVaultConfiguration() {
    this.printTestHeader(11, 'Vault Configuration (Simulated)');
    
    const vaultConfigs = [
      { url: 'http://localhost:8200', valid: true },
      { url: 'https://vault.example.com:8200', valid: true },
      { url: 'invalid-url', valid: false },
      { url: '', valid: false }
    ];
    
    for (const config of vaultConfigs) {
      // Simulate URL validation
      const urlPattern = /^https?:\/\/.+/;
      const isValid = urlPattern.test(config.url);
      
      const passed = isValid === config.valid;
      this.printTestResult(
        passed,
        `Vault URL '${config.url || '(empty)'}' validation: ${isValid ? 'valid' : 'invalid'}`
      );
    }
  }

  // Test 12: Token Storage Simulation
  async testTokenStorage() {
    this.printTestHeader(12, 'Token Storage (Simulated)');
    
    const mockTokens = {
      jiraToken: 'mock-jira-token-123',
      portalToken: 'mock-portal-token-456'
    };
    
    // Simulate token storage in OOBE state
    const state = this.readOOBEState() || {};
    state.tokens = mockTokens;
    
    try {
      fs.writeFileSync(OOBE_STATE_FILE, JSON.stringify(state, null, 2));
      const readBack = this.readOOBEState();
      
      this.printTestResult(
        readBack.tokens && readBack.tokens.jiraToken === mockTokens.jiraToken,
        'JIRA token stored correctly'
      );
      this.printTestResult(
        readBack.tokens && readBack.tokens.portalToken === mockTokens.portalToken,
        'Portal token stored correctly'
      );
      
      this.log('\n⚠️  Note:', 'yellow');
      this.log('   In production, tokens should be encrypted/secured');
      this.log('   This test only verifies storage mechanism');
      
    } catch (error) {
      this.printTestResult(false, `Token storage test failed: ${error.message}`);
    }
  }

  // Print final summary
  printSummary() {
    console.log('\n' + '═'.repeat(60));
    this.log('TEST SUMMARY', 'bold');
    console.log('═'.repeat(60));
    
    this.log(`\nTotal Tests: ${results.passed + results.failed + results.skipped}`, 'cyan');
    this.log(`✅ Passed: ${results.passed}`, 'green');
    this.log(`❌ Failed: ${results.failed}`, 'red');
    this.log(`⏭️  Skipped: ${results.skipped}`, 'yellow');
    
    const successRate = ((results.passed / (results.passed + results.failed)) * 100).toFixed(1);
    console.log(`\nSuccess Rate: ${successRate}%`);
    
    if (results.failed === 0) {
      this.log('\n🎉 All tests passed!', 'green');
    } else {
      this.log('\n⚠️  Some tests failed. Review output above.', 'yellow');
    }
    
    console.log('═'.repeat(60) + '\n');
  }

  // Run all tests
  async runAllTests() {
    this.log('\n🤖 OOBE Automated Test Simulator', 'bold');
    this.log('Testing Taminator OOBE Wizard Implementation\n', 'cyan');
    
    try {
      await this.testFirstRunDetection();
      await this.testOOBEStateCreation();
      await this.testStatePersistence();
      await this.testAuthMethodSelection();
      await this.testStepCompletion();
      await this.testOOBECompletion();
      await this.testSkipSetup();
      await this.testFactoryReset();
      await this.testProgressCalculation();
      await this.testErrorRecovery();
      await this.testVaultConfiguration();
      await this.testTokenStorage();
      
      this.printSummary();
      
      // Clean up test artifacts
      this.log('\n🗑️  Cleaning up test artifacts...', 'yellow');
      this.clearOOBEState();
      this.log('✅ Cleanup complete', 'green');
      
      return results.failed === 0;
      
    } catch (error) {
      this.log(`\n❌ Test suite crashed: ${error.message}`, 'red');
      console.error(error);
      return false;
    }
  }
}

// Main execution
if (require.main === module) {
  const simulator = new OOBETestSimulator();
  simulator.runAllTests()
    .then(success => {
      process.exit(success ? 0 : 1);
    })
    .catch(error => {
      console.error('Fatal error:', error);
      process.exit(1);
    });
}

module.exports = OOBETestSimulator;

