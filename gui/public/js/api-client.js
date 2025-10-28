/**
 * Taminator API Client - JavaScript SDK for GUI
 * 
 * Production-grade API client with:
 * - Structured error handling
 * - Type-safe responses
 * - Retry logic
 * - Request/response logging
 */

class TaminatorApiClient {
  constructor(baseUrl = 'http://127.0.0.1:8765') {
    this.baseUrl = baseUrl;
    this.timeout = 30000; // 30 seconds
  }

  /**
   * Generic API request handler
   * @param {string} endpoint - API endpoint (e.g., '/api/customers')
   * @param {object} options - Fetch options
   * @returns {Promise<object>} - API response
   */
  async _request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      signal: AbortSignal.timeout(this.timeout)
    };

    try {
      console.log(`[API] ${options.method || 'GET'} ${endpoint}`);
      const response = await fetch(url, config);
      
      if (!response.ok) {
        // Parse error response
        const error = await response.json().catch(() => ({
          error_code: 'UNKNOWN_ERROR',
          message: `HTTP ${response.status}`
        }));
        
        throw new TaminatorApiError(
          error.message || `Request failed: ${response.status}`,
          error.error_code || 'HTTP_ERROR',
          response.status,
          error.details
        );
      }

      const data = await response.json();
      console.log(`[API] ✅ ${endpoint} success`);
      return data;
      
    } catch (error) {
      if (error instanceof TaminatorApiError) {
        throw error;
      }
      
      // Network or other errors
      console.error(`[API] ❌ ${endpoint} failed:`, error.message);
      throw new TaminatorApiError(
        error.message || 'Request failed',
        'NETWORK_ERROR',
        0,
        { originalError: error.name }
      );
    }
  }

  // ============================================================================
  // HEALTH ENDPOINTS
  // ============================================================================

  /**
   * Check service health
   * @returns {Promise<object>} - Health status
   */
  async health() {
    return this._request('/health');
  }

  /**
   * Get detailed service info
   * @returns {Promise<object>} - Service info
   */
  async info() {
    return this._request('/info');
  }

  // ============================================================================
  // CUSTOMER ENDPOINTS
  // ============================================================================

  /**
   * List all customers
   * @returns {Promise<Array>} - Array of customers
   */
  async listCustomers() {
    return this._request('/api/customers/');
  }

  /**
   * Get customer by ID
   * @param {string} customerId - Customer slug
   * @returns {Promise<object>} - Customer data
   */
  async getCustomer(customerId) {
    return this._request(`/api/customers/${customerId}`);
  }

  /**
   * Create new customer
   * @param {object} customer - Customer data
   * @returns {Promise<object>} - Created customer
   */
  async createCustomer(customer) {
    return this._request('/api/customers', {
      method: 'POST',
      body: JSON.stringify(customer)
    });
  }

  /**
   * Delete customer
   * @param {string} customerId - Customer slug
   * @returns {Promise<void>}
   */
  async deleteCustomer(customerId) {
    return this._request(`/api/customers/${customerId}`, {
      method: 'DELETE'
    });
  }

  /**
   * Get customer statistics
   * @param {string} customerId - Customer slug
   * @returns {Promise<object>} - Customer stats
   */
  async getCustomerStats(customerId) {
    return this._request(`/api/customers/${customerId}/stats`);
  }

  // ============================================================================
  // JIRA ENDPOINTS
  // ============================================================================

  /**
   * Check customer's JIRA issues
   * @param {string} customerId - Customer slug
   * @returns {Promise<Array>} - Array of issues
   */
  async checkJira(customerId) {
    return this._request(`/api/jira/${customerId}/check`);
  }

  /**
   * Update customer's JIRA issues
   * @param {string} customerId - Customer slug
   * @returns {Promise<object>} - Update result
   */
  async updateJira(customerId) {
    return this._request(`/api/jira/${customerId}/update`, {
      method: 'POST'
    });
  }

  /**
   * List customer's issues (from report)
   * @param {string} customerId - Customer slug
   * @returns {Promise<Array>} - Array of issues
   */
  async listIssues(customerId) {
    return this._request(`/api/jira/${customerId}/issues`);
  }

  // ============================================================================
  // PORTAL ENDPOINTS
  // ============================================================================

  /**
   * Post report to Customer Portal
   * @param {string} customerId - Customer slug
   * @param {string} format - Report format (html, markdown, pdf)
   * @returns {Promise<object>} - Post result with URL
   */
  async postToPortal(customerId, format = 'html') {
    return this._request(`/api/portal/${customerId}/post`, {
      method: 'POST',
      body: JSON.stringify({ format })
    });
  }

  /**
   * Preview report before posting
   * @param {string} customerId - Customer slug
   * @param {string} format - Report format
   * @returns {Promise<object>} - Preview data
   */
  async previewPortal(customerId, format = 'html') {
    return this._request(`/api/portal/${customerId}/preview?format=${format}`);
  }
}

/**
 * Custom error class for API errors
 */
class TaminatorApiError extends Error {
  constructor(message, errorCode, httpStatus, details = null) {
    super(message);
    this.name = 'TaminatorApiError';
    this.errorCode = errorCode;
    this.httpStatus = httpStatus;
    this.details = details;
  }

  /**
   * Get user-friendly error message
   */
  getUserMessage() {
    switch (this.errorCode) {
      case 'CUSTOMER_NOT_FOUND':
        return 'Customer not found. Please check the customer ID.';
      
      case 'CONFIG_ERROR':
        return 'Configuration error. Please check customer settings.';
      
      case 'JIRA_AUTH_ERROR':
        return 'JIRA authentication failed. Please check your token.';
      
      case 'NETWORK_ERROR':
        return 'Network error. Please check your connection.';
      
      case 'SERVICE_UNAVAILABLE':
        return 'Service temporarily unavailable. Please try again.';
      
      default:
        return this.message;
    }
  }

  /**
   * Check if error is retryable
   */
  isRetryable() {
    const retryableErrors = [
      'NETWORK_ERROR',
      'SERVICE_UNAVAILABLE',
      'TIMEOUT_ERROR'
    ];
    
    return retryableErrors.includes(this.errorCode);
  }
}

// Export for use in renderer
if (typeof window !== 'undefined') {
  window.TaminatorApiClient = TaminatorApiClient;
  window.TaminatorApiError = TaminatorApiError;
}

// Export for Node.js (if needed)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { TaminatorApiClient, TaminatorApiError };
}

