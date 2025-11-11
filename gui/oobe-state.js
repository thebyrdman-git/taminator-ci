/**
 * OOBE (Out-of-Box Experience) State Management
 * Handles first-run detection and setup wizard state persistence
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// OOBE state file location
const OOBE_DIR = path.join(os.homedir(), '.config', 'taminator-gui');
const OOBE_STATE_FILE = path.join(OOBE_DIR, 'oobe-state.json');

/**
 * Default OOBE state structure
 */
const DEFAULT_OOBE_STATE = {
  completed: false,
  version: '1.0',
  completedAt: null,
  steps: {
    welcome: false,
    authentication: false,
    authMethod: null, // 'vault' or 'manual'
    testConfiguration: false,
    firstCustomer: false
  },
  skippedSetup: false,
  lastScreen: 'welcome'
};

class OOBEStateManager {
  constructor() {
    this.state = this.loadState();
  }

  /**
   * Check if this is the first run (OOBE not completed)
   */
  isFirstRun() {
    return !this.state.completed;
  }

  /**
   * Check if setup was skipped
   */
  wasSetupSkipped() {
    return this.state.skippedSetup;
  }

  /**
   * Load OOBE state from disk
   */
  loadState() {
    try {
      if (fs.existsSync(OOBE_STATE_FILE)) {
        const data = fs.readFileSync(OOBE_STATE_FILE, 'utf8');
        const state = JSON.parse(data);

        // Merge with defaults to handle version upgrades
        return { ...DEFAULT_OOBE_STATE, ...state };
      }
    } catch (error) {
      console.warn('[OOBE] Could not load state, using defaults:', error.message);
    }

    return { ...DEFAULT_OOBE_STATE };
  }

  /**
   * Save OOBE state to disk
   */
  saveState() {
    try {
      // Ensure directory exists
      if (!fs.existsSync(OOBE_DIR)) {
        fs.mkdirSync(OOBE_DIR, { recursive: true });
      }

      // Write state file
      fs.writeFileSync(
        OOBE_STATE_FILE,
        JSON.stringify(this.state, null, 2),
        'utf8'
      );

      return true;
    } catch (error) {
      console.error('[OOBE] Could not save state:', error.message);
      return false;
    }
  }

  /**
   * Mark a specific step as completed
   */
  completeStep(stepName) {
    if (Object.prototype.hasOwnProperty.call(this.state.steps, stepName)) {
      this.state.steps[stepName] = true;
      this.saveState();
    }
  }

  /**
   * Update the last screen user was on
   */
  updateLastScreen(screenName) {
    this.state.lastScreen = screenName;
    this.saveState();
  }

  /**
   * Set authentication method (vault or manual)
   */
  setAuthMethod(method) {
    if (method === 'vault' || method === 'manual') {
      this.state.steps.authMethod = method;
      this.saveState();
    }
  }

  /**
   * Mark OOBE as completed
   */
  completeOOBE() {
    this.state.completed = true;
    this.state.completedAt = new Date().toISOString();
    this.saveState();
  }

  /**
   * Mark setup as skipped
   */
  skipSetup() {
    this.state.skippedSetup = true;
    this.state.completed = true; // Don't show OOBE again
    this.state.completedAt = new Date().toISOString();
    this.saveState();
  }

  /**
   * Reset OOBE state (for factory reset)
   */
  resetState() {
    this.state = { ...DEFAULT_OOBE_STATE };

    // Delete the state file
    try {
      if (fs.existsSync(OOBE_STATE_FILE)) {
        fs.unlinkSync(OOBE_STATE_FILE);
      }
    } catch (error) {
      console.error('[OOBE] Could not delete state file:', error.message);
    }

    return true;
  }

  /**
   * Get current state
   */
  getState() {
    return { ...this.state };
  }

  /**
   * Get OOBE state file path (for debugging)
   */
  getStateFilePath() {
    return OOBE_STATE_FILE;
  }
}

// Export singleton instance
module.exports = new OOBEStateManager();


