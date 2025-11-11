/**
 * Google OAuth Handler for Electron Desktop App
 *
 * Flow:
 * 1. User clicks "Sign In with Google" in Electron app
 * 2. Electron calls API to get OAuth URL
 * 3. Electron opens browser tab with OAuth URL
 * 4. User authenticates in browser (opens Google login page)
 * 5. Browser redirects to localhost callback
 * 6. API receives callback and stores token
 * 7. Electron polls for completion
 * 8. User returns to desktop app (authenticated!)
 */

const { shell } = require('electron');

class GoogleAuthHandler {
    constructor(apiClient) {
        this.api = apiClient;
        this.pollInterval = null;
    }

    /**
     * Start Google Sign-In flow
     *
     * Opens browser for authentication, then polls for completion
     */
    async signIn() {
        console.log('🔐 Starting Google Sign-In...');

        try {
            // Step 1: Get OAuth URL from API
            const response = await this.api.request('/api/google/auth/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ port: 8080 })
            });

            const authUrl = response.auth_url;
            console.log(`🌐 Opening browser: ${authUrl}`);

            // Step 2: Open browser for user to authenticate
            shell.openExternal(authUrl);

            // Step 3: Show waiting message in app
            this.showAuthWaiting();

            // Step 4: Poll API for completion
            await this.pollForCompletion();

            console.log('✅ Google Sign-In complete!');
            return true;

        } catch (error) {
            console.error('❌ Sign-In failed:', error);
            this.showAuthError(error.message);
            return false;
        }
    }

    /**
     * Poll API until authentication is complete
     */
    async pollForCompletion() {
        return new Promise((resolve, reject) => {
            let attempts = 0;
            const maxAttempts = 60; // 2 minutes (60 * 2 seconds)

            this.pollInterval = setInterval(async () => {
                attempts++;

                try {
                    // Check if user is now authenticated
                    const status = await this.api.request('/api/google/status');

                    if (status.authenticated) {
                        // Success! User is authenticated
                        clearInterval(this.pollInterval);
                        this.showAuthSuccess(status);
                        resolve(status);
                    } else if (attempts >= maxAttempts) {
                        // Timeout
                        clearInterval(this.pollInterval);
                        reject(new Error('Authentication timeout. Please try again.'));
                    }

                } catch (error) {
                    console.error('Poll error:', error);
                    // Continue polling (might be temporary network issue)
                }

            }, 2000); // Poll every 2 seconds
        });
    }

    /**
     * Cancel authentication flow
     */
    cancelSignIn() {
        if (this.pollInterval) {
            clearInterval(this.pollInterval);
            this.pollInterval = null;
        }
        console.log('❌ Sign-In cancelled');
    }

    /**
     * Sign out (revoke Google access)
     */
    async signOut() {
        console.log('🚪 Signing out from Google...');

        try {
            await this.api.request('/api/google/auth/revoke', {
                method: 'POST'
            });

            console.log('✅ Signed out successfully');
            this.showSignOutSuccess();
            return true;

        } catch (error) {
            console.error('❌ Sign-Out failed:', error);
            this.showSignOutError(error.message);
            return false;
        }
    }

    /**
     * Check current authentication status
     */
    async checkStatus() {
        try {
            const status = await this.api.request('/api/google/status');
            return status;
        } catch (error) {
            console.error('❌ Status check failed:', error);
            return { authenticated: false };
        }
    }

    /**
     * UI Helpers
     */

    showAuthWaiting() {
        const modal = document.getElementById('auth-modal');
        if (modal) {
            modal.innerHTML = `
                <div class="modal-content">
                    <h2>🔐 Authenticating with Google</h2>
                    <div class="spinner"></div>
                    <p>Please complete authentication in your browser.</p>
                    <p style="color: #999; font-size: 14px;">
                        A browser tab has opened for you to sign in with your @redhat.com account.
                    </p>
                    <button onclick="googleAuth.cancelSignIn()" class="secondary">
                        Cancel
                    </button>
                </div>
            `;
            modal.style.display = 'flex';
        }
    }

    showAuthSuccess(status) {
        const modal = document.getElementById('auth-modal');
        if (modal) {
            modal.innerHTML = `
                <div class="modal-content">
                    <h2>✅ Authentication Successful!</h2>
                    <p>Signed in as: <strong>${status.user_email}</strong></p>
                    <p style="color: #4caf50;">You can now close this window and return to Taminator.</p>
                    <button onclick="closeAuthModal()">Continue</button>
                </div>
            `;

            // Auto-close after 3 seconds
            setTimeout(() => {
                this.closeModal();
                // Refresh UI to show authenticated state
                window.location.reload();
            }, 3000);
        }
    }

    showAuthError(message) {
        const modal = document.getElementById('auth-modal');
        if (modal) {
            modal.innerHTML = `
                <div class="modal-content">
                    <h2>❌ Authentication Failed</h2>
                    <p style="color: #f44336;">${message}</p>
                    <p>Please try again or contact support if the problem persists.</p>
                    <button onclick="closeAuthModal()">Close</button>
                </div>
            `;
        }
    }

    showSignOutSuccess() {
        alert('✅ Signed out successfully');
    }

    showSignOutError(message) {
        alert(`❌ Sign-Out failed: ${message}`);
    }

    closeModal() {
        const modal = document.getElementById('auth-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    }
}

// Global instance
let googleAuth = null;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // TaminatorAPI is loaded from api-client.js
    /* global TaminatorAPI */
    const api = new TaminatorAPI();
    googleAuth = new GoogleAuthHandler(api);

    // Add global functions for UI
    window.googleAuth = googleAuth;
    window.closeAuthModal = () => googleAuth.closeModal();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GoogleAuthHandler;
}

