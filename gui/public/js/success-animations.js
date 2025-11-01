/**
 * Success Animations
 * Celebrate successful operations with visual feedback
 */

class SuccessAnimator {
  constructor() {
    this.confettiActive = false;
    console.log('[SuccessAnimator] Initialized');
  }

  /**
   * Show success checkmark animation
   * @param {string} containerId - Container to show animation in
   * @param {string} message - Success message
   * @param {number} duration - How long to show (ms)
   */
  showCheckmark(containerId, message = 'Success!', duration = 2000) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const animationHTML = `
      <div class="success-animation" style="text-align: center; padding: 40px;">
        <div class="success-checkmark">
          <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
            <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
            <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
          </svg>
        </div>
        <h3 style="margin: 16px 0 8px; color: #3E8635; font-size: 20px;">${message}</h3>
      </div>
    `;

    container.innerHTML = animationHTML;

    // Auto-hide after duration
    if (duration > 0) {
      setTimeout(() => {
        const animation = container.querySelector('.success-animation');
        if (animation) {
          animation.style.opacity = '0';
          animation.style.transform = 'scale(0.9)';
          setTimeout(() => animation.remove(), 300);
        }
      }, duration);
    }
  }

  /**
   * Show confetti celebration
   * @param {number} duration - How long confetti falls (ms)
   */
  showConfetti(duration = 3000) {
    if (this.confettiActive) return;
    this.confettiActive = true;

    const confettiContainer = document.createElement('div');
    confettiContainer.id = 'confetti-container';
    confettiContainer.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 9999;
      overflow: hidden;
    `;

    document.body.appendChild(confettiContainer);

    // Generate confetti pieces
    const colors = ['#EE0000', '#0066CC', '#F0AB00', '#3E8635', '#FF6B6B', '#FFD700'];
    const confettiCount = 50;

    for (let i = 0; i < confettiCount; i++) {
      const confetti = document.createElement('div');
      confetti.className = 'confetti-piece';
      confetti.style.cssText = `
        position: absolute;
        width: 10px;
        height: 10px;
        background-color: ${colors[Math.floor(Math.random() * colors.length)]};
        top: -10px;
        left: ${Math.random() * 100}%;
        opacity: ${0.7 + Math.random() * 0.3};
        transform: rotate(${Math.random() * 360}deg);
        animation: confetti-fall ${2 + Math.random() * 3}s linear forwards;
      `;
      confettiContainer.appendChild(confetti);
    }

    // Remove after duration
    setTimeout(() => {
      confettiContainer.style.opacity = '0';
      setTimeout(() => {
        confettiContainer.remove();
        this.confettiActive = false;
      }, 500);
    }, duration);
  }

  /**
   * Show pulse animation (subtle success indicator)
   * @param {string} elementId - Element to pulse
   */
  pulse(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    element.style.animation = 'success-pulse 0.6s ease-out';

    setTimeout(() => {
      element.style.animation = '';
    }, 600);
  }

  /**
   * Show success toast with animation
   * @param {string} message - Success message
   * @param {boolean} withConfetti - Show confetti effect
   */
  showSuccess(message, withConfetti = false) {
    // Use existing toast system
    if (window.errorHandler) {
      window.errorHandler.showSuccess(message, 5000);
    }

    // Optional confetti for major wins
    if (withConfetti) {
      this.showConfetti(3000);
    }
  }

  /**
   * Flash element green briefly (for updates)
   * @param {string} elementId - Element to flash
   */
  flashSuccess(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const originalBg = element.style.backgroundColor;
    element.style.transition = 'background-color 0.3s';
    element.style.backgroundColor = '#E7F5E7';

    setTimeout(() => {
      element.style.backgroundColor = originalBg;
      setTimeout(() => {
        element.style.transition = '';
      }, 300);
    }, 600);
  }
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
  /* Success Checkmark Animation */
  .success-animation {
    animation: success-fade-in 0.5s ease-out;
  }

  .success-checkmark {
    width: 80px;
    height: 80px;
    margin: 0 auto 16px;
    border-radius: 50%;
    display: block;
    stroke-width: 2;
    stroke: #3E8635;
    stroke-miterlimit: 10;
    box-shadow: inset 0 0 0 #3E8635;
    animation: success-scale 0.3s ease-in-out 0.9s both;
  }

  .checkmark {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: block;
    stroke-width: 3;
    stroke: #fff;
    stroke-miterlimit: 10;
    margin: 10% auto;
    box-shadow: inset 0px 0px 0px #3E8635;
    animation: checkmark-fill 0.4s ease-in-out 0.4s forwards, checkmark-scale 0.3s ease-in-out 0.9s both;
  }

  .checkmark-circle {
    stroke-dasharray: 166;
    stroke-dashoffset: 166;
    stroke-width: 2;
    stroke-miterlimit: 10;
    stroke: #3E8635;
    fill: none;
    animation: checkmark-stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
  }

  .checkmark-check {
    transform-origin: 50% 50%;
    stroke-dasharray: 48;
    stroke-dashoffset: 48;
    stroke: #3E8635;
    animation: checkmark-stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
  }

  @keyframes checkmark-stroke {
    100% {
      stroke-dashoffset: 0;
    }
  }

  @keyframes checkmark-scale {
    0%, 100% {
      transform: none;
    }
    50% {
      transform: scale3d(1.1, 1.1, 1);
    }
  }

  @keyframes checkmark-fill {
    100% {
      box-shadow: inset 0px 0px 0px 30px #3E8635;
    }
  }

  @keyframes success-fade-in {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes success-pulse {
    0%, 100% {
      transform: scale(1);
      box-shadow: 0 0 0 0 rgba(62, 134, 53, 0.7);
    }
    50% {
      transform: scale(1.05);
      box-shadow: 0 0 0 10px rgba(62, 134, 53, 0);
    }
  }

  /* Confetti Animation */
  @keyframes confetti-fall {
    to {
      transform: translateY(100vh) rotate(720deg);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);

// Global singleton
window.successAnimator = new SuccessAnimator();

console.log('✅ Success animations initialized');

