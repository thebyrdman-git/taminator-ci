# Taminator Intelligence - GUI Integration Specification

**Date:** October 29, 2025  
**Status:** Ready for Implementation  
**Target:** Taminator v2.0.0+

---

## 🎯 Goal

Add AI-augmented email analysis to Taminator GUI:
- **"Analyze Email" button** in main interface
- **Intelligence display panel** with confidence scores
- **Auto-populate case form** from extracted data
- **History view** of analyzed cases
- **Feedback system** for continuous learning

---

## 📐 Architecture

### **Frontend (Electron/HTML)**
```
gui/
├── index.html (main interface)
│   └── Add "Analyze Email" section
│
├── intelligence-analyzer.html (NEW)
│   ├── Email input textarea
│   ├── "Analyze" button
│   ├── Intelligence results display
│   └── "Create Case" button
│
├── intelligence-history.html (NEW)
│   ├── List of analyzed cases
│   ├── Search/filter
│   └── Statistics dashboard
│
└── public/js/
    └── intelligence-client.js (NEW)
        ├── analyzeEmail()
        ├── displayIntelligence()
        ├── populateCaseForm()
        └── recordFeedback()
```

### **Backend (Electron Main Process)**
```
main.js
└── IPC Handlers (NEW)
    ├── analyze-email → Call Python intelligence engine
    ├── get-case-history → Query SQLite database
    ├── record-feedback → Update database
    └── get-statistics → Get accuracy stats
```

### **Python Backend (Intelligence Engine)**
```
src/taminator/core/
├── intelligence_engine.py ✅ (exists)
├── database.py ✅ (exists)
└── ipc_bridge.py (NEW)
    └── Bridge between Electron and Python
```

---

## 🎨 UI Design

### **Main Dashboard - New Section**

```
┌─────────────────────────────────────────────────────────────┐
│  Taminator - AI-Augmented TAM Assistant                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📧 Email Intelligence Analyzer                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                                                         │ │
│  │  Paste email content here...                           │ │
│  │                                                         │ │
│  │                                                         │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  [🧠 Analyze Email]  [📋 View History]  [📊 Statistics]     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### **Intelligence Results Panel**

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Intelligence Analysis Results                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Overall Confidence: ● HIGH (89%)                           │
│                                                              │
│  ✅ Case Number: 04293185                                   │
│     Confidence: 95%                                          │
│                                                              │
│  ✅ Customer: JP Morgan Chase (334224)                      │
│     Confidence: 92%                                          │
│                                                              │
│  ✅ Issue Type: LICENSING                                   │
│     Product: Ansible Automation Platform                    │
│     Confidence: 89%                                          │
│                                                              │
│  🔴 Urgency: HIGH (62 days to deadline)                     │
│     Deadline: December 31, 2025                             │
│                                                              │
│  💡 Recommendation:                                          │
│     Escalate to licensing team                              │
│     • Verify subscription entitlements                      │
│     • Check renewal timeline                                │
│     • Loop in account executive                             │
│                                                              │
│  [✅ Create Case]  [❌ Incorrect]  [💾 Save for Later]      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### **Auto-Populated Case Form**

```
┌─────────────────────────────────────────────────────────────┐
│  📝 Create Case (Auto-Populated)                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Case Number: [04293185        ]  ✅ Verified              │
│                                                              │
│  Customer:    [JP Morgan Chase ]  ✅ Verified              │
│  Account:     [334224          ]  ✅ Verified              │
│                                                              │
│  Issue Type:  [Licensing ▼     ]  ✅ Auto-selected         │
│  Product:     [AAP ▼           ]  ✅ Auto-selected         │
│                                                              │
│  Priority:    [High ▼          ]  ✅ Auto-selected         │
│  Deadline:    [2025-12-31      ]  ✅ Auto-filled           │
│                                                              │
│  Contacts:                                                   │
│  • Ganesh Kasthurirangan (ganesh.kasthurirangan@jpmchase.com) │
│  • Kedar Dixit (kedar.dixit@jpmchase.com)                  │
│                                                              │
│  Recommendation:                                             │
│  [Escalate to licensing team                              ] │
│  [                                                         ] │
│                                                              │
│  [💾 Create Case]  [✏️ Edit]  [❌ Cancel]                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔌 IPC Communication

### **Electron Main Process → Python Backend**

```javascript
// main.js

const { spawn } = require('child_process');
const path = require('path');

// IPC Handler: Analyze Email
ipcMain.handle('analyze-email', async (event, emailText, tags) => {
  return new Promise((resolve, reject) => {
    // Get Python path
    const pythonPath = getPythonPath();
    const scriptPath = path.join(__dirname, '../src/taminator/core/ipc_bridge.py');
    
    // Spawn Python process
    const python = spawn(pythonPath, [
      scriptPath,
      'analyze',
      '--email', emailText,
      '--tags', JSON.stringify(tags || ['all'])
    ]);
    
    let output = '';
    let error = '';
    
    python.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    python.stderr.on('data', (data) => {
      error += data.toString();
    });
    
    python.on('close', (code) => {
      if (code === 0) {
        try {
          const intelligence = JSON.parse(output);
          resolve(intelligence);
        } catch (e) {
          reject(new Error(`Failed to parse intelligence: ${e.message}`));
        }
      } else {
        reject(new Error(`Analysis failed: ${error}`));
      }
    });
  });
});

// IPC Handler: Get Case History
ipcMain.handle('get-case-history', async (event, limit) => {
  // Similar pattern - call Python to query database
  // Return list of recent cases
});

// IPC Handler: Record Feedback
ipcMain.handle('record-feedback', async (event, caseNumber, feedback) => {
  // Call Python to update database with TAM feedback
});

// IPC Handler: Get Statistics
ipcMain.handle('get-statistics', async (event, days) => {
  // Call Python to get accuracy statistics
});
```

### **Frontend → Electron Main Process**

```javascript
// public/js/intelligence-client.js

class IntelligenceClient {
  /**
   * Analyze email and get intelligence
   */
  async analyzeEmail(emailText, tags = ['all']) {
    try {
      const intelligence = await window.api.analyzeEmail(emailText, tags);
      return intelligence;
    } catch (error) {
      console.error('Analysis failed:', error);
      throw error;
    }
  }
  
  /**
   * Get case history
   */
  async getCaseHistory(limit = 50) {
    return await window.api.getCaseHistory(limit);
  }
  
  /**
   * Record TAM feedback
   */
  async recordFeedback(caseNumber, decision, aiFollowed, notes) {
    return await window.api.recordFeedback(caseNumber, {
      decision,
      aiFollowed,
      notes
    });
  }
  
  /**
   * Get accuracy statistics
   */
  async getStatistics(days = 7) {
    return await window.api.getStatistics(days);
  }
}

// Global instance
window.intelligenceClient = new IntelligenceClient();
```

---

## 📝 Implementation Files

### **File 1: IPC Bridge (Python)**

**Location:** `src/taminator/core/ipc_bridge.py`

```python
#!/usr/bin/env python3
"""
IPC Bridge between Electron and Intelligence Engine

Handles communication from Electron main process to Python backend.
"""

import sys
import json
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from taminator.core.intelligence_engine import get_intelligence_engine
from taminator.core.database import get_intelligence_database


def analyze_email(email_text, tags):
    """Analyze email and return intelligence as JSON"""
    engine = get_intelligence_engine()
    intelligence = engine.analyze_email(email_text, tags=tags)
    
    # Store in database
    if intelligence.case_number:
        db = get_intelligence_database()
        intelligence_id = db.store_intelligence(intelligence)
    
    # Return as JSON
    return intelligence.to_dict()


def get_case_history(limit):
    """Get recent cases from database"""
    db = get_intelligence_database()
    return db.get_recent_cases(limit=limit)


def record_feedback(case_number, feedback):
    """Record TAM feedback"""
    db = get_intelligence_database()
    db.record_feedback(
        case_number=case_number,
        tam_decision=feedback['decision'],
        ai_followed=feedback['aiFollowed'],
        notes=feedback.get('notes')
    )
    return {"success": True}


def get_statistics(days):
    """Get accuracy statistics"""
    db = get_intelligence_database()
    accuracy = db.get_accuracy_stats(days=days)
    stats = db.get_database_stats()
    return {
        "accuracy": accuracy,
        "stats": stats
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['analyze', 'history', 'feedback', 'stats'])
    parser.add_argument('--email', help='Email text to analyze')
    parser.add_argument('--tags', help='Analysis tags (JSON array)')
    parser.add_argument('--limit', type=int, default=50, help='History limit')
    parser.add_argument('--case-number', help='Case number for feedback')
    parser.add_argument('--feedback', help='Feedback data (JSON)')
    parser.add_argument('--days', type=int, default=7, help='Statistics days')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'analyze':
            tags = json.loads(args.tags) if args.tags else ['all']
            result = analyze_email(args.email, tags)
        elif args.command == 'history':
            result = get_case_history(args.limit)
        elif args.command == 'feedback':
            feedback = json.loads(args.feedback)
            result = record_feedback(args.case_number, feedback)
        elif args.command == 'stats':
            result = get_statistics(args.days)
        
        # Output JSON to stdout
        print(json.dumps(result, default=str))
        sys.exit(0)
        
    except Exception as e:
        error = {"error": str(e)}
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
```

### **File 2: Intelligence Client (JavaScript)**

**Location:** `gui/public/js/intelligence-client.js`

```javascript
/**
 * Intelligence Client for Taminator GUI
 * 
 * Provides interface to AI-augmented email analysis
 */

class IntelligenceClient {
  constructor() {
    this.analyzing = false;
  }
  
  /**
   * Analyze email and get intelligence
   * 
   * @param {string} emailText - Email content to analyze
   * @param {Array} tags - Analysis tags (default: ['all'])
   * @returns {Promise<Object>} Intelligence results
   */
  async analyzeEmail(emailText, tags = ['all']) {
    if (this.analyzing) {
      throw new Error('Analysis already in progress');
    }
    
    this.analyzing = true;
    
    try {
      const intelligence = await window.api.analyzeEmail(emailText, tags);
      return intelligence;
    } finally {
      this.analyzing = false;
    }
  }
  
  /**
   * Get case history from database
   * 
   * @param {number} limit - Number of cases to retrieve
   * @returns {Promise<Array>} List of cases
   */
  async getCaseHistory(limit = 50) {
    return await window.api.getCaseHistory(limit);
  }
  
  /**
   * Record TAM feedback on AI recommendation
   * 
   * @param {string} caseNumber - Case number
   * @param {string} decision - TAM's decision
   * @param {boolean} aiFollowed - Whether TAM followed AI recommendation
   * @param {string} notes - Optional feedback notes
   * @returns {Promise<Object>} Success response
   */
  async recordFeedback(caseNumber, decision, aiFollowed, notes = null) {
    return await window.api.recordFeedback(caseNumber, {
      decision,
      aiFollowed,
      notes
    });
  }
  
  /**
   * Get accuracy statistics
   * 
   * @param {number} days - Number of days to retrieve
   * @returns {Promise<Object>} Statistics data
   */
  async getStatistics(days = 7) {
    return await window.api.getStatistics(days);
  }
  
  /**
   * Display intelligence results in UI
   * 
   * @param {Object} intelligence - Intelligence data
   * @param {Element} container - DOM element to display in
   */
  displayIntelligence(intelligence, container) {
    const html = this._generateIntelligenceHTML(intelligence);
    container.innerHTML = html;
    
    // Attach event listeners
    this._attachEventListeners(container, intelligence);
  }
  
  /**
   * Generate HTML for intelligence display
   * @private
   */
  _generateIntelligenceHTML(intelligence) {
    const confidence = intelligence.confidence_scores || {};
    const overall = intelligence.confidence_score || 0;
    const level = intelligence.confidence_level || 'unknown';
    
    const confidenceColor = overall >= 0.8 ? 'success' : overall >= 0.5 ? 'warning' : 'danger';
    const confidenceIcon = overall >= 0.8 ? '✅' : overall >= 0.5 ? '⚠️' : '❌';
    
    return `
      <div class="intelligence-results">
        <div class="confidence-header">
          <h3>📊 Intelligence Analysis Results</h3>
          <span class="confidence-badge confidence-${confidenceColor}">
            ${confidenceIcon} ${level.toUpperCase()} (${(overall * 100).toFixed(0)}%)
          </span>
        </div>
        
        <div class="intelligence-sections">
          ${this._generateCaseSection(intelligence)}
          ${this._generateCustomerSection(intelligence)}
          ${this._generateIssueSection(intelligence)}
          ${this._generateUrgencySection(intelligence)}
          ${this._generateRecommendationSection(intelligence)}
        </div>
        
        <div class="intelligence-actions">
          <button class="btn btn-primary" data-action="create-case">
            ✅ Create Case
          </button>
          <button class="btn btn-secondary" data-action="incorrect">
            ❌ Incorrect
          </button>
          <button class="btn btn-secondary" data-action="save">
            💾 Save for Later
          </button>
        </div>
      </div>
    `;
  }
  
  /**
   * Generate case number section HTML
   * @private
   */
  _generateCaseSection(intelligence) {
    if (!intelligence.case_number) {
      return '<div class="intelligence-section">❌ Case Number: Not detected</div>';
    }
    
    const conf = (intelligence.confidence_scores?.case_number || 0) * 100;
    return `
      <div class="intelligence-section">
        <div class="section-header">
          <span class="section-icon">✅</span>
          <span class="section-title">Case Number</span>
          <span class="section-confidence">${conf.toFixed(0)}%</span>
        </div>
        <div class="section-content">
          <strong>${intelligence.case_number}</strong>
        </div>
      </div>
    `;
  }
  
  /**
   * Generate customer section HTML
   * @private
   */
  _generateCustomerSection(intelligence) {
    if (!intelligence.customer) {
      return '<div class="intelligence-section">❌ Customer: Not detected</div>';
    }
    
    const customer = intelligence.customer;
    const conf = (customer.confidence || 0) * 100;
    
    return `
      <div class="intelligence-section">
        <div class="section-header">
          <span class="section-icon">✅</span>
          <span class="section-title">Customer</span>
          <span class="section-confidence">${conf.toFixed(0)}%</span>
        </div>
        <div class="section-content">
          <strong>${customer.name}</strong>
          ${customer.account_number ? `<br>Account: ${customer.account_number}` : ''}
        </div>
      </div>
    `;
  }
  
  /**
   * Generate issue section HTML
   * @private
   */
  _generateIssueSection(intelligence) {
    if (!intelligence.issue) {
      return '<div class="intelligence-section">❌ Issue Type: Not classified</div>';
    }
    
    const issue = intelligence.issue;
    const conf = (issue.confidence || 0) * 100;
    
    return `
      <div class="intelligence-section">
        <div class="section-header">
          <span class="section-icon">✅</span>
          <span class="section-title">Issue Type</span>
          <span class="section-confidence">${conf.toFixed(0)}%</span>
        </div>
        <div class="section-content">
          <strong>${issue.primary_type.toUpperCase()}</strong>
          ${issue.product ? `<br>Product: ${issue.product}` : ''}
          ${issue.reasoning ? `<br><em>${issue.reasoning}</em>` : ''}
        </div>
      </div>
    `;
  }
  
  /**
   * Generate urgency section HTML
   * @private
   */
  _generateUrgencySection(intelligence) {
    if (!intelligence.urgency) {
      return '<div class="intelligence-section">❌ Urgency: Not assessed</div>';
    }
    
    const urgency = intelligence.urgency;
    const levelEmoji = urgency.level === 'high' ? '🔴' : urgency.level === 'medium' ? '🟡' : '🟢';
    
    return `
      <div class="intelligence-section">
        <div class="section-header">
          <span class="section-icon">${levelEmoji}</span>
          <span class="section-title">Urgency</span>
        </div>
        <div class="section-content">
          <strong>${urgency.level.toUpperCase()}</strong>
          ${urgency.deadline ? `<br>Deadline: ${urgency.deadline}` : ''}
          ${urgency.days_remaining ? `<br>${urgency.days_remaining} days remaining` : ''}
        </div>
      </div>
    `;
  }
  
  /**
   * Generate recommendation section HTML
   * @private
   */
  _generateRecommendationSection(intelligence) {
    if (!intelligence.recommended_actions) {
      return '';
    }
    
    const actions = intelligence.recommended_actions;
    
    return `
      <div class="intelligence-section">
        <div class="section-header">
          <span class="section-icon">💡</span>
          <span class="section-title">Recommendation</span>
        </div>
        <div class="section-content">
          <strong>${actions.primary_action}</strong>
          <br><em>${actions.reasoning}</em>
          ${actions.immediate_actions && actions.immediate_actions.length > 0 ? `
            <ul>
              ${actions.immediate_actions.map(a => `<li>${a}</li>`).join('')}
            </ul>
          ` : ''}
        </div>
      </div>
    `;
  }
  
  /**
   * Attach event listeners to intelligence display
   * @private
   */
  _attachEventListeners(container, intelligence) {
    // Create Case button
    const createBtn = container.querySelector('[data-action="create-case"]');
    if (createBtn) {
      createBtn.addEventListener('click', () => {
        this.populateCaseForm(intelligence);
      });
    }
    
    // Incorrect button
    const incorrectBtn = container.querySelector('[data-action="incorrect"]');
    if (incorrectBtn) {
      incorrectBtn.addEventListener('click', () => {
        this.handleIncorrectFeedback(intelligence);
      });
    }
    
    // Save button
    const saveBtn = container.querySelector('[data-action="save"]');
    if (saveBtn) {
      saveBtn.addEventListener('click', () => {
        this.saveForLater(intelligence);
      });
    }
  }
  
  /**
   * Populate case form with intelligence data
   * 
   * @param {Object} intelligence - Intelligence data
   */
  populateCaseForm(intelligence) {
    // TODO: Implement case form population
    // This will depend on your existing case form structure
    
    console.log('Populating case form with:', intelligence);
    
    // Example:
    // document.getElementById('case-number').value = intelligence.case_number || '';
    // document.getElementById('customer-name').value = intelligence.customer?.name || '';
    // etc.
  }
  
  /**
   * Handle incorrect feedback
   * 
   * @param {Object} intelligence - Intelligence data
   */
  async handleIncorrectFeedback(intelligence) {
    const notes = prompt('What was incorrect? (This helps improve accuracy)');
    if (notes && intelligence.case_number) {
      await this.recordFeedback(
        intelligence.case_number,
        'Marked as incorrect',
        false,
        notes
      );
      alert('Feedback recorded. Thank you!');
    }
  }
  
  /**
   * Save intelligence for later review
   * 
   * @param {Object} intelligence - Intelligence data
   */
  saveForLater(intelligence) {
    // Intelligence is already saved in database
    // Just show confirmation
    alert('Intelligence saved! View in History.');
  }
}

// Create global instance
window.intelligenceClient = new IntelligenceClient();
```

---

## 🧪 Testing Plan

### **Unit Tests:**
1. Test IPC bridge Python script
2. Test intelligence client JavaScript
3. Test database queries
4. Test UI rendering

### **Integration Tests:**
1. Test Electron → Python communication
2. Test full analyze workflow
3. Test case form population
4. Test feedback recording

### **User Acceptance Tests:**
1. Analyze real case email
2. Verify intelligence accuracy
3. Create case from intelligence
4. Record feedback
5. View history and statistics

---

## 📦 Packaging Requirements

### **Include in Build:**
```json
// package.json
{
  "build": {
    "files": [
      "gui/**/*",
      "src/taminator/**/*",
      "!src/**/*.pyc",
      "!src/**/__pycache__"
    ],
    "extraResources": [
      {
        "from": "src/taminator",
        "to": "taminator",
        "filter": ["**/*", "!**/*.pyc", "!**/__pycache__"]
      }
    ]
  }
}
```

### **Python Dependencies:**
- No external dependencies needed!
- Uses only Python stdlib
- SQLite is built into Python

---

## 🎯 Success Criteria

### **Phase 3 Complete When:**
- [ ] "Analyze Email" button in GUI
- [ ] Intelligence results display correctly
- [ ] Confidence scores shown with colors
- [ ] Case form auto-populates
- [ ] Feedback buttons work
- [ ] History view shows past cases
- [ ] Statistics dashboard displays accuracy
- [ ] All tests passing
- [ ] Works on all platforms (Linux, Windows, macOS)

---

## 🚀 Implementation Timeline

### **Day 1: Core Integration (4-6 hours)**
- Create IPC bridge Python script
- Add IPC handlers to main.js
- Create intelligence-client.js
- Test Electron → Python communication

### **Day 2: UI Implementation (4-6 hours)**
- Add "Analyze Email" section to index.html
- Create intelligence results display
- Add CSS styling
- Test UI rendering

### **Day 3: Case Form Integration (2-4 hours)**
- Implement auto-populate logic
- Add feedback buttons
- Create history view
- Test complete workflow

### **Day 4: Testing & Polish (2-4 hours)**
- Integration testing
- Cross-platform testing
- Bug fixes
- Documentation

**Total: 12-20 hours (~2-3 days)**

---

**Status:** ✅ **SPECIFICATION COMPLETE**

**Next:** Implement IPC bridge and intelligence client

**Ready for:** Development sprint!

