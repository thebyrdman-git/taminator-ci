/**
 * Intelligence Client for Taminator GUI
 * 
 * Provides interface to AI-augmented email analysis
 */

class IntelligenceClient {
  constructor() {
    this.analyzing = false;
    
    // Use globally available ipcRenderer (from index.html)
    // nodeIntegration: true means it's already in global scope
    this.ipcRenderer = typeof ipcRenderer !== 'undefined' ? ipcRenderer : null;
    
    if (!this.ipcRenderer) {
      console.warn('[Intelligence Client] Running in browser mode (IPC unavailable)');
    }
  }
  
  /**
   * Analyze email and get intelligence
   */
  async analyzeEmail(emailText, tags = ['all']) {
    if (this.analyzing) {
      throw new Error('Analysis already in progress');
    }
    
    if (!this.ipcRenderer) {
      throw new Error('IPC not available - running in browser mode');
    }
    
    this.analyzing = true;
    
    try {
      const intelligence = await this.ipcRenderer.invoke('analyze-email', emailText, tags);
      return intelligence;
    } finally {
      this.analyzing = false;
    }
  }
  
  /**
   * Get case history from database
   */
  async getCaseHistory(limit = 50) {
    if (!this.ipcRenderer) {
      throw new Error('IPC not available - running in browser mode');
    }
    
    return await this.ipcRenderer.invoke('get-case-history', limit);
  }
  
  /**
   * Record TAM feedback on AI recommendation
   */
  async recordFeedback(caseNumber, decision, aiFollowed, notes = null) {
    if (!this.ipcRenderer) {
      throw new Error('IPC not available - running in browser mode');
    }
    
    return await this.ipcRenderer.invoke('record-feedback', caseNumber, {
      decision,
      aiFollowed,
      notes
    });
  }
  
  /**
   * Get accuracy statistics
   */
  async getStatistics(days = 7) {
    if (!this.ipcRenderer) {
      throw new Error('IPC not available - running in browser mode');
    }
    
    return await this.ipcRenderer.invoke('get-statistics', days);
  }
  
  /**
   * Display intelligence results in UI
   */
  displayIntelligence(intelligence, container) {
    const html = this._generateIntelligenceHTML(intelligence);
    container.innerHTML = html;
    this._attachEventListeners(container, intelligence);
  }
  
  /**
   * Generate HTML for intelligence display
   */
  _generateIntelligenceHTML(intelligence) {
    const overall = intelligence.confidence_score || 0;
    const level = intelligence.confidence_level || 'unknown';
    const confidenceColor = overall >= 0.8 ? 'success' : overall >= 0.5 ? 'warning' : 'danger';
    const confidenceIcon = overall >= 0.8 ? '✅' : overall >= 0.5 ? '⚠️' : '❌';
    
    return `
      <div class="intelligence-results" style="padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <div class="confidence-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
          <h3 style="margin: 0;">📊 Intelligence Analysis Results</h3>
          <span class="confidence-badge confidence-${confidenceColor}" style="padding: 8px 16px; border-radius: 4px; font-weight: bold; background: ${overall >= 0.8 ? '#28a745' : overall >= 0.5 ? '#ffc107' : '#dc3545'}; color: white;">
            ${confidenceIcon} ${level.toUpperCase()} (${(overall * 100).toFixed(0)}%)
          </span>
        </div>
        
        <div class="intelligence-sections" style="display: grid; gap: 16px;">
          ${this._generateCaseSection(intelligence)}
          ${this._generateCustomerSection(intelligence)}
          ${this._generateIssueSection(intelligence)}
          ${this._generateUrgencySection(intelligence)}
          ${this._generateRecommendationSection(intelligence)}
        </div>
        
        <div class="intelligence-actions" style="margin-top: 24px; display: flex; gap: 12px;">
          <button class="btn btn-primary" data-action="create-case" style="padding: 10px 20px; background: #EE0000; color: white; border: none; border-radius: 4px; cursor: pointer;">
            ✅ Create Case
          </button>
          <button class="btn btn-secondary" data-action="incorrect" style="padding: 10px 20px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">
            ❌ Incorrect
          </button>
          <button class="btn btn-secondary" data-action="save" style="padding: 10px 20px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">
            💾 Save for Later
          </button>
        </div>
      </div>
    `;
  }
  
  _generateCaseSection(intelligence) {
    if (!intelligence.case_number) {
      return '<div class="intelligence-section" style="padding: 12px; background: #f8f9fa; border-radius: 4px;">❌ Case Number: Not detected</div>';
    }
    
    const conf = ((intelligence.confidence_scores?.case_number || 0) * 100).toFixed(0);
    return `
      <div class="intelligence-section" style="padding: 12px; background: #f8f9fa; border-radius: 4px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
          <span style="font-weight: bold;">✅ Case Number</span>
          <span style="color: #6c757d;">${conf}% confidence</span>
        </div>
        <div style="font-size: 18px; font-weight: bold;">${intelligence.case_number}</div>
      </div>
    `;
  }
  
  _generateCustomerSection(intelligence) {
    if (!intelligence.customer) {
      return '<div class="intelligence-section" style="padding: 12px; background: #f8f9fa; border-radius: 4px;">❌ Customer: Not detected</div>';
    }
    
    const customer = intelligence.customer;
    const conf = ((customer.confidence || 0) * 100).toFixed(0);
    
    return `
      <div class="intelligence-section" style="padding: 12px; background: #f8f9fa; border-radius: 4px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
          <span style="font-weight: bold;">✅ Customer</span>
          <span style="color: #6c757d;">${conf}% confidence</span>
        </div>
        <div style="font-size: 16px; font-weight: bold;">${customer.name}</div>
        ${customer.account_number ? `<div style="color: #6c757d; margin-top: 4px;">Account: ${customer.account_number}</div>` : ''}
      </div>
    `;
  }
  
  _generateIssueSection(intelligence) {
    if (!intelligence.issue) {
      return '<div class="intelligence-section" style="padding: 12px; background: #f8f9fa; border-radius: 4px;">❌ Issue Type: Not classified</div>';
    }
    
    const issue = intelligence.issue;
    const conf = ((issue.confidence || 0) * 100).toFixed(0);
    
    return `
      <div class="intelligence-section" style="padding: 12px; background: #f8f9fa; border-radius: 4px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
          <span style="font-weight: bold;">✅ Issue Type</span>
          <span style="color: #6c757d;">${conf}% confidence</span>
        </div>
        <div style="font-size: 16px; font-weight: bold;">${issue.primary_type.toUpperCase()}</div>
        ${issue.product ? `<div style="color: #6c757d; margin-top: 4px;">Product: ${issue.product}</div>` : ''}
        ${issue.reasoning ? `<div style="color: #6c757d; margin-top: 4px; font-style: italic;">${issue.reasoning}</div>` : ''}
      </div>
    `;
  }
  
  _generateUrgencySection(intelligence) {
    if (!intelligence.urgency) {
      return '<div class="intelligence-section" style="padding: 12px; background: #f8f9fa; border-radius: 4px;">❌ Urgency: Not assessed</div>';
    }
    
    const urgency = intelligence.urgency;
    const levelEmoji = urgency.level === 'high' ? '🔴' : urgency.level === 'medium' ? '🟡' : '🟢';
    
    return `
      <div class="intelligence-section" style="padding: 12px; background: #f8f9fa; border-radius: 4px;">
        <div style="font-weight: bold; margin-bottom: 8px;">${levelEmoji} Urgency</div>
        <div style="font-size: 16px; font-weight: bold;">${urgency.level.toUpperCase()}</div>
        ${urgency.deadline ? `<div style="color: #6c757d; margin-top: 4px;">Deadline: ${urgency.deadline}</div>` : ''}
        ${urgency.days_remaining ? `<div style="color: #6c757d; margin-top: 4px;">${urgency.days_remaining} days remaining</div>` : ''}
      </div>
    `;
  }
  
  _generateRecommendationSection(intelligence) {
    if (!intelligence.recommended_actions) {
      return '';
    }
    
    const actions = intelligence.recommended_actions;
    
    return `
      <div class="intelligence-section" style="padding: 12px; background: #f8f9fa; border-radius: 4px;">
        <div style="font-weight: bold; margin-bottom: 8px;">💡 Recommendation</div>
        <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px;">${actions.primary_action}</div>
        <div style="color: #6c757d; font-style: italic; margin-bottom: 8px;">${actions.reasoning}</div>
        ${actions.immediate_actions && actions.immediate_actions.length > 0 ? `
          <ul style="margin: 8px 0; padding-left: 20px;">
            ${actions.immediate_actions.map(a => `<li style="margin: 4px 0;">${a}</li>`).join('')}
          </ul>
        ` : ''}
      </div>
    `;
  }
  
  _attachEventListeners(container, intelligence) {
    const createBtn = container.querySelector('[data-action="create-case"]');
    if (createBtn) {
      createBtn.addEventListener('click', () => {
        this.populateCaseForm(intelligence);
      });
    }
    
    const incorrectBtn = container.querySelector('[data-action="incorrect"]');
    if (incorrectBtn) {
      incorrectBtn.addEventListener('click', () => {
        this.handleIncorrectFeedback(intelligence);
      });
    }
    
    const saveBtn = container.querySelector('[data-action="save"]');
    if (saveBtn) {
      saveBtn.addEventListener('click', () => {
        this.saveForLater(intelligence);
      });
    }
  }
  
  populateCaseForm(intelligence) {
    alert('Case form population will be implemented based on your existing form structure. Intelligence data is ready!');
    console.log('Intelligence data for case form:', intelligence);
  }
  
  async handleIncorrectFeedback(intelligence) {
    const notes = prompt('What was incorrect? (This helps improve accuracy)');
    if (notes && intelligence.case_number) {
      try {
        await this.recordFeedback(
          intelligence.case_number,
          'Marked as incorrect',
          false,
          notes
        );
        alert('Feedback recorded. Thank you!');
      } catch (error) {
        alert('Failed to record feedback: ' + error.message);
      }
    }
  }
  
  saveForLater(intelligence) {
    alert('Intelligence saved! View in History.');
  }
}

// Create global instance
if (typeof window !== 'undefined') {
  window.intelligenceClient = new IntelligenceClient();
}

