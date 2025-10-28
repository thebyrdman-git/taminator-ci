/**
 * Taminator API Client - Frontend SDK
 * 
 * Production-grade API client for GUI:
 * - Structured requests/responses
 * - Automatic error handling
 * - Type-safe operations
 * - No more CLI spawning!
 */

class TaminatorAPIError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.name = 'TaminatorAPIError';
    this.code = code;
    this.details = details;
  }
}

class TaminatorAPI {
  constructor(baseURL = 'http://127.0.0.1:8765') {
    this.baseURL = baseURL;
  }

  /**
   * Make HTTP request to API
   * Handles errors and returns structured data
   */
  async _request(method, endpoint, data = null) {
    const url = `${this.baseURL}${endpoint}`;
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(url, options);
      const responseData = await response.json();

      // Handle error responses
      if (!response.ok) {
        if (responseData.error) {
          throw new TaminatorAPIError(
            responseData.error.code,
            responseData.error.message,
            responseData.error.details || {}
          );
        }
        throw new Error(`API request failed: ${response.statusText}`);
      }

      return responseData;
    } catch (error) {
      if (error instanceof TaminatorAPIError) {
        throw error;
      }
      
      // Network or connection errors
      if (error.message.includes('fetch')) {
        throw new TaminatorAPIError(
          'service_unavailable',
          'Cannot connect to Taminator service. Is it running?',
          { originalError: error.message }
        );
      }

      throw error;
    }
  }

  // ============== Health Checks ==============

  async getHealth() {
    return await this._request('GET', '/health');
  }

  async isServiceHealthy() {
    try {
      const health = await this.getHealth();
      return health.status === 'healthy';
    } catch {
      return false;
    }
  }

  // ============== Customers API ==============

  async listCustomers() {
    return await this._request('GET', '/api/customers/');
  }

  async getCustomer(customerId) {
    return await this._request('GET', `/api/customers/${customerId}`);
  }

  async createCustomer(customerData) {
    return await this._request('POST', '/api/customers/', customerData);
  }

  async deleteCustomer(customerId) {
    return await this._request('DELETE', `/api/customers/${customerId}`);
  }

  async getCustomerStats(customerId) {
    return await this._request('GET', `/api/customers/${customerId}/stats`);
  }

  // ============== JIRA API ==============

  async checkJiraStatus(customerId) {
    return await this._request('POST', `/api/jira/${customerId}/check`);
  }

  async updateFromJira(customerId, dryRun = false) {
    return await this._request('POST', `/api/jira/${customerId}/update`, {
      dry_run: dryRun
    });
  }

  async listJiraIssues(customerId) {
    return await this._request('GET', `/api/jira/${customerId}/issues`);
  }

  // ============== Portal API ==============

  async postToPortal(customerId, groupId, title, content, previewMode = false) {
    return await this._request('POST', '/api/portal/post', {
      customer_id: customerId,
      group_id: groupId,
      title,
      content,
      preview_mode: previewMode
    });
  }

  async previewPortalPost(customerId, groupId, title, content) {
    return await this._request('POST', '/api/portal/preview', {
      customer_id: customerId,
      group_id: groupId,
      title,
      content
    });
  }

  async getPortalGroup(customerId) {
    return await this._request('GET', `/api/portal/${customerId}/group`);
  }
}

// Create singleton instance
const taminatorAPI = new TaminatorAPI();

// Export for use in renderer process
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { TaminatorAPI, TaminatorAPIError, taminatorAPI };
}


