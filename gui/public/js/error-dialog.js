/**
 * Error Dialog System with Copy/Paste for Bug Reports
 *
 * Provides user-friendly error dialogs with:
 * - Clear error messages
 * - Technical details (collapsible)
 * - Copy to clipboard button
 * - Direct link to GitLab issues
 */

class ErrorDialog {
  constructor() {
    this.dialogContainer = null;
    this.init();
  }

  init() {
    // Create dialog container if it doesn't exist
    if (!document.getElementById('error-dialog-container')) {
      this.dialogContainer = document.createElement('div');
      this.dialogContainer.id = 'error-dialog-container';
      this.dialogContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: none;
        justify-content: center;
        align-items: center;
        z-index: 10000;
      `;
      document.body.appendChild(this.dialogContainer);
    }
  }

  /**
   * Show error dialog
   * @param {Object} options - Error dialog options
   * @param {string} options.title - Error title
   * @param {string} options.message - User-friendly error message
   * @param {string} options.technicalDetails - Technical error details
   * @param {string} options.stack - Stack trace (optional)
   * @param {string} options.context - Additional context (optional)
   */
  show(options) {
    const {
      title = 'Error',
      message = 'An unexpected error occurred',
      technicalDetails = '',
      stack = '',
      context = ''
    } = options;

    // Build error report for copy/paste
    const errorReport = this._buildErrorReport({
      title,
      message,
      technicalDetails,
      stack,
      context
    });

    // Create dialog HTML
    const dialogHTML = `
      <div style="
        background: white;
        border-radius: 8px;
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
      ">
        <!-- Header -->
        <div style="
          background: #c9190b;
          color: white;
          padding: 16px 20px;
          display: flex;
          align-items: center;
          gap: 12px;
        ">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
          </svg>
          <h3 style="margin: 0; font-size: 18px; font-weight: 600;">${this._escapeHtml(title)}</h3>
        </div>

        <!-- Content -->
        <div style="
          padding: 20px;
          overflow-y: auto;
          flex: 1;
        ">
          <!-- User-friendly message -->
          <p style="margin: 0 0 16px 0; font-size: 14px; line-height: 1.5;">
            ${this._escapeHtml(message)}
          </p>

          <!-- Technical details (collapsible) -->
          ${technicalDetails || stack ? `
            <details style="margin-bottom: 16px;">
              <summary style="
                cursor: pointer;
                font-weight: 600;
                font-size: 13px;
                color: #06c;
                padding: 8px 0;
                user-select: none;
              ">
                Technical Details (click to expand)
              </summary>
              <div style="
                background: #f5f5f5;
                border: 1px solid #d2d2d2;
                border-radius: 4px;
                padding: 12px;
                margin-top: 8px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                overflow-x: auto;
                white-space: pre-wrap;
                word-break: break-all;
              ">${this._escapeHtml(technicalDetails || stack)}</div>
            </details>
          ` : ''}

          <!-- Error report preview -->
          <div style="
            background: #f5f5f5;
            border: 1px solid #d2d2d2;
            border-radius: 4px;
            padding: 12px;
            margin-bottom: 16px;
          ">
            <div style="
              font-weight: 600;
              font-size: 13px;
              margin-bottom: 8px;
              color: #151515;
            ">Error Report (ready to copy):</div>
            <textarea id="error-report-text" readonly style="
              width: 100%;
              height: 120px;
              font-family: 'Courier New', monospace;
              font-size: 11px;
              border: none;
              background: white;
              padding: 8px;
              border-radius: 3px;
              resize: vertical;
            ">${errorReport}</textarea>
          </div>

          <!-- Help text -->
          <p style="
            font-size: 12px;
            color: #6a6e73;
            margin: 0;
            line-height: 1.5;
          ">
            📋 Click "Copy Error Report" below, then paste it into a 
            <a href="https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues/new" target="_blank" style="color: #06c;">GitLab issue</a>.
          </p>
        </div>

        <!-- Footer -->
        <div style="
          padding: 16px 20px;
          border-top: 1px solid #d2d2d2;
          display: flex;
          gap: 12px;
          justify-content: flex-end;
        ">
          <button id="error-dialog-copy-btn" style="
            background: #06c;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
          ">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
              <path d="M4 2h8a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V4a2 2 0 012-2zm0 1a1 1 0 00-1 1v8a1 1 0 001 1h8a1 1 0 001-1V4a1 1 0 00-1-1H4z"/>
              <path d="M6 0h6a2 2 0 012 2v6h-1V2a1 1 0 00-1-1H6V0z"/>
            </svg>
            Copy Error Report
          </button>
          <button id="error-dialog-close-btn" style="
            background: #f0f0f0;
            color: #151515;
            border: 1px solid #d2d2d2;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
          ">
            Close
          </button>
        </div>
      </div>
    `;

    this.dialogContainer.innerHTML = dialogHTML;
    this.dialogContainer.style.display = 'flex';

    // Add event listeners
    document.getElementById('error-dialog-copy-btn').addEventListener('click', () => {
      this._copyToClipboard(errorReport);
    });

    document.getElementById('error-dialog-close-btn').addEventListener('click', () => {
      this.close();
    });

    // Close on background click
    this.dialogContainer.addEventListener('click', (e) => {
      if (e.target === this.dialogContainer) {
        this.close();
      }
    });

    // Close on Escape key
    const escapeHandler = (e) => {
      if (e.key === 'Escape') {
        this.close();
        document.removeEventListener('keydown', escapeHandler);
      }
    };
    document.addEventListener('keydown', escapeHandler);
  }

  close() {
    if (this.dialogContainer) {
      this.dialogContainer.style.display = 'none';
      this.dialogContainer.innerHTML = '';
    }
  }

  async _buildErrorReport(options) {
    const {
      title,
      message,
      technicalDetails,
      stack,
      context
    } = options;

    const timestamp = new Date().toISOString();
    const userAgent = navigator.userAgent;

    // Get version dynamically from IPC
    let taminatorVersion = '2.0.0';
    try {
      if (typeof ipcRenderer !== 'undefined') {
        taminatorVersion = await ipcRenderer.invoke('get-version');
      }
    } catch (error) {
      console.warn('[ErrorDialog] Could not get version:', error);
    }

    let report = `# Taminator Error Report

**Timestamp:** ${timestamp}
**Version:** ${taminatorVersion}
**User Agent:** ${userAgent}

## Error

**Title:** ${title}
**Message:** ${message}

`;

    if (technicalDetails) {
      report += `## Technical Details

\`\`\`
${technicalDetails}
\`\`\`

`;
    }

    if (stack) {
      report += `## Stack Trace

\`\`\`
${stack}
\`\`\`

`;
    }

    if (context) {
      report += `## Additional Context

${context}

`;
    }

    report += `## Steps to Reproduce

1. [Describe what you were doing when the error occurred]
2. [Add any additional steps]

## Expected Behavior

[Describe what you expected to happen]

## Actual Behavior

[Describe what actually happened]

---
*This error report was automatically generated by Taminator.*
`;

    return report;
  }

  _copyToClipboard(text) {
    const textarea = document.getElementById('error-report-text');
    textarea.select();

    try {
      document.execCommand('copy');

      // Show success feedback
      const copyBtn = document.getElementById('error-dialog-copy-btn');
      const originalText = copyBtn.innerHTML;
      copyBtn.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
          <path d="M13.78 4.22a.75.75 0 010 1.06l-7.25 7.25a.75.75 0 01-1.06 0L2.22 9.28a.75.75 0 011.06-1.06L6 10.94l6.72-6.72a.75.75 0 011.06 0z"/>
        </svg>
        Copied!
      `;
      copyBtn.style.background = '#3e8635';

      setTimeout(() => {
        copyBtn.innerHTML = originalText;
        copyBtn.style.background = '#06c';
      }, 2000);

    } catch (err) {
      console.error('Failed to copy:', err);
      alert('Failed to copy. Please select and copy manually.');
    }
  }

  _escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Global error dialog instance
window.errorDialog = new ErrorDialog();

// Override console.error to show dialog for critical errors (production mode only)
const isDevelopment = window.location.href.includes('--dev') ||
                      (typeof process !== 'undefined' && process.env.NODE_ENV === 'development');

if (!isDevelopment) {
  const originalConsoleError = console.error;
  console.error = function(...args) {
    originalConsoleError.apply(console, args);

    // Only show dialog for actual Error objects with critical severity
    const firstArg = args[0];

    // Don't show dialog for certain non-critical errors
    const ignoredErrors = [
      'Autofill.enable',
      'Autofill.setAddresses',
      'Content-Security-Policy',
      '[Warning]',
      '[Info]'
    ];

    const isCriticalError = firstArg instanceof Error ||
                           (typeof firstArg === 'string' &&
                            (firstArg.includes('[CRITICAL]') || firstArg.includes('[FATAL]')));

    if (isCriticalError && !ignoredErrors.some(ignored =>
      (firstArg.message || firstArg).includes(ignored))) {

      const errorMessage = firstArg instanceof Error ? firstArg.message : firstArg;
      const errorStack = firstArg instanceof Error ? firstArg.stack : '';

      window.errorDialog.show({
        title: 'Critical Error',
        message: errorMessage,
        technicalDetails: errorStack,
        context: `Arguments: ${JSON.stringify(args, null, 2)}`
      });
    }
  };

  console.log('[ErrorDialog] Production mode - critical errors will show dialog');
} else {
  console.log('[ErrorDialog] Development mode - error dialogs disabled');
}

console.log('[ErrorDialog] ✅ Error dialog system initialized with copy/paste support');

