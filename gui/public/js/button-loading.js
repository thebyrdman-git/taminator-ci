/**
 * Button Loading States
 * Show spinners in buttons during async operations
 */

/**
 * Set button to loading state
 * @param {string|HTMLElement} button - Button ID or element
 * @param {string} loadingText - Optional text to show while loading
 */
function setButtonLoading(button, loadingText = null) {
  const btn = typeof button === 'string' ? document.getElementById(button) : button;
  if (!btn) return;

  // Save original content
  if (!btn.dataset.originalContent) {
    btn.dataset.originalContent = btn.innerHTML;
  }

  // Add loading class
  btn.classList.add('loading');
  btn.disabled = true;

  // Update text if provided
  if (loadingText) {
    btn.innerHTML = loadingText;
  }
}

/**
 * Remove loading state from button
 * @param {string|HTMLElement} button - Button ID or element
 */
function clearButtonLoading(button) {
  const btn = typeof button === 'string' ? document.getElementById(button) : button;
  if (!btn) return;

  // Remove loading class
  btn.classList.remove('loading');
  btn.disabled = false;

  // Restore original content
  if (btn.dataset.originalContent) {
    btn.innerHTML = btn.dataset.originalContent;
    delete btn.dataset.originalContent;
  }
}

/**
 * Wrap async function with automatic button loading state
 * @param {HTMLElement} button - Button element
 * @param {Function} asyncFn - Async function to execute
 * @param {string} loadingText - Optional loading text
 */
async function withButtonLoading(button, asyncFn, loadingText = null) {
  setButtonLoading(button, loadingText);
  try {
    const result = await asyncFn();
    return result;
  } finally {
    clearButtonLoading(button);
  }
}

// Make globally available
window.setButtonLoading = setButtonLoading;
window.clearButtonLoading = clearButtonLoading;
window.withButtonLoading = withButtonLoading;

console.log('✅ Button loading system initialized');

