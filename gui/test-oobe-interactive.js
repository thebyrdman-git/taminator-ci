#!/usr/bin/env node
/**
 * OOBE Interactive Test Runner
 * 
 * Launches Electron app and provides test scenarios to execute manually.
 * Run with: node test-oobe-interactive.js
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');

const OOBE_STATE_FILE = path.join(os.homedir(), '.config', 'taminator-gui', 'oobe-state.json');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function question(prompt) {
  return new Promise(resolve => {
    rl.question(prompt, resolve);
  });
}

function clearScreen() {
  console.clear();
}

function printHeader(title) {
  console.log('\n' + '═'.repeat(60));
  console.log(`  ${title}`);
  console.log('═'.repeat(60) + '\n');
}

function clearOOBEState() {
  try {
    if (fs.existsSync(OOBE_STATE_FILE)) {
      fs.unlinkSync(OOBE_STATE_FILE);
      console.log('✅ OOBE state cleared');
    } else {
      console.log('ℹ️  OOBE state file does not exist');
    }
  } catch (error) {
    console.log(`❌ Failed to clear OOBE state: ${error.message}`);
  }
}

function readOOBEState() {
  try {
    if (fs.existsSync(OOBE_STATE_FILE)) {
      const data = fs.readFileSync(OOBE_STATE_FILE, 'utf8');
      return JSON.parse(data);
    }
    return null;
  } catch (error) {
    console.log(`⚠️  Failed to read OOBE state: ${error.message}`);
    return null;
  }
}

function displayOOBEState() {
  const state = readOOBEState();
  if (state) {
    console.log('📄 Current OOBE State:');
    console.log(JSON.stringify(state, null, 2));
  } else {
    console.log('ℹ️  No OOBE state exists (first run condition)');
  }
}

function launchElectron() {
  console.log('\n🚀 Launching Electron app...\n');
  const electronProcess = spawn('npm', ['run', 'start'], {
    cwd: __dirname,
    stdio: 'inherit'
  });

  return electronProcess;
}

async function runTestScenario(scenarioNum) {
  clearScreen();
  
  switch (scenarioNum) {
    case 1:
      printHeader('Test Scenario 1: First Run Experience');
      console.log('📋 Steps:');
      console.log('  1. Clear OOBE state');
      console.log('  2. Launch app');
      console.log('  3. Verify OOBE wizard appears');
      console.log('  4. Navigate through welcome screen\n');
      
      await question('Press Enter to clear OOBE state and launch app...');
      clearOOBEState();
      launchElectron();
      
      console.log('\n✅ App launched. Manual verification required:');
      console.log('   - Does OOBE wizard appear?');
      console.log('   - Does welcome screen show?');
      console.log('   - Are buttons functional?');
      break;
      
    case 2:
      printHeader('Test Scenario 2: Vault Authentication Path');
      console.log('📋 Steps:');
      console.log('  1. Clear OOBE state');
      console.log('  2. Launch app');
      console.log('  3. Select "Team Setup (Vault)"');
      console.log('  4. Enter Vault credentials');
      console.log('  5. Test connection\n');
      
      await question('Press Enter to clear OOBE state and launch app...');
      clearOOBEState();
      launchElectron();
      
      console.log('\n✅ App launched. Follow these steps:');
      console.log('   1. Click "Let\'s Get Started"');
      console.log('   2. Select "Team Setup (Vault)" card');
      console.log('   3. Enter Vault URL: http://miraclemax.local:8201');
      console.log('   4. Enter Vault token');
      console.log('   5. Click "Test Connection"');
      console.log('   6. Verify success or error message');
      break;
      
    case 3:
      printHeader('Test Scenario 3: Manual Token Path');
      console.log('📋 Steps:');
      console.log('  1. Clear OOBE state');
      console.log('  2. Launch app');
      console.log('  3. Select "Personal Setup"');
      console.log('  4. Enter JIRA token');
      console.log('  5. Test token validation\n');
      
      await question('Press Enter to clear OOBE state and launch app...');
      clearOOBEState();
      launchElectron();
      
      console.log('\n✅ App launched. Follow these steps:');
      console.log('   1. Click "Let\'s Get Started"');
      console.log('   2. Select "Personal Setup" card');
      console.log('   3. Enter a fake JIRA token: "fake-token-123"');
      console.log('   4. Click "Test JIRA Token"');
      console.log('   5. Verify error message appears');
      console.log('   6. (Optional) Enter real token and verify success');
      break;
      
    case 4:
      printHeader('Test Scenario 4: State Persistence');
      console.log('📋 Steps:');
      console.log('  1. Clear OOBE state');
      console.log('  2. Launch app');
      console.log('  3. Navigate to mid-wizard');
      console.log('  4. Close app');
      console.log('  5. Relaunch and verify resume\n');
      
      await question('Press Enter to clear OOBE state and launch app...');
      clearOOBEState();
      launchElectron();
      
      console.log('\n✅ App launched. Follow these steps:');
      console.log('   1. Navigate through OOBE to "Manual Setup" screen');
      console.log('   2. Close the app (Ctrl+C or close window)');
      console.log('   3. Press Enter here to relaunch');
      await question('   Press Enter after closing app...');
      launchElectron();
      console.log('   4. Verify app resumes at "Manual Setup" screen');
      break;
      
    case 5:
      printHeader('Test Scenario 5: Factory Reset');
      console.log('📋 Steps:');
      console.log('  1. Complete OOBE fully');
      console.log('  2. Navigate to Settings → Danger Zone');
      console.log('  3. Click "Factory Reset"');
      console.log('  4. Verify OOBE restarts\n');
      
      console.log('⚠️  This test requires completing OOBE first.');
      const complete = await question('Have you completed OOBE? (y/n): ');
      
      if (complete.toLowerCase() === 'y') {
        launchElectron();
        console.log('\n✅ App launched. Follow these steps:');
        console.log('   1. Navigate to Settings tab (gear icon)');
        console.log('   2. Scroll to bottom to find "Danger Zone"');
        console.log('   3. Click "Factory Reset" button');
        console.log('   4. Confirm the dialog');
        console.log('   5. Verify OOBE wizard appears again');
      } else {
        console.log('\n⚠️  Complete OOBE first, then run this test.');
        await question('Press Enter to clear state and launch for setup...');
        clearOOBEState();
        launchElectron();
      }
      break;
      
    case 6:
      printHeader('Test Scenario 6: Skip Setup Flow');
      console.log('📋 Steps:');
      console.log('  1. Clear OOBE state');
      console.log('  2. Launch app');
      console.log('  3. Click "Skip Setup"');
      console.log('  4. Verify dashboard with warning\n');
      
      await question('Press Enter to clear OOBE state and launch app...');
      clearOOBEState();
      launchElectron();
      
      console.log('\n✅ App launched. Follow these steps:');
      console.log('   1. On welcome screen, click "Skip Setup"');
      console.log('   2. Verify main dashboard loads');
      console.log('   3. Verify warning banner appears at top');
      console.log('   4. Warning should say: "⚠️ Authentication not configured"');
      break;
      
    case 7:
      printHeader('Test Scenario 7: Progress Bar Verification');
      console.log('📋 Steps:');
      console.log('  1. Clear OOBE state');
      console.log('  2. Launch app');
      console.log('  3. Navigate through all screens');
      console.log('  4. Verify progress bar updates\n');
      
      await question('Press Enter to clear OOBE state and launch app...');
      clearOOBEState();
      launchElectron();
      
      console.log('\n✅ App launched. Verify progress bar at each screen:');
      console.log('   - Welcome: ~20%');
      console.log('   - Auth Choice: ~40%');
      console.log('   - Vault/Manual Setup: ~60%');
      console.log('   - First Customer: ~80%');
      console.log('   - Completion: 100%');
      break;
      
    case 8:
      printHeader('Test Scenario 8: Back Button Navigation');
      console.log('📋 Steps:');
      console.log('  1. Clear OOBE state');
      console.log('  2. Launch app');
      console.log('  3. Navigate forward, then backward');
      console.log('  4. Verify state preservation\n');
      
      await question('Press Enter to clear OOBE state and launch app...');
      clearOOBEState();
      launchElectron();
      
      console.log('\n✅ App launched. Follow these steps:');
      console.log('   1. Click "Let\'s Get Started"');
      console.log('   2. Click "← Back" button');
      console.log('   3. Verify welcome screen appears');
      console.log('   4. Click "Next" again');
      console.log('   5. Verify auth choice screen appears');
      console.log('   6. Select an option, then click "← Back"');
      console.log('   7. Verify selection is preserved when going forward');
      break;
      
    case 9:
      printHeader('Test Scenario 9: Error Recovery');
      console.log('📋 Steps:');
      console.log('  1. Test invalid inputs');
      console.log('  2. Verify error messages');
      console.log('  3. Verify recovery is possible\n');
      
      await question('Press Enter to clear OOBE state and launch app...');
      clearOOBEState();
      launchElectron();
      
      console.log('\n✅ App launched. Test these error scenarios:');
      console.log('   1. Enter invalid Vault URL (e.g., "not-a-url")');
      console.log('      - Verify clear error message');
      console.log('   2. Enter fake JIRA token');
      console.log('      - Verify validation fails gracefully');
      console.log('   3. Test with empty fields');
      console.log('      - Verify helpful validation messages');
      break;
      
    case 10:
      printHeader('Test Scenario 10: View Current State');
      console.log('📄 Current OOBE State:\n');
      displayOOBEState();
      await question('\nPress Enter to return to menu...');
      break;
      
    default:
      console.log('❌ Invalid scenario number');
  }
}

async function mainMenu() {
  while (true) {
    clearScreen();
    printHeader('OOBE Interactive Test Runner');
    
    console.log('Available Test Scenarios:\n');
    console.log('  1. First Run Experience');
    console.log('  2. Vault Authentication Path');
    console.log('  3. Manual Token Path');
    console.log('  4. State Persistence (Exit & Resume)');
    console.log('  5. Factory Reset');
    console.log('  6. Skip Setup Flow');
    console.log('  7. Progress Bar Verification');
    console.log('  8. Back Button Navigation');
    console.log('  9. Error Recovery');
    console.log(' 10. View Current OOBE State');
    console.log('\n  0. Exit\n');
    
    const choice = await question('Select test scenario (0-10): ');
    const num = parseInt(choice);
    
    if (num === 0) {
      console.log('\n👋 Exiting test runner...\n');
      rl.close();
      process.exit(0);
    }
    
    if (num >= 1 && num <= 10) {
      await runTestScenario(num);
      await question('\nPress Enter to return to menu...');
    } else {
      console.log('\n❌ Invalid choice. Please select 0-10.');
      await question('Press Enter to continue...');
    }
  }
}

// Main execution
if (require.main === module) {
  console.log('\n🤖 OOBE Interactive Test Runner');
  console.log('This tool helps you test OOBE scenarios manually\n');
  
  mainMenu().catch(error => {
    console.error('Fatal error:', error);
    rl.close();
    process.exit(1);
  });
}

