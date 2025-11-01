/**
 * Service Manager - Auto-start/stop Taminator API Service
 * 
 * Production-grade service lifecycle management:
 * - Auto-starts service when GUI launches
 * - Health checks before declaring ready
 * - Auto-stops service when GUI closes
 * - Handles errors gracefully
 */

const { spawn } = require('child_process');
const http = require('http');
const path = require('path');
const { app } = require('electron');

class ServiceManager {
  constructor() {
    this.serviceProcess = null;
    this.serviceUrl = 'http://127.0.0.1:8765';
    this.maxStartupTime = 30000; // 30 seconds
    this.healthCheckInterval = null;
    
    // Watchdog configuration
    this.watchdogEnabled = true;
    this.restartAttempts = 0;
    this.maxRestartAttempts = 5;
    this.restartWindow = 300000; // 5 minutes
    this.lastRestartTime = null;
    this.onCrashCallback = null;
  }

  /**
   * Start the API service
   * Returns a promise that resolves when service is healthy
   */
  async start() {
    console.log('[ServiceManager] Starting Taminator API service...');

    // Check if already running
    if (await this.isHealthy()) {
      console.log('[ServiceManager] ✅ Service already running');
      return true;
    }

    // Get service binary path
    const servicePath = this._getServicePath();
    console.log('[ServiceManager] Service path:', servicePath);

    // Spawn service process
    this.serviceProcess = spawn(servicePath, ['--port', '8765'], {
      stdio: ['ignore', 'pipe', 'pipe'],
      detached: false,
      env: { ...process.env }
    });

    // Log service output (for debugging)
    this.serviceProcess.stdout.on('data', (data) => {
      console.log('[Service]', data.toString().trim());
    });

    this.serviceProcess.stderr.on('data', (data) => {
      console.error('[Service Error]', data.toString().trim());
    });

    this.serviceProcess.on('error', (error) => {
      console.error('[ServiceManager] ❌ Failed to start service:', error);
    });

    this.serviceProcess.on('exit', (code, signal) => {
      console.log(`[ServiceManager] Service exited (code: ${code}, signal: ${signal})`);
      this.serviceProcess = null;
      
      // Watchdog: Auto-restart on unexpected exit
      if (this.watchdogEnabled && code !== 0 && code !== null) {
        this._handleCrash(code, signal);
      }
    });

    // Wait for service to become healthy
    try {
      await this.waitForHealthy(this.maxStartupTime);
      console.log('[ServiceManager] ✅ Service started successfully');
      return true;
    } catch (error) {
      console.error('[ServiceManager] ❌ Service failed to start:', error);
      this.stop();
      throw error;
    }
  }

  /**
   * Stop the API service
   */
  stop() {
    console.log('[ServiceManager] Stopping service...');

    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
      this.healthCheckInterval = null;
    }

    if (this.serviceProcess) {
      try {
        this.serviceProcess.kill('SIGTERM');
        console.log('[ServiceManager] ✅ Service stopped');
      } catch (error) {
        console.error('[ServiceManager] ⚠️  Error stopping service:', error);
      }
      this.serviceProcess = null;
    }
  }

  /**
   * Check if service is healthy
   * Returns a promise that resolves to true if healthy, false otherwise
   * 
   * Uses /health/live for fast startup checks (no expensive AI/rhcase checks)
   */
  isHealthy() {
    return new Promise((resolve) => {
      const req = http.get(`${this.serviceUrl}/health/live`, { timeout: 1000 }, (res) => {
        let data = '';
        res.on('data', (chunk) => { data += chunk; });
        res.on('end', () => {
          try {
            const health = JSON.parse(data);
            resolve(health.status === 'alive');
          } catch {
            resolve(false);
          }
        });
      });

      req.on('error', () => resolve(false));
      req.on('timeout', () => {
        req.destroy();
        resolve(false);
      });
    });
  }

  /**
   * Wait for service to become healthy
   * Polls health endpoint until success or timeout
   */
  async waitForHealthy(timeout = 30000) {
    const startTime = Date.now();
    const pollInterval = 500; // Check every 500ms

    while (Date.now() - startTime < timeout) {
      if (await this.isHealthy()) {
        return true;
      }

      // Wait before next check
      await new Promise(resolve => setTimeout(resolve, pollInterval));
    }

    throw new Error('Service failed to become healthy within timeout');
  }

  /**
   * Get service binary path
   * Checks multiple locations for the service executable
   */
  _getServicePath() {
    const fs = require('fs');

    // Priority 1: Bundled PyInstaller binary (production)
    const bundledPath = app.isPackaged
      ? path.join(process.resourcesPath, 'bin', 'taminator-service')
      : path.join(__dirname, '../dist/taminator-service');

    if (fs.existsSync(bundledPath)) {
      return bundledPath;
    }

    // Priority 2: Development mode (shell script)
    const devPath = path.join(__dirname, '../bin/taminator-service');
    if (fs.existsSync(devPath)) {
      return devPath;
    }

    // Priority 3: System PATH (fallback)
    return 'taminator-service';
  }

  /**
   * Get service health status
   * Returns health data or null if unhealthy
   */
  async getHealth() {
    return new Promise((resolve) => {
      const req = http.get(`${this.serviceUrl}/health`, { timeout: 2000 }, (res) => {
        let data = '';
        res.on('data', (chunk) => { data += chunk; });
        res.on('end', () => {
          try {
            resolve(JSON.parse(data));
          } catch {
            resolve(null);
          }
        });
      });

      req.on('error', () => resolve(null));
      req.on('timeout', () => {
        req.destroy();
        resolve(null);
      });
    });
  }

  /**
   * Start health monitoring
   * Periodically checks if service is still running
   */
  startHealthMonitoring(onUnhealthy) {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
    }

    let lastCheckTime = 0;
    const debounceMs = 2000; // Minimum 2 seconds between checks

    this.healthCheckInterval = setInterval(async () => {
      const now = Date.now();
      
      // Debounce: Skip if last check was too recent
      if (now - lastCheckTime < debounceMs) {
        return;
      }
      
      lastCheckTime = now;
      const healthy = await this.isHealthy();
      
      if (!healthy && onUnhealthy) {
        console.log('[ServiceManager] ⚠️  Service became unhealthy');
        onUnhealthy();
      }
    }, 10000); // Check every 10 seconds
  }

  /**
   * Handle service crash (watchdog)
   * Attempts to auto-restart with exponential backoff
   */
  async _handleCrash(exitCode, signal) {
    console.log('[ServiceManager] 🔄 Service crashed, attempting auto-restart...');

    // Reset restart counter if outside restart window
    const now = Date.now();
    if (this.lastRestartTime && (now - this.lastRestartTime) > this.restartWindow) {
      console.log('[ServiceManager] Reset restart counter (window expired)');
      this.restartAttempts = 0;
    }

    // Check if we should restart
    if (!this._shouldRestart()) {
      console.error('[ServiceManager] 🛑 Max restart attempts reached. Service will not auto-restart.');
      
      // Notify user
      if (this.onCrashCallback) {
        this.onCrashCallback({
          type: 'max_restarts_exceeded',
          exitCode,
          signal,
          attempts: this.restartAttempts
        });
      }
      
      return;
    }

    // Increment restart counter
    this.restartAttempts++;
    this.lastRestartTime = now;

    // Exponential backoff: 2s, 4s, 8s, 16s, 32s
    const backoffDelay = Math.min(Math.pow(2, this.restartAttempts) * 1000, 32000);
    console.log(`[ServiceManager] Waiting ${backoffDelay/1000}s before restart (attempt ${this.restartAttempts}/${this.maxRestartAttempts})`);

    // Wait before restarting
    await new Promise(resolve => setTimeout(resolve, backoffDelay));

    // Attempt restart
    try {
      console.log(`[ServiceManager] Restart attempt ${this.restartAttempts}/${this.maxRestartAttempts}`);
      await this.start();
      
      console.log('[ServiceManager] ✅ Service restarted successfully');
      
      // Notify user of successful recovery
      if (this.onCrashCallback) {
        this.onCrashCallback({
          type: 'restart_success',
          attempts: this.restartAttempts
        });
      }
      
    } catch (error) {
      console.error('[ServiceManager] ❌ Restart failed:', error);
      
      // Exponential backoff for retry attempts
      const backoffDelay = Math.min(
        1000 * Math.pow(2, this.restartAttempts) + Math.random() * 1000,
        30000 // Max 30 seconds
      );
      
      console.log(`[ServiceManager] ⏱️ Waiting ${Math.round(backoffDelay/1000)}s before next attempt...`);
      
      // Wait before notifying (allows for retry)
      setTimeout(() => {
        // Notify user of failed restart
        if (this.onCrashCallback) {
          this.onCrashCallback({
            type: 'restart_failed',
            error: error.message,
            attempts: this.restartAttempts,
            maxAttempts: this.maxRestartAttempts,
            nextRetryIn: backoffDelay
          });
        }
      }, backoffDelay);
    }
  }

  /**
   * Check if service should be restarted
   * Returns false if max attempts exceeded
   */
  _shouldRestart() {
    return this.restartAttempts < this.maxRestartAttempts;
  }

  /**
   * Enable watchdog auto-restart
   */
  enableWatchdog(onCrash = null) {
    this.watchdogEnabled = true;
    this.onCrashCallback = onCrash;
    console.log('[ServiceManager] 🐕 Watchdog enabled');
  }

  /**
   * Disable watchdog auto-restart
   */
  disableWatchdog() {
    this.watchdogEnabled = false;
    this.onCrashCallback = null;
    console.log('[ServiceManager] Watchdog disabled');
  }

  /**
   * Reset restart attempt counter
   * Call this after successful long-running period
   */
  resetRestartAttempts() {
    this.restartAttempts = 0;
    this.lastRestartTime = null;
    console.log('[ServiceManager] Restart counter reset');
  }

  /**
   * Get watchdog status
   */
  getWatchdogStatus() {
    return {
      enabled: this.watchdogEnabled,
      restartAttempts: this.restartAttempts,
      maxRestartAttempts: this.maxRestartAttempts,
      lastRestartTime: this.lastRestartTime
    };
  }
}

module.exports = { ServiceManager };

