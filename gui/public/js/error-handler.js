/**
 * Global Error Handler
 *
 * Professional features:
 * - Toast notifications for user feedback
 * - Error classification (retryable vs fatal)
 * - Automatic retry for network errors
 * - User-friendly error messages
 * - Debug info logging
 */

class ErrorHandler {
    constructor() {
        this.toastContainer = null;
        this.activeToasts = new Map();
        this.retryQueue = new Map();
        this.maxRetries = 3;

        this._initToastContainer();
        this._initGlobalHandlers();

        console.log('✅ ErrorHandler initialized');
    }

    /**
     * Create toast container on page load
     */
    _initToastContainer() {
        this.toastContainer = document.createElement('div');
        this.toastContainer.id = 'toast-container';
        this.toastContainer.className = 'toast-container';
        document.body.appendChild(this.toastContainer);
    }

    /**
     * Set up global error handlers
     */
    _initGlobalHandlers() {
        // Catch unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            this.showError('An unexpected error occurred', event.reason);
            event.preventDefault();
        });

        // Catch JavaScript errors
        window.addEventListener('error', (event) => {
            console.error('JavaScript error:', event.error);
            this.showError('Application error', event.error?.message);
            event.preventDefault();
        });
    }

    /**
     * Show success toast
     */
    showSuccess(message, duration = 3000) {
        this._showToast(message, 'success', '✅', duration);
    }

    /**
     * Show info toast
     */
    showInfo(message, duration = 5000) {
        this._showToast(message, 'info', 'ℹ️', duration);
    }

    /**
     * Show warning toast
     */
    showWarning(message, duration = 5000) {
        this._showToast(message, 'warning', '⚠️', duration);
    }

    /**
     * Show error toast with help link and retry option
     */
    showError(message, details = null, helpLink = null, retryCallback = null) {
        const toast = this._showToast(
            message,
            'error',
            '❌',
            0,  // Don't auto-dismiss errors
            helpLink,
            retryCallback
        );

        // Log details for debugging
        if (details) {
            console.error('Error details:', details);
        }

        return toast;
    }

    /**
     * Show warning toast with help link
     */
    showWarningWithHelp(message, duration, helpLink) {
        return this._showToast(message, 'warning', '⚠️', duration, helpLink);
    }

    /**
     * Handle API error response (user-friendly with actionable help)
     */
    handleApiError(error, retryCallback = null) {
        console.error('API Error:', error);

        // Parse error from API client
        let message = 'An error occurred';
        let helpLink = null;
        let canRetry = false;

        if (error.error_code) {
            // Structured Taminator error
            message = error.message || message;
            canRetry = this._isRetryable(error.error_code);

            // Show specific error UI based on code
            switch (error.error_code) {
                case 'auth_token_missing':
                    message = `🔐 ${error.details?.token_type || 'Authentication'} not configured`;
                    helpLink = { text: 'Configure in Settings', action: () => this._openSettings() };
                    this.showWarning(message, 10000, helpLink);
                    return;

                case 'auth_token_expired':
                case 'auth_token_invalid':
                    message = `🔐 ${error.details?.token_type || 'Token'} expired or invalid`;
                    helpLink = { text: 'Update in Settings', action: () => this._openSettings() };
                    this.showError(message, error.details, helpLink);
                    return;

                case 'jira_auth_failed':
                    message = '🎫 JIRA authentication failed';
                    helpLink = { text: 'Check Token', action: () => this._openSettings('jira') };
                    this.showError(message, error.details, helpLink);
                    return;

                case 'portal_auth_failed':
                    message = '📰 Customer Portal authentication failed';
                    helpLink = { text: 'Check Token', action: () => this._openSettings('portal') };
                    this.showError(message, error.details, helpLink);
                    return;

                case 'jira_connection_error':
                case 'jira_network_error':
                    message = '🎫 Cannot connect to JIRA. Check VPN connection.';
                    helpLink = { text: 'Troubleshoot', action: () => this._openTroubleshoot('vpn') };
                    canRetry = true;
                    break;

                case 'portal_network_error':
                    message = '📰 Cannot connect to Customer Portal. Check VPN connection.';
                    helpLink = { text: 'Troubleshoot', action: () => this._openTroubleshoot('vpn') };
                    canRetry = true;
                    break;

                case 'jira_rate_limit':
                case 'portal_rate_limit': {
                    const retryAfter = error.retry_after || 60;
                    message = `⏱️ API rate limit reached. Retry in ${retryAfter}s`;
                    this.showWarning(message, retryAfter * 1000);

                    // Auto-retry after wait period
                    if (retryCallback) {
                        setTimeout(() => {
                            console.log('Auto-retrying after rate limit...');
                            retryCallback();
                        }, retryAfter * 1000);
                    }
                    return;
                }

                case 'service_unavailable':
                    message = '🔧 Service temporarily unavailable. Restarting...';
                    this.showWarning(message, 5000);
                    canRetry = true;
                    break;

                case 'network_error':
                    message = '📡 Network error. Check your internet connection.';
                    helpLink = { text: 'Troubleshoot', action: () => this._openTroubleshoot('network') };
                    canRetry = true;
                    break;

                case 'customer_not_found':
                    message = `📁 Customer not found: ${error.details?.customer_id}`;
                    helpLink = { text: 'View Customers', action: () => this._openCustomers() };
                    this.showError(message, error.details, helpLink);
                    return;

                default:
                    // Use error message from API
                    message = error.message || 'An unexpected error occurred';
            }
        } else if (error.message) {
            // Generic error
            message = error.message;
        }

        // Show error with retry option
        if (canRetry && retryCallback) {
            this.showError(message, error, helpLink, retryCallback);
        } else {
            this.showError(message, error, helpLink);
        }
    }

    /**
     * Check if error code is retryable
     */
    _isRetryable(errorCode) {
        const retryableCodes = [
            'NETWORK_ERROR',
            'SERVICE_UNAVAILABLE',
            'EXTERNAL_API_TIMEOUT',
            'EXTERNAL_API_ERROR'  // Some external API errors are transient
        ];
        return retryableCodes.includes(errorCode);
    }

    /**
     * Show token setup prompt
     */
    _promptTokenSetup(tokenType) {
        // Open settings and focus on token section
        this._openSettings(tokenType.toLowerCase());

        // Show helpful modal
        const modal = document.createElement('div');
        modal.className = 'token-setup-modal-overlay';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10001;
        `;

        modal.innerHTML = `
            <div class="token-setup-modal" style="background: white; padding: 30px; border-radius: 8px; max-width: 500px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
                <div class="modal-header" style="margin-bottom: 20px;">
                    <h3 style="margin: 0; display: flex; align-items: center; gap: 10px;">
                        <span>🔐</span>
                        <span>${tokenType} Token Required</span>
                    </h3>
                    <button class="modal-close" style="position: absolute; top: 10px; right: 10px; background: none; border: none; font-size: 24px; cursor: pointer; color: #999;">&times;</button>
                </div>
                <div class="modal-content" style="margin-bottom: 20px; line-height: 1.6;">
                    <p>To use ${tokenType} features, you need to configure your API token.</p>
                    
                    <h4 style="margin-top: 20px; margin-bottom: 10px;">Steps:</h4>
                    <ol style="padding-left: 20px;">
                        <li>Visit <a href="https://access.redhat.com/management/api" target="_blank" style="color: #EE0000;">Red Hat API Management</a></li>
                        <li>Click "Generate Token"</li>
                        <li>Copy the token</li>
                        <li>Paste it in Settings → Authentication</li>
                    </ol>
                </div>
                <div class="modal-footer" style="display: flex; gap: 10px; justify-content: flex-end;">
                    <button class="btn-cancel" style="padding: 10px 20px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">
                        Later
                    </button>
                    <button class="btn-get-token" style="padding: 10px 20px; background: #EE0000; color: white; border: none; border-radius: 4px; cursor: pointer;">
                        Get Token
                    </button>
                </div>
            </div>
        `;

        // Event listeners
        const closeModal = () => modal.remove();
        modal.querySelector('.modal-close').onclick = closeModal;
        modal.querySelector('.btn-cancel').onclick = closeModal;
        modal.onclick = (e) => { if (e.target === modal) closeModal(); };

        modal.querySelector('.btn-get-token').onclick = () => {
            window.open('https://access.redhat.com/management/api', '_blank');
            closeModal();
        };

        document.body.appendChild(modal);
    }

    /**
     * Create and show toast notification
     */
    _showToast(message, type, icon, duration = 5000, helpLink = null, retryCallback = null) {
        const toastId = `toast-${Date.now()}`;

        const toast = document.createElement('div');
        toast.id = toastId;
        toast.className = `toast toast-${type}`;

        // Toast content
        const content = document.createElement('div');
        content.className = 'toast-content';

        const iconSpan = document.createElement('span');
        iconSpan.className = 'toast-icon';
        iconSpan.textContent = icon;

        const messageSpan = document.createElement('span');
        messageSpan.className = 'toast-message';
        messageSpan.textContent = message;

        content.appendChild(iconSpan);
        content.appendChild(messageSpan);

        // Actions
        const actions = document.createElement('div');
        actions.className = 'toast-actions';

        // Help link button (if provided)
        if (helpLink && helpLink.text && helpLink.action) {
            const helpBtn = document.createElement('button');
            helpBtn.className = 'toast-btn toast-btn-help';
            helpBtn.textContent = `💡 ${helpLink.text}`;
            helpBtn.onclick = () => {
                this._removeToast(toastId);
                helpLink.action();
            };
            actions.appendChild(helpBtn);
        }

        // Retry button (for errors with retry callback)
        if (retryCallback) {
            const retryBtn = document.createElement('button');
            retryBtn.className = 'toast-btn toast-btn-retry';
            retryBtn.textContent = '🔄 Retry';
            retryBtn.onclick = () => {
                this._removeToast(toastId);
                retryCallback();
            };
            actions.appendChild(retryBtn);
        }

        // Dismiss button
        const dismissBtn = document.createElement('button');
        dismissBtn.className = 'toast-btn toast-btn-dismiss';
        dismissBtn.textContent = '×';
        dismissBtn.onclick = () => this._removeToast(toastId);
        actions.appendChild(dismissBtn);

        toast.appendChild(content);
        toast.appendChild(actions);

        // Add to container
        this.toastContainer.appendChild(toast);
        this.activeToasts.set(toastId, toast);

        // Animate in
        setTimeout(() => toast.classList.add('toast-show'), 10);

        // Auto-dismiss after duration (if set)
        if (duration > 0) {
            setTimeout(() => this._removeToast(toastId), duration);
        }

        return toastId;
    }

    /**
     * Remove toast notification
     */
    _removeToast(toastId) {
        const toast = this.activeToasts.get(toastId);
        if (!toast) return;

        // Animate out
        toast.classList.remove('toast-show');
        toast.classList.add('toast-hide');

        // Remove from DOM
        setTimeout(() => {
            try {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            } catch (error) {
                console.warn('[ErrorHandler] Failed to remove toast from DOM:', error);
            } finally {
                // ALWAYS clean up Map entry, even if DOM removal failed
                this.activeToasts.delete(toastId);
            }
        }, 300);
    }

    /**
     * Clear all toasts
     */
    clearAll() {
        this.activeToasts.forEach((toast, toastId) => {
            this._removeToast(toastId);
        });
    }

    /**
     * Wrap async function with automatic error handling
     */
    async wrap(asyncFn, _errorMessage = 'Operation failed') {
        try {
            return await asyncFn();
        } catch (error) {
            this.handleApiError(error);
            throw error;
        }
    }

    /**
     * Wrap async function with retry logic
     */
    async wrapWithRetry(asyncFn, maxRetries = 3, _errorMessage = 'Operation failed') {
        let lastError;

        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                return await asyncFn();
            } catch (error) {
                lastError = error;

                if (attempt < maxRetries && this._isRetryable(error.error_code)) {
                    console.log(`Attempt ${attempt} failed, retrying...`);
                    this.showInfo(`Retrying... (${attempt}/${maxRetries})`, 2000);

                    // Exponential backoff
                    await new Promise(resolve => {
                        setTimeout(() => resolve(), Math.pow(2, attempt) * 1000);
                    });
                } else {
                    break;
                }
            }
        }

        // All retries exhausted
        this.handleApiError(lastError);
        throw lastError;
    }

    /**
     * Navigation helpers (link to help/settings)
     */
    _openSettings(section = null) {
        console.log(`Opening settings${section ? ` (${section})` : ''}`);

        // Navigate to settings page
        if (typeof window.showAuthManagement === 'function') {
            window.showAuthManagement();

            // Scroll to specific section if provided
            if (section) {
                setTimeout(() => {
                    const element = document.getElementById(`${section}-section`);
                    if (element) {
                        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        element.style.animation = 'highlight-flash 2s';
                    }
                }, 500);
            }
        }
    }

    _openCustomers() {
        console.log('Opening customers page');
        if (typeof window.showCustomers === 'function') {
            window.showCustomers();
        }
    }

    _openTroubleshoot(topic = null) {
        console.log(`Opening troubleshooting${topic ? ` (${topic})` : ''}`);

        // Show help modal with troubleshooting guide
        const troubleshootGuides = {
            vpn: {
                title: 'VPN Connection Issues',
                steps: [
                    '1. Verify VPN is connected',
                    '2. Check Red Hat VPN client status',
                    '3. Try disconnecting and reconnecting',
                    '4. Verify network routes: ip route show',
                    '5. Test connectivity: ping issues.redhat.com'
                ],
                links: [
                    { text: 'Red Hat VPN Guide', url: 'https://mojo.redhat.com/docs/DOC-1234567' }
                ]
            },
            network: {
                title: 'Network Connection Issues',
                steps: [
                    '1. Check internet connection',
                    '2. Verify DNS resolution: dig redhat.com',
                    '3. Check firewall settings',
                    '4. Try restarting network: sudo systemctl restart NetworkManager'
                ],
                links: []
            }
        };

        const guide = troubleshootGuides[topic] || {
            title: 'Troubleshooting',
            steps: ['Check service logs', 'Restart the application', 'Contact support'],
            links: []
        };

        this._showTroubleshootModal(guide);
    }

    _showTroubleshootModal(guide) {
        // Create modal overlay
        const modal = document.createElement('div');
        modal.className = 'troubleshoot-modal-overlay';
        modal.innerHTML = `
            <div class="troubleshoot-modal">
                <div class="troubleshoot-header">
                    <h3>${guide.title}</h3>
                    <button class="modal-close">×</button>
                </div>
                <div class="troubleshoot-content">
                    <h4>Troubleshooting Steps:</h4>
                    <ul>
                        ${guide.steps.map(step => `<li>${step}</li>`).join('')}
                    </ul>
                    ${guide.links.length > 0 ? `
                        <h4>Additional Resources:</h4>
                        <ul>
                            ${guide.links.map(link =>
                                `<li><a href="${link.url}" target="_blank">${link.text}</a></li>`
                            ).join('')}
                        </ul>
                    ` : ''}
                </div>
                <div class="troubleshoot-footer">
                    <button class="btn btn-primary" onclick="this.closest('.troubleshoot-modal-overlay').remove()">
                        Got it
                    </button>
                </div>
            </div>
        `;

        // Add close handlers
        modal.querySelector('.modal-close').onclick = () => modal.remove();
        modal.onclick = (e) => {
            if (e.target === modal) modal.remove();
        };

        // Add to page
        document.body.appendChild(modal);
    }
}

// Global singleton
window.errorHandler = new ErrorHandler();

console.log('✅ Global error handler initialized');

