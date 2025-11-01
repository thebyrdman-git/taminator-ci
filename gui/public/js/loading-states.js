/**
 * Loading States System
 * Professional loading indicators for async operations
 */

class LoadingStateManager {
  constructor() {
    this.activeLoaders = new Map();
    console.log('[LoadingStates] Initialized');
  }

  /**
   * Show loading spinner in a container
   *
   * @param {string} containerId - Element ID to show spinner in
   * @param {string} message - Loading message
   * @param {string} size - 'small', 'medium', 'large'
   */
  show(containerId, message = 'Loading...', size = 'medium') {
    const container = document.getElementById(containerId);
    if (!container) {
      console.warn(`[LoadingStates] Container not found: ${containerId}`);
      // Clean up tracking if container missing
      this.activeLoaders.delete(containerId);
      return;
    }

    const loaderId = `loader-${containerId}-${Date.now()}`;

    const sizeClass = {
      small: 'loader-small',
      medium: 'loader-medium',
      large: 'loader-large'
    }[size] || 'loader-medium';

    const loaderHTML = `
      <div id="${loaderId}" class="loading-overlay">
        <div class="loading-content">
          <div class="spinner ${sizeClass}"></div>
          <div class="loading-message">${message}</div>
        </div>
      </div>
    `;

    container.style.position = 'relative';
    container.insertAdjacentHTML('beforeend', loaderHTML);

    this.activeLoaders.set(containerId, loaderId);

    return loaderId;
  }

  /**
   * Show inline loading (for buttons, small areas)
   */
  showInline(containerId, message = 'Loading...') {
    const container = document.getElementById(containerId);
    if (!container) return;

    const loaderId = `loader-inline-${containerId}-${Date.now()}`;

    const loaderHTML = `
      <span id="${loaderId}" class="loading-inline">
        <span class="spinner-small"></span>
        <span>${message}</span>
      </span>
    `;

    container.innerHTML = loaderHTML;
    this.activeLoaders.set(containerId, loaderId);

    return loaderId;
  }

  /**
   * Show progress bar
   */
  showProgress(containerId, message = 'Processing...', progress = 0) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const loaderId = `loader-progress-${containerId}-${Date.now()}`;

    const loaderHTML = `
      <div id="${loaderId}" class="loading-progress">
        <div class="progress-message">${message}</div>
        <div class="progress-bar-container">
          <div class="progress-bar" style="width: ${progress}%"></div>
        </div>
        <div class="progress-percent">${progress}%</div>
      </div>
    `;

    container.innerHTML = loaderHTML;
    this.activeLoaders.set(containerId, loaderId);

    return loaderId;
  }

  /**
   * Update progress bar
   */
  updateProgress(containerId, progress, message = null) {
    const loaderId = this.activeLoaders.get(containerId);
    if (!loaderId) return;

    const loader = document.getElementById(loaderId);
    if (!loader) return;

    const progressBar = loader.querySelector('.progress-bar');
    const progressPercent = loader.querySelector('.progress-percent');

    if (progressBar) {
      progressBar.style.width = `${progress}%`;
    }

    if (progressPercent) {
      progressPercent.textContent = `${progress}%`;
    }

    if (message) {
      const progressMessage = loader.querySelector('.progress-message');
      if (progressMessage) {
        progressMessage.textContent = message;
      }
    }
  }

  /**
   * Hide loading indicator
   */
  hide(containerId) {
    const loaderId = this.activeLoaders.get(containerId);
    if (!loaderId) {
      // Clean up tracking even if loader not found
      this.activeLoaders.delete(containerId);
      return;
    }

    const loader = document.getElementById(loaderId);
    if (loader) {
      // Fade out
      loader.style.opacity = '0';
      setTimeout(() => {
        try {
          if (loader.parentNode) {
            loader.parentNode.removeChild(loader);
          }
        } catch (error) {
          console.warn('[LoadingStates] Failed to remove loader from DOM:', error);
        }
      }, 300);
    }

    // Always clean up tracking
    this.activeLoaders.delete(containerId);
  }

  /**
   * Hide all active loaders
   */
  hideAll() {
    this.activeLoaders.forEach((loaderId, containerId) => {
      this.hide(containerId);
    });
  }

  /**
   * Wrap async function with automatic loading state
   */
  async wrap(containerId, asyncFn, message = 'Loading...') {
    this.show(containerId, message);
    try {
      const result = await asyncFn();
      return result;
    } finally {
      this.hide(containerId);
    }
  }

  /**
   * Wrap async function with progress tracking
   */
  async wrapWithProgress(containerId, asyncFn, message = 'Processing...') {
    this.showProgress(containerId, message, 0);

    try {
      // Create progress callback
      const updateProgress = (progress, msg) => {
        this.updateProgress(containerId, progress, msg);
      };

      const result = await asyncFn(updateProgress);

      // Show 100% briefly
      this.updateProgress(containerId, 100, 'Complete!');
      await new Promise(resolve => {
        setTimeout(() => resolve(), 500);
      });

      return result;
    } finally {
      this.hide(containerId);
    }
  }
}

// Global singleton
window.loadingStates = new LoadingStateManager();

console.log('✅ Loading states system initialized');

