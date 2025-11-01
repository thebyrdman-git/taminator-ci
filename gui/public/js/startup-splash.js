/**
 * Startup Splash Screen - Professional Loading Experience
 * 
 * Shows during service startup with animated progress
 */

class StartupSplash {
    constructor() {
        this.splash = null;
        this.progressBar = null;
        this.statusText = null;
        this.shown = false;
    }

    show() {
        if (this.shown) return;

        // Create splash overlay
        this.splash = document.createElement('div');
        this.splash.id = 'startup-splash';
        this.splash.innerHTML = `
            <div class="splash-content">
                <div class="splash-icon">
                    🤖
                </div>
                <h1 class="splash-title">Taminator</h1>
                <p class="splash-subtitle">v2.0 - AI-Augmented TAM Assistant</p>
                
                <div class="splash-progress">
                    <div class="splash-progress-bar" id="splash-progress-bar"></div>
                </div>
                
                <p class="splash-status" id="splash-status">Starting service...</p>
            </div>
        `;

        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            #startup-splash {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, #151515 0%, #2a2a2a 100%);
                z-index: 100000;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: fadeIn 0.3s ease;
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }

            .splash-content {
                text-align: center;
                max-width: 400px;
                padding: 48px;
            }

            .splash-icon {
                font-size: 80px;
                margin-bottom: 24px;
                animation: pulse 2s ease-in-out infinite;
            }

            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }

            .splash-title {
                font-size: 48px;
                font-weight: 700;
                color: #EE0000;
                margin: 0 0 12px 0;
                font-family: 'Red Hat Display', sans-serif;
                letter-spacing: -1px;
            }

            .splash-subtitle {
                font-size: 18px;
                color: #999;
                margin: 0 0 48px 0;
                font-weight: 400;
            }

            .splash-progress {
                width: 100%;
                height: 4px;
                background: rgba(255,255,255,0.1);
                border-radius: 2px;
                overflow: hidden;
                margin-bottom: 24px;
            }

            .splash-progress-bar {
                height: 100%;
                background: linear-gradient(90deg, #EE0000 0%, #FF6B6B 100%);
                width: 0%;
                transition: width 0.3s ease;
                animation: shimmer 2s ease-in-out infinite;
            }

            @keyframes shimmer {
                0% { opacity: 1; }
                50% { opacity: 0.7; }
                100% { opacity: 1; }
            }

            .splash-status {
                font-size: 14px;
                color: #666;
                margin: 0;
                min-height: 20px;
            }

            #startup-splash.hide {
                animation: fadeOut 0.5s ease forwards;
            }
        `;
        document.head.appendChild(style);

        // Add to DOM
        document.body.appendChild(this.splash);

        // Get references
        this.progressBar = document.getElementById('splash-progress-bar');
        this.statusText = document.getElementById('splash-status');

        this.shown = true;

        // Start progress simulation
        this.simulateProgress();
    }

    updateStatus(message) {
        if (this.statusText) {
            this.statusText.textContent = message;
        }
    }

    updateProgress(percent) {
        if (this.progressBar) {
            this.progressBar.style.width = `${percent}%`;
        }
    }

    simulateProgress() {
        let progress = 0;
        const steps = [
            { progress: 20, message: 'Loading configuration...', delay: 300 },
            { progress: 40, message: 'Starting API service...', delay: 800 },
            { progress: 60, message: 'Checking health...', delay: 1200 },
            { progress: 80, message: 'Initializing UI...', delay: 1500 },
            { progress: 95, message: 'Almost ready...', delay: 2000 }
        ];

        steps.forEach(step => {
            setTimeout(() => {
                this.updateProgress(step.progress);
                this.updateStatus(step.message);
            }, step.delay);
        });
    }

    hide() {
        if (!this.splash) return;

        // Animate out
        this.splash.classList.add('hide');

        // Remove after animation
        setTimeout(() => {
            if (this.splash && this.splash.parentNode) {
                this.splash.parentNode.removeChild(this.splash);
            }
            this.shown = false;
        }, 500);
    }
}

// Global instance
window.startupSplash = new StartupSplash();

