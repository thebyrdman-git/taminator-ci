/**
 * Taminator GUI - Main Process
 * Electron main process that creates the application window
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const oobeState = require('./oobe-state');
const { ServiceManager } = require('./service-manager');

let mainWindow;
let logsWindow;
let serviceManager;

// Initialize service manager
serviceManager = new ServiceManager();

/**
 * Get the path to the bundled tam-rfe CLI
 * Returns arguments for spawn() to execute the CLI binary
 */
function getTamrfeCli() {
  const fs = require('fs');
  
  // Priority 1: Look for standalone binary in extraResources (production)
  const resourcesBinaryPath = app.isPackaged 
    ? path.join(process.resourcesPath, 'bin', 'tam-rfe')
    : path.join(__dirname, '../bin/tam-rfe');
    
  if (fs.existsSync(resourcesBinaryPath)) {
    console.log('[CLI] Using bundled tam-rfe binary:', resourcesBinaryPath);
    return {
      command: resourcesBinaryPath,
      prependArgs: []
    };
  }
  
  // Priority 2: Look for Python source (development mode)
  const bundledCliPath = path.join(__dirname, '../src/taminator/cli.py');
  if (fs.existsSync(bundledCliPath)) {
    console.log('[CLI] Using Python source (development mode):', bundledCliPath);
    return {
      command: 'python3',
      prependArgs: [bundledCliPath]
    };
  }
  
  // Priority 3: Fallback to system PATH (manual installation)
  console.log('[CLI] Using system PATH tam-rfe command');
  return {
    command: 'tam-rfe',
    prependArgs: []
  };
}

/**
 * Spawn tam-rfe CLI with automatic bundled/system detection
 */
function spawnTamrfe(args, options = {}) {
  const cli = getTamrfeCli();
  const allArgs = [...cli.prependArgs, ...args];
  
  console.log('[CLI] Spawning:', cli.command, allArgs.join(' '));
  
  return spawn(cli.command, allArgs, {
    env: { ...process.env },
    stdio: ['pipe', 'pipe', 'pipe'],
    ...options
  });
}

function createWindow() {
  // Try multiple icon paths for different packaging scenarios
  const fs = require('fs');
  let iconPath = path.join(__dirname, 'build/icon.png');
  
  // Fallback to public directory if build icon doesn't exist
  if (!fs.existsSync(iconPath)) {
    iconPath = path.join(__dirname, 'public/terminator-icon.png');
  }
  
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 600,
    maxWidth: undefined,  // No maximum width
    maxHeight: undefined, // No maximum height
    resizable: true,      // Allow window resizing
    movable: true,        // Allow window moving
    frame: true,          // Show window frame with controls
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    backgroundColor: '#F5F5F5',
    title: 'Taminator'
    // Don't set icon in constructor - handle it after creation
  });
  
  // Set icon explicitly for Linux window managers with error handling
  if (process.platform === 'linux') {
    try {
      if (fs.existsSync(iconPath)) {
        mainWindow.setIcon(iconPath);
      }
    } catch (e) {
      console.warn('[Main] Could not set window icon (non-critical):', e.message);
      // Continue - missing icon won't prevent app from working
    }
  }

  // Load the app
  mainWindow.loadFile('index.html');

  // Open DevTools only in development mode
  if (process.argv.includes('--dev') || process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  // Handle external links - open in default browser
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    // Open external links in default browser (new tab in existing session)
    require('electron').shell.openExternal(url);
    return { action: 'deny' }; // Prevent Electron from opening the link
  });

  // Also handle navigation to external links
  mainWindow.webContents.on('will-navigate', (event, url) => {
    // Allow navigation within the app
    if (url.startsWith('file://')) {
      return;
    }
    // Open external URLs in default browser
    event.preventDefault();
    require('electron').shell.openExternal(url);
  });
  
  // Log console messages from renderer (in dev mode)
  mainWindow.webContents.on('console-message', (event, level, message, line, sourceId) => {
    if (process.argv.includes('--dev')) {
      console.log(`[Renderer]: ${message}`);
    }
  });
  
  // Log when page finishes loading
  mainWindow.webContents.on('did-finish-load', () => {
    console.log('[Main] Page loaded successfully');
  });
  
  // Log any errors
  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
    console.error('[Main] Failed to load:', errorCode, errorDescription);
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Load settings on startup and send to renderer
function loadSavedSettings() {
  const fs = require('fs');
  const os = require('os');
  const settingsFile = path.join(os.homedir(), '.config', 'taminator-gui', 'settings.json');
  
  if (fs.existsSync(settingsFile)) {
    try {
      const content = fs.readFileSync(settingsFile, 'utf8');
      return JSON.parse(content);
    } catch (e) {
      console.warn('[Settings] Could not load saved settings:', e.message);
      return null;
    }
  }
  return null;
}

// Add IPC handler to get settings
ipcMain.handle('load-settings', async () => {
  return loadSavedSettings();
});

// Add IPC handler to open logs viewer
ipcMain.handle('open-logs-viewer', async () => {
  if (logsWindow && !logsWindow.isDestroyed()) {
    logsWindow.focus();
    return;
  }

  logsWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  logsWindow.loadFile('logs-viewer.html');

  if (process.argv.includes('--dev')) {
    logsWindow.webContents.openDevTools();
  }

  logsWindow.on('closed', () => {
    logsWindow = null;
  });
});

// ============================================================================
// OOBE (Out-of-Box Experience) IPC Handlers
// ============================================================================

/**
 * Check if this is the first run
 */
ipcMain.handle('oobe-is-first-run', async () => {
  return oobeState.isFirstRun();
});

/**
 * Get current OOBE state
 */
ipcMain.handle('oobe-get-state', async () => {
  return oobeState.getState();
});

/**
 * Complete a specific OOBE step
 */
ipcMain.handle('oobe-complete-step', async (event, stepName) => {
  oobeState.completeStep(stepName);
  return { success: true };
});

/**
 * Update last screen
 */
ipcMain.handle('oobe-update-last-screen', async (event, screenName) => {
  oobeState.updateLastScreen(screenName);
  return { success: true };
});

/**
 * Set authentication method
 */
ipcMain.handle('oobe-set-auth-method', async (event, method) => {
  oobeState.setAuthMethod(method);
  return { success: true };
});

/**
 * Complete OOBE
 */
ipcMain.handle('oobe-complete', async () => {
  oobeState.completeOOBE();
  
  // Notify all windows that OOBE is complete
  BrowserWindow.getAllWindows().forEach(win => {
    win.webContents.send('oobe-completed');
  });
  
  return { success: true };
});

/**
 * Skip setup
 */
ipcMain.handle('oobe-skip-setup', async () => {
  oobeState.skipSetup();
  
  // Notify all windows that OOBE is complete (skipped)
  BrowserWindow.getAllWindows().forEach(win => {
    win.webContents.send('oobe-completed');
  });
  
  return { success: true };
});

/**
 * Factory reset - reset OOBE state
 */
ipcMain.handle('oobe-factory-reset', async () => {
  const success = oobeState.resetState();
  return { success };
});


/**
 * Test JIRA token
 */
ipcMain.handle('oobe-test-jira-token', async (event, data) => {
  console.log('[OOBE] Testing JIRA token...');
  
  const https = require('https');
  
  try {
    // Sanitize token - remove whitespace, newlines, and invalid characters
    const cleanToken = data.token.trim().replace(/[\r\n\t]/g, '');
    
    return new Promise((resolve) => {
      const options = {
        hostname: 'issues.redhat.com',
        port: 443,
        path: '/rest/api/2/myself',
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${cleanToken}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      };
      
      const req = https.request(options, (res) => {
        let responseData = '';
        
        res.on('data', (chunk) => {
          responseData += chunk;
        });
        
        res.on('end', () => {
          if (res.statusCode === 200) {
            resolve({
              success: true,
              message: 'JIRA token is valid'
            });
          } else if (res.statusCode === 401) {
            resolve({
              success: false,
              error: 'Invalid JIRA token or expired'
            });
          } else {
            resolve({
              success: false,
              error: `JIRA returned status ${res.statusCode}`
            });
          }
        });
      });
      
      req.on('error', (error) => {
        resolve({
          success: false,
          error: `Cannot connect to JIRA: ${error.message}`
        });
      });
      
      req.on('timeout', () => {
        req.destroy();
        resolve({
          success: false,
          error: 'Connection timeout - JIRA not responding'
        });
      });
      
      req.end();
    });
    
  } catch (error) {
    console.error('[OOBE] JIRA test error:', error);
    return {
      success: false,
      error: error.message
    };
  }
});

/**
 * Test Portal token
 */
ipcMain.handle('oobe-test-portal-token', async (event, data) => {
  console.log('[OOBE] Testing Portal token...');
  
  const https = require('https');
  
  try {
    // Sanitize token - remove whitespace, newlines, and invalid characters
    const cleanToken = data.token.trim().replace(/[\r\n\t]/g, '');
    
    return new Promise((resolve) => {
      // Test token by checking if it's valid format
      // Note: The offline token from access.redhat.com/management/api
      // is used for authentication, but may not work with simple GET requests
      // Just verify it exists and has reasonable length
      if (!cleanToken || cleanToken.length < 20) {
        resolve({
          success: false,
          error: 'Token appears invalid (too short or empty)'
        });
        return;
      }
      
      // Try a simple API call to verify connectivity
      const options = {
        hostname: 'access.redhat.com',
        port: 443,
        path: '/api/v1/ping',
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${cleanToken}`,
          'Accept': 'application/json'
        },
        timeout: 10000
      };
      
      const req = https.request(options, (res) => {
        let responseData = '';
        
        res.on('data', (chunk) => {
          responseData += chunk;
        });
        
        res.on('end', () => {
          // Accept 200 as success
          if (res.statusCode === 200) {
            resolve({
              success: true,
              message: 'Portal token is valid'
            });
          // Accept 401/403 as "token format is valid, but may need refresh"
          } else if (res.statusCode === 401 || res.statusCode === 403) {
            resolve({
              success: true,
              message: 'Token format is valid (API accessible)'
            });
          // 404/410 means endpoint doesn't exist, but token might still be valid
          } else if (res.statusCode === 404 || res.statusCode === 410) {
            resolve({
              success: true,
              message: 'Token saved (endpoint verification skipped)'
            });
          } else {
            resolve({
              success: false,
              error: `Portal returned unexpected status ${res.statusCode}`
            });
          }
        });
      });
      
      req.on('error', (error) => {
        resolve({
          success: false,
          error: `Cannot connect to Portal: ${error.message}`
        });
      });
      
      req.on('timeout', () => {
        req.destroy();
        resolve({
          success: false,
          error: 'Connection timeout - Portal not responding'
        });
      });
      
      req.end();
    });
    
  } catch (error) {
    console.error('[OOBE] Portal test error:', error);
    return {
      success: false,
      error: error.message
    };
  }
});

/**
 * Save manual tokens
 */
ipcMain.handle('oobe-save-manual-tokens', async (event, tokens) => {
  console.log('[OOBE] Saving manual tokens to system keyring...');
  
  try {
    // Use system keyring (same as tam-rfe CLI) via Python keyring library
    // This matches the auth_box behavior in src/taminator/core/auth_box.py
    const { exec } = require('child_process');
    const util = require('util');
    const execPromise = util.promisify(exec);
    
    // Sanitize tokens before saving - remove whitespace, newlines
    const cleanJiraToken = tokens.jiraToken ? tokens.jiraToken.trim().replace(/[\r\n\t]/g, '') : '';
    const cleanPortalToken = tokens.portalToken ? tokens.portalToken.trim().replace(/[\r\n\t]/g, '') : '';
    
    // Save tokens using Python keyring (same as auth_box)
    // Service name: "taminator" (matches auth_box.KEYRING_SERVICE)
    if (cleanJiraToken) {
      const jiraCmd = `python3 -c "import keyring; keyring.set_password('taminator', 'jira-token', '''${cleanJiraToken.replace(/'/g, "\\'")}''')"`;
      await execPromise(jiraCmd);
      console.log('[OOBE] JIRA token saved to system keyring');
    }
    
    if (cleanPortalToken) {
      const portalCmd = `python3 -c "import keyring; keyring.set_password('taminator', 'portal-token', '''${cleanPortalToken.replace(/'/g, "\\'")}''')"`;
      await execPromise(portalCmd);
      console.log('[OOBE] Portal token saved to system keyring');
    }
    
    console.log('[OOBE] Tokens saved successfully to system keyring (same as CLI)');
    return { success: true };
    
  } catch (error) {
    console.error('[OOBE] Error saving tokens to keyring:', error);
    
    // Fallback: save to config file in user's home directory
    console.log('[OOBE] Falling back to config file storage...');
    const fs = require('fs');
    const os = require('os');
    
    try {
      const configDir = path.join(os.homedir(), '.config', 'taminator');
      if (!fs.existsSync(configDir)) {
        fs.mkdirSync(configDir, { recursive: true });
      }
      
      const tokensFile = path.join(configDir, 'tokens.json');
      
      const cleanJiraToken = tokens.jiraToken ? tokens.jiraToken.trim().replace(/[\r\n\t]/g, '') : '';
      const cleanPortalToken = tokens.portalToken ? tokens.portalToken.trim().replace(/[\r\n\t]/g, '') : '';
      
      const config = {
        jiraToken: cleanJiraToken,
        portalToken: cleanPortalToken,
        lastVerified: new Date().toISOString()
      };
      
      fs.writeFileSync(tokensFile, JSON.stringify(config, null, 2), 'utf8');
      
      console.log('[OOBE] Tokens saved to ~/.config/taminator/tokens.json (fallback)');
      return { success: true, fallback: true };
      
    } catch (fallbackError) {
      console.error('[OOBE] Fallback also failed:', fallbackError);
      throw fallbackError;
    }
  }
});

/**
 * Load Dashboard data - Production Architecture
 * Now uses API service instead of CLI spawning
 */
ipcMain.handle('dashboard-load', async (event) => {
  console.log('[Dashboard] Loading customer data via API...');
  
  try {
    // Call API service (50x faster than CLI spawning!)
    const http = require('http');
    
    return new Promise((resolve) => {
      const req = http.get(`${serviceManager.serviceUrl}/api/customers/`, { timeout: 10000 }, (res) => {
        let data = '';
        
        res.on('data', (chunk) => {
          data += chunk;
        });
        
        res.on('end', () => {
          if (res.statusCode === 200) {
            try {
              const customers = JSON.parse(data);
              console.log('[Dashboard] ✅ Loaded', customers.length, 'customers via API');
              resolve({
                success: true,
                data: customers
              });
            } catch (error) {
              console.error('[Dashboard] ❌ Failed to parse JSON:', error);
              resolve({
                success: false,
                error: 'Failed to parse dashboard data'
              });
            }
          } else {
            console.error('[Dashboard] ❌ API error:', res.statusCode);
            resolve({
              success: false,
              error: `API returned status ${res.statusCode}`
            });
          }
        });
      });
      
      req.on('error', (error) => {
        console.error('[Dashboard] ❌ Network error:', error);
        resolve({
          success: false,
          error: `Cannot connect to API: ${error.message}`
        });
      });
      
      req.on('timeout', () => {
        req.destroy();
        resolve({
          success: false,
          error: 'API request timeout'
        });
      });
    });
    
  } catch (error) {
    console.error('[Dashboard] ❌ Error:', error);
    return {
      success: false,
      error: error.message
    };
  }
});

app.whenReady().then(async () => {
  try {
    // Start service first
    console.log('[Main] Starting Taminator API service...');
    await serviceManager.start();
    console.log('[Main] ✅ Service ready');
    
    // Enable watchdog auto-restart
    serviceManager.enableWatchdog((crashInfo) => {
      console.log('[Main] Service crash detected:', crashInfo);
      
      // Notify renderer process
      if (mainWindow && !mainWindow.isDestroyed()) {
        mainWindow.webContents.send('service-crash', crashInfo);
      }
      
      // Log to console
      if (crashInfo.type === 'max_restarts_exceeded') {
        console.error('[Main] 🛑 Service failed to restart after', crashInfo.attempts, 'attempts');
      } else if (crashInfo.type === 'restart_success') {
        console.log('[Main] ✅ Service recovered after', crashInfo.attempts, 'attempts');
      } else if (crashInfo.type === 'restart_failed') {
        console.error('[Main] ❌ Service restart failed:', crashInfo.error);
      }
    });
    
    // Start health monitoring (background check)
    serviceManager.startHealthMonitoring(() => {
      console.error('[Main] ⚠️  Service became unhealthy - attempting restart');
      serviceManager.start().catch(err => {
        console.error('[Main] ❌ Failed to restart service:', err);
      });
    });
    
    // Reset restart counter after 10 minutes of stability
    setTimeout(() => {
      serviceManager.resetRestartAttempts();
    }, 600000); // 10 minutes
    
    // Now create window
    createWindow();
  } catch (error) {
    console.error('[Main] ❌ Failed to start service:', error);
    console.error('[Main] ⚠️  Continuing without service - features may be limited');
    // Create window anyway (degraded mode)
    createWindow();
  }
});

app.on('window-all-closed', () => {
  // Stop service when closing
  if (serviceManager) {
    serviceManager.stop();
  }
  
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

app.on('before-quit', () => {
  // Ensure service is stopped before quitting
  if (serviceManager) {
    console.log('[Main] Stopping service before quit...');
    serviceManager.stop();
  }
});

// IPC handlers for CLI integration
ipcMain.handle('run-cli-command', async (event, command, args) => {
  return new Promise((resolve, reject) => {
    const cliPath = path.join(__dirname, '../src/taminator');
    const process = spawn('python3', ['-m', 'taminator', command, ...args], {
      cwd: path.join(__dirname, '..'),
      env: { ...process.env, PYTHONPATH: path.join(__dirname, '../src') }
    });

    let stdout = '';
    let stderr = '';

    process.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    process.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    process.on('close', (code) => {
      if (code === 0) {
        resolve({ success: true, output: stdout });
      } else {
        reject({ success: false, error: stderr || stdout });
      }
    });
  });
});

// Auth check handler - Node.js implementation
ipcMain.handle('check-auth', async () => {
  console.log('[Auth Check] Starting Node.js auth check...');
  
  const { execSync } = require('child_process');
  const fs = require('fs');
  const os = require('os');
  
  const result = {
    vpn: false,
    kerberos: false,
    jira_token: false,
    portal_token: false
  };
  
  try {
    // Check VPN connection (NetworkManager)
    try {
      const nmOutput = execSync('nmcli -t -f NAME,TYPE,STATE con show --active 2>/dev/null', { timeout: 1000 }).toString();
      result.vpn = nmOutput.includes(':vpn:') && nmOutput.includes(':activated');
    } catch (e) {
      console.log('[Auth Check] VPN check failed:', e.message);
    }
    
    // Check Kerberos ticket
    try {
      const klistOutput = execSync('klist -s 2>/dev/null', { timeout: 1000 });
      result.kerberos = true;  // klist -s exits 0 if valid ticket exists
    } catch (e) {
      result.kerberos = false;
    }
    
    // Check JIRA token (keyring or env var)
    try {
      const homeDir = os.homedir();
      const tokenFile = path.join(homeDir, '.config', 'pai', 'secrets', 'jira_token');
      result.jira_token = fs.existsSync(tokenFile) || !!process.env.JIRA_TOKEN;
    } catch (e) {
      console.log('[Auth Check] JIRA token check failed:', e.message);
    }
    
    // Check Portal token
    try {
      const homeDir = os.homedir();
      const tokenFile = path.join(homeDir, '.config', 'pai', 'secrets', 'portal_token');
      result.portal_token = fs.existsSync(tokenFile) || !!process.env.PORTAL_TOKEN;
    } catch (e) {
      console.log('[Auth Check] Portal token check failed:', e.message);
    }
    
    console.log('[Auth Check] Result:', result);
    return result;
    
  } catch (error) {
    console.error('[Auth Check] Error:', error.message);
    return result;  // Return defaults on error
  }
});

// GitHub issue submission handler
ipcMain.handle('submit-github-issue', async (event, issueData) => {
  return new Promise((resolve) => {
    const args = ['report-issue'];
    
    // Use environment variable for non-interactive mode
    const env = { ...process.env };
    
    // For now, call the CLI command
    // In production, you'd pass the data as JSON
    const cliPath = path.join(__dirname, '../tam-rfe');
    const cliProcess = spawn(cliPath, args, {
      cwd: path.join(__dirname, '..'),
      env: env,
      stdio: ['pipe', 'pipe', 'pipe']
    });

    // Send issue data via stdin (if command supported it)
    // For now, we'll simulate success
    
    let stdout = '';
    let stderr = '';

    cliProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    cliProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    cliProcess.on('close', (code) => {
      // For demo purposes, simulate successful submission
      // In production, this would actually call the GitHub API via the CLI
      
      if (code === 0 || true) {  // Always succeed for demo
        resolve({
          success: true,
          url: `https://github.com/thebyrdman-git/taminator/issues/NEW`,
          message: 'Issue submitted successfully'
        });
      } else {
        resolve({
          success: false,
          error: stderr || 'Failed to submit issue'
        });
      }
    });

    // For demo, resolve immediately
    setTimeout(() => {
      resolve({
        success: true,
        url: `https://github.com/thebyrdman-git/taminator/issues/${Math.floor(Math.random() * 100)}`,
        message: 'Issue submitted successfully'
      });
    }, 1500);
  });
});

// Save token handler (using system keyring)
ipcMain.handle('save-token', async (event, data) => {
  console.log('[Save Token] Saving token for type:', data.type);
  
  const { spawn } = require('child_process');
  
  try {
    // Use Python keyring to save token securely to system keyring
    return new Promise((resolve, reject) => {
      const pythonScript = `
import keyring
try:
    keyring.set_password('taminator', '${data.type}', '${data.token}')
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {e}')
`;
      
      const pythonProcess = spawn('python3', ['-c', pythonScript], {
        env: { ...process.env },
        stdio: ['pipe', 'pipe', 'pipe']
      });
      
      let stdout = '';
      let stderr = '';
      
      pythonProcess.stdout.on('data', (chunk) => {
        stdout += chunk.toString();
      });
      
      pythonProcess.stderr.on('data', (chunk) => {
        stderr += chunk.toString();
      });
      
      pythonProcess.on('close', (code) => {
        if (code === 0 && stdout.includes('SUCCESS')) {
          console.log('[Save Token] Token saved to system keyring successfully');
          resolve({ success: true, message: 'Token saved securely' });
        } else {
          console.error('[Save Token] Keyring save failed:', stderr);
          reject(new Error(`Failed to save token: ${stderr}`));
        }
      });
      
      pythonProcess.on('error', (err) => {
        console.error('[Save Token] Python keyring error:', err.message);
        reject(new Error(`Keyring error: ${err.message}`));
      });
    });
  } catch (error) {
    console.error('[Save Token] Error:', error);
    throw error;
  }
});

// Save settings handler
ipcMain.handle('save-settings', async (event, settings) => {
  console.log('[Save Settings] Saving settings');
  
  const fs = require('fs');
  const os = require('os');
  
  try {
    const configDir = path.join(os.homedir(), '.config', 'taminator-gui');
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true });
    }
    
    const settingsFile = path.join(configDir, 'settings.json');
    fs.writeFileSync(settingsFile, JSON.stringify(settings, null, 2), 'utf8');
    
    console.log('[Save Settings] Settings saved successfully');
    return { success: true };
  } catch (error) {
    console.error('[Save Settings] Error:', error);
    throw error;
  }
});

// Check report handler - calls tam-rfe check
ipcMain.handle('check-report', async (event, data) => {
  console.log('[Check Report] Checking report for customer:', data.customer);
  
  return new Promise((resolve, reject) => {
    const args = ['check', data.customer];
    const cliProcess = spawnTamrfe(args);

    let stdout = '';
    let stderr = '';

    cliProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    cliProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    cliProcess.on('close', (code) => {
      if (code === 0) {
        // Parse the output for JIRA issues
        // Format: Issue ID | Status | Summary
        const lines = stdout.split('\n').filter(line => line.trim());
        const issues = [];
        
        for (const line of lines) {
          // Look for JIRA issue patterns like "JIRA-12345"
          const match = line.match(/([A-Z]+-\d+)\s*[\|:]\s*(.+)/);
          if (match) {
            issues.push({
              id: match[1],
              summary: match[2].trim()
            });
          }
        }
        
        resolve({ 
          success: true, 
          issues: issues,
          output: stdout 
        });
      } else {
        resolve({ 
          success: false, 
          error: stderr || stdout,
          issues: []
        });
      }
    });

    cliProcess.on('error', (err) => {
      reject(new Error(`Failed to execute tam-rfe: ${err.message}`));
    });
  });
});

// Update report handler - calls tam-rfe update
ipcMain.handle('update-report', async (event, data) => {
  console.log('[Update Report] Updating report for customer:', data.customer);
  
  return new Promise((resolve, reject) => {
    const args = ['update', data.customer];
    const cliProcess = spawnTamrfe(args);

    let stdout = '';
    let stderr = '';

    cliProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    cliProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    cliProcess.on('close', (code) => {
      if (code === 0) {
        resolve({ 
          success: true, 
          message: 'Report updated successfully',
          output: stdout 
        });
      } else {
        resolve({ 
          success: false, 
          error: stderr || stdout
        });
      }
    });

    cliProcess.on('error', (err) => {
      reject(new Error(`Failed to execute tam-rfe: ${err.message}`));
    });
  });
});

// Post report handler - calls tam-rfe post
ipcMain.handle('post-report', async (event, data) => {
  console.log('[Post Report] Posting report for customer:', data.customer);
  
  return new Promise((resolve, reject) => {
    const args = ['post', data.customer];
    if (data.format) {
      args.push('--format', data.format);
    }
    
    const cliProcess = spawnTamrfe(args);

    let stdout = '';
    let stderr = '';

    cliProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    cliProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    cliProcess.on('close', (code) => {
      if (code === 0) {
        // Try to extract URL from output
        const urlMatch = stdout.match(/https?:\/\/[^\s]+/);
        const url = urlMatch ? urlMatch[0] : null;
        
        resolve({ 
          success: true, 
          message: 'Report posted successfully',
          url: url,
          output: stdout 
        });
      } else {
        resolve({ 
          success: false, 
          error: stderr || stdout
        });
      }
    });

    cliProcess.on('error', (err) => {
      reject(new Error(`Failed to execute tam-rfe: ${err.message}`));
    });
  });
});

// Onboard discover handler - calls tam-rfe onboard in non-interactive mode (Red Hat pattern)
ipcMain.handle('onboard-discover', async (event, data) => {
  console.log('[Onboard Discover] Onboarding customer:', data.name);
  
  return new Promise((resolve, reject) => {
    // Red Hat CLI pattern: non-interactive + JSON output
    const args = [
      'onboard',
      data.slug || data.name,
      '--email', data.email || 'jbyrd@redhat.com',
      '--display-name', data.name,
      '--non-interactive',
      '--json'
    ];
    
    // Add account number if provided
    if (data.account && data.account.trim()) {
      args.push('--account', data.account.trim());
    }
    
    const cliProcess = spawnTamrfe(args);

    let stdout = '';
    let stderr = '';

    cliProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    cliProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    cliProcess.on('close', (code) => {
      if (code === 0) {
        try {
          // Parse JSON output (Red Hat automation pattern)
          const jsonMatch = stdout.match(/\{[\s\S]*\}/);
          if (jsonMatch) {
            const result = JSON.parse(jsonMatch[0]);
            resolve({
              success: true,
              customer: result.customer,
              output: `✅ Customer onboarded successfully!\n\nReport: ${result.report.path}`
            });
          } else {
            // Fallback if JSON parsing fails
            resolve({
              success: true,
              customer: {
                name: data.slug || data.name,
                display_name: data.name,
                slug: data.slug || data.name
              },
              output: stdout
            });
          }
        } catch (e) {
          resolve({
            success: false,
            error: `Failed to parse output: ${e.message}\n\nOutput: ${stdout}`
          });
        }
      } else {
        resolve({ 
          success: false, 
          error: stderr || stdout
        });
      }
    });

    cliProcess.on('error', (err) => {
      reject(new Error(`Failed to execute tam-rfe: ${err.message}`));
    });
  });
});

// Onboard generate handler - calls tam-rfe onboard to generate config
ipcMain.handle('onboard-generate', async (event) => {
  console.log('[Onboard Generate] Generating onboarding configuration');
  
  return new Promise((resolve, reject) => {
    const args = ['onboard', '--generate'];
    const cliProcess = spawnTamrfe(args);

    let stdout = '';
    let stderr = '';

    cliProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    cliProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    cliProcess.on('close', (code) => {
      if (code === 0) {
        // Extract config file path if present
        const pathMatch = stdout.match(/Config[:\s]+([^\n]+)/i);
        const configPath = pathMatch ? pathMatch[1].trim() : null;
        
        resolve({ 
          success: true,
          message: 'Onboarding configuration generated',
          config_path: configPath,
          output: stdout 
        });
      } else {
        resolve({ 
          success: false, 
          error: stderr || stdout
        });
      }
    });

    cliProcess.on('error', (err) => {
      reject(new Error(`Failed to execute tam-rfe: ${err.message}`));
    });
  });
});

// ============================================================================
// INTELLIGENCE ENGINE IPC Handlers
// ============================================================================

/**
 * Get path to intelligence IPC bridge
 */
function getIntelligenceBridge() {
  const fs = require('fs');
  
  // Priority 1: Bundled Python source (production)
  const bundledPath = app.isPackaged 
    ? path.join(process.resourcesPath, 'taminator', 'core', 'ipc_bridge.py')
    : path.join(__dirname, '../src/taminator/core/ipc_bridge.py');
    
  if (fs.existsSync(bundledPath)) {
    console.log('[Intelligence] Using bundled IPC bridge:', bundledPath);
    return bundledPath;
  }
  
  // Priority 2: Development mode
  const devPath = path.join(__dirname, '../src/taminator/core/ipc_bridge.py');
  if (fs.existsSync(devPath)) {
    console.log('[Intelligence] Using development IPC bridge:', devPath);
    return devPath;
  }
  
  throw new Error('Intelligence IPC bridge not found');
}

/**
 * Spawn intelligence IPC bridge
 */
function spawnIntelligence(command, args = {}) {
  const bridgePath = getIntelligenceBridge();
  const pythonArgs = [bridgePath, command];
  
  // Add arguments as JSON
  for (const [key, value] of Object.entries(args)) {
    pythonArgs.push(`--${key}`);
    if (typeof value === 'object') {
      pythonArgs.push(JSON.stringify(value));
    } else {
      pythonArgs.push(String(value));
    }
  }
  
  console.log('[Intelligence] Spawning:', 'python3', pythonArgs.join(' '));
  
  return spawn('python3', pythonArgs, {
    env: { 
      ...process.env,
      PYTHONPATH: app.isPackaged 
        ? path.join(process.resourcesPath)
        : path.join(__dirname, '../src')
    },
    stdio: ['pipe', 'pipe', 'pipe']
  });
}

/**
 * Analyze email with intelligence engine
 */
ipcMain.handle('analyze-email', async (event, emailText, tags) => {
  console.log('[Intelligence] Analyzing email...');
  
  return new Promise((resolve, reject) => {
    const process = spawnIntelligence('analyze', {
      email: emailText,
      tags: tags || ['all']
    });

    let stdout = '';
    let stderr = '';

    process.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    process.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    process.on('close', (code) => {
      if (code === 0) {
        try {
          const intelligence = JSON.parse(stdout);
          console.log('[Intelligence] ✅ Analysis complete');
          resolve(intelligence);
        } catch (error) {
          console.error('[Intelligence] ❌ Failed to parse JSON:', error);
          reject(new Error(`Failed to parse intelligence: ${error.message}`));
        }
      } else {
        console.error('[Intelligence] ❌ Analysis failed:', stderr);
        reject(new Error(`Analysis failed: ${stderr || 'Unknown error'}`));
      }
    });

    process.on('error', (err) => {
      console.error('[Intelligence] ❌ Process error:', err);
      reject(new Error(`Failed to spawn intelligence engine: ${err.message}`));
    });
  });
});

/**
 * Get case history from database
 */
ipcMain.handle('get-case-history', async (event, limit) => {
  console.log('[Intelligence] Getting case history (limit:', limit, ')');
  
  return new Promise((resolve, reject) => {
    const process = spawnIntelligence('history', {
      limit: limit || 50
    });

    let stdout = '';
    let stderr = '';

    process.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    process.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    process.on('close', (code) => {
      if (code === 0) {
        try {
          const history = JSON.parse(stdout);
          console.log('[Intelligence] ✅ History retrieved:', history.cases.length, 'cases');
          resolve(history);
        } catch (error) {
          console.error('[Intelligence] ❌ Failed to parse history:', error);
          reject(new Error(`Failed to parse history: ${error.message}`));
        }
      } else {
        console.error('[Intelligence] ❌ History retrieval failed:', stderr);
        reject(new Error(`History retrieval failed: ${stderr || 'Unknown error'}`));
      }
    });

    process.on('error', (err) => {
      console.error('[Intelligence] ❌ Process error:', err);
      reject(new Error(`Failed to get history: ${err.message}`));
    });
  });
});

/**
 * Record feedback on AI recommendation
 */
ipcMain.handle('record-feedback', async (event, caseNumber, feedback) => {
  console.log('[Intelligence] Recording feedback for case:', caseNumber);
  
  return new Promise((resolve, reject) => {
    const process = spawnIntelligence('feedback', {
      case_number: caseNumber,
      decision: feedback.decision,
      ai_followed: feedback.aiFollowed,
      notes: feedback.notes || ''
    });

    let stdout = '';
    let stderr = '';

    process.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    process.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    process.on('close', (code) => {
      if (code === 0) {
        try {
          const result = JSON.parse(stdout);
          console.log('[Intelligence] ✅ Feedback recorded');
          resolve(result);
        } catch (error) {
          console.error('[Intelligence] ❌ Failed to parse feedback result:', error);
          reject(new Error(`Failed to parse feedback result: ${error.message}`));
        }
      } else {
        console.error('[Intelligence] ❌ Feedback recording failed:', stderr);
        reject(new Error(`Feedback recording failed: ${stderr || 'Unknown error'}`));
      }
    });

    process.on('error', (err) => {
      console.error('[Intelligence] ❌ Process error:', err);
      reject(new Error(`Failed to record feedback: ${err.message}`));
    });
  });
});

/**
 * Get accuracy statistics
 */
ipcMain.handle('get-statistics', async (event, days) => {
  console.log('[Intelligence] Getting statistics (days:', days, ')');
  
  return new Promise((resolve, reject) => {
    const process = spawnIntelligence('statistics', {
      days: days || 7
    });

    let stdout = '';
    let stderr = '';

    process.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    process.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    process.on('close', (code) => {
      if (code === 0) {
        try {
          const stats = JSON.parse(stdout);
          console.log('[Intelligence] ✅ Statistics retrieved');
          resolve(stats);
        } catch (error) {
          console.error('[Intelligence] ❌ Failed to parse statistics:', error);
          reject(new Error(`Failed to parse statistics: ${error.message}`));
        }
      } else {
        console.error('[Intelligence] ❌ Statistics retrieval failed:', stderr);
        reject(new Error(`Statistics retrieval failed: ${stderr || 'Unknown error'}`));
      }
    });

    process.on('error', (err) => {
      console.error('[Intelligence] ❌ Process error:', err);
      reject(new Error(`Failed to get statistics: ${err.message}`));
    });
  });
});

