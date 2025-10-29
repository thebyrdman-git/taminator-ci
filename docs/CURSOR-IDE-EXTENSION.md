# Taminator Intelligence - Cursor IDE Extension

**Bring Taminator's AI-powered case analysis directly into your IDE**

---

## Overview

A Cursor IDE extension that connects to your local Taminator Intelligence service, allowing TAMs to analyze customer emails and cases without leaving their development environment.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CURSOR IDE                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────┐               │
│  │  Taminator Extension (TypeScript)        │               │
│  │  - Email analyzer panel                  │               │
│  │  - Case history sidebar                  │               │
│  │  - Quick actions                         │               │
│  │  - Status bar integration                │               │
│  └──────────────┬───────────────────────────┘               │
│                 │ HTTP/WebSocket                            │
└─────────────────┼───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│          Taminator Intelligence Service                      │
│          (Container or Desktop App)                          │
│          http://localhost:8080                               │
├─────────────────────────────────────────────────────────────┤
│  - Intelligence Engine (Python)                              │
│  - SQLite Database                                           │
│  - REST API                                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Features

### 1. Email Analysis Panel

**Command Palette:**
- `Taminator: Analyze Email` - Analyze selected text or clipboard
- `Taminator: Open Analyzer` - Open analysis panel

**Panel Features:**
- Paste email content
- One-click analysis
- Real-time results display
- Copy results to clipboard
- Save to case history

**Results Display:**
```
┌─────────────────────────────────────────────┐
│ 📧 Email Analysis Results                   │
├─────────────────────────────────────────────┤
│ Case Number: 04293185                       │
│ Customer: JP Morgan Chase                   │
│ Account: 334224                             │
│                                             │
│ Issue Type: Licensing/Subscription          │
│ Urgency: 🔴 HIGH (Deadline: Dec 31, 2025)  │
│                                             │
│ Recommended Actions:                        │
│ • Contact licensing team                    │
│ • Verify subscription status                │
│ • Schedule renewal call                     │
│                                             │
│ Confidence: 89% (HIGH)                      │
│                                             │
│ [Copy to Clipboard] [Save] [Feedback]      │
└─────────────────────────────────────────────┘
```

### 2. Case History Sidebar

**Tree View:**
```
TAMINATOR INTELLIGENCE
├─ 📊 Recent Cases (5)
│  ├─ 04293185 - JPMC - HIGH
│  ├─ 04280915 - Wells Fargo - MEDIUM
│  └─ ...
├─ 📈 Accuracy: 89%
├─ 🎯 Cases Analyzed: 47
└─ ⚙️ Settings
```

**Click on case:**
- View full analysis
- See original email
- Review feedback history
- Re-analyze with updated rules

### 3. Quick Actions

**Context Menu (Right-click on selected text):**
- `Analyze with Taminator` - Analyze selected email
- `Extract Case Number` - Quick extraction
- `Check Urgency` - Quick urgency check

**Status Bar:**
```
🤖 Taminator: Connected | Cases: 47 | Accuracy: 89%
```

### 4. Inline Decorations

**Email Detection:**
- Automatically detect email patterns in open files
- Show inline hints for case numbers
- Highlight urgency keywords

**Example:**
```
From: ganesh.kasthurirangan@jpmchase.com
                                      ↑
                          [🔍 Analyze with Taminator]

Case 04293185 needs attention
     ↑
     [📋 View Case History]
```

---

## Extension Structure

```
taminator-cursor-extension/
├── package.json                 # Extension manifest
├── tsconfig.json               # TypeScript config
├── src/
│   ├── extension.ts            # Main entry point
│   ├── api/
│   │   └── taminator-client.ts # API client
│   ├── panels/
│   │   ├── analyzer-panel.ts   # Email analyzer
│   │   └── results-view.ts     # Results display
│   ├── sidebar/
│   │   ├── history-provider.ts # Case history tree
│   │   └── stats-view.ts       # Statistics view
│   ├── commands/
│   │   ├── analyze.ts          # Analyze command
│   │   ├── extract.ts          # Extract case number
│   │   └── feedback.ts         # Provide feedback
│   ├── decorations/
│   │   └── email-detector.ts   # Inline decorations
│   └── utils/
│       ├── config.ts           # Configuration
│       └── logger.ts           # Logging
├── media/
│   ├── icon.png                # Extension icon
│   └── screenshots/            # Screenshots
├── webview/
│   ├── analyzer.html           # Analyzer panel HTML
│   ├── results.html            # Results view HTML
│   └── styles.css              # Webview styles
└── README.md                   # Extension docs
```

---

## API Client

### Taminator Intelligence API

**Base URL:** `http://localhost:8080/api/v1`

**Endpoints:**

```typescript
interface TaminatorClient {
  // Analyze email
  analyzeEmail(email: string, tags?: string[]): Promise<IntelligenceOutput>;
  
  // Get case history
  getCaseHistory(limit?: number): Promise<CaseHistory[]>;
  
  // Get case by number
  getCase(caseNumber: string): Promise<IntelligenceOutput>;
  
  // Record feedback
  recordFeedback(caseNumber: string, feedback: Feedback): Promise<void>;
  
  // Get statistics
  getStatistics(days?: number): Promise<Statistics>;
  
  // Health check
  healthCheck(): Promise<HealthStatus>;
}
```

**Example Usage:**

```typescript
import { TaminatorClient } from './api/taminator-client';

const client = new TaminatorClient('http://localhost:8080');

// Analyze email
const result = await client.analyzeEmail(emailText);

console.log(`Case: ${result.case_number}`);
console.log(`Customer: ${result.customer.name}`);
console.log(`Urgency: ${result.urgency.level}`);
```

---

## Configuration

### Extension Settings

```json
{
  "taminator.serviceUrl": {
    "type": "string",
    "default": "http://localhost:8080",
    "description": "Taminator Intelligence service URL"
  },
  "taminator.autoDetect": {
    "type": "boolean",
    "default": true,
    "description": "Automatically detect emails in open files"
  },
  "taminator.showInlineHints": {
    "type": "boolean",
    "default": true,
    "description": "Show inline hints for case numbers"
  },
  "taminator.statusBarEnabled": {
    "type": "boolean",
    "default": true,
    "description": "Show Taminator status in status bar"
  },
  "taminator.defaultTags": {
    "type": "array",
    "default": ["all"],
    "description": "Default tags for analysis"
  }
}
```

---

## Commands

### Command Palette

```json
{
  "commands": [
    {
      "command": "taminator.analyzeEmail",
      "title": "Taminator: Analyze Email",
      "category": "Taminator"
    },
    {
      "command": "taminator.openAnalyzer",
      "title": "Taminator: Open Analyzer",
      "category": "Taminator"
    },
    {
      "command": "taminator.showHistory",
      "title": "Taminator: Show Case History",
      "category": "Taminator"
    },
    {
      "command": "taminator.extractCaseNumber",
      "title": "Taminator: Extract Case Number",
      "category": "Taminator"
    },
    {
      "command": "taminator.checkConnection",
      "title": "Taminator: Check Connection",
      "category": "Taminator"
    },
    {
      "command": "taminator.openSettings",
      "title": "Taminator: Open Settings",
      "category": "Taminator"
    }
  ]
}
```

### Keybindings

```json
{
  "keybindings": [
    {
      "command": "taminator.analyzeEmail",
      "key": "ctrl+shift+t",
      "mac": "cmd+shift+t",
      "when": "editorTextFocus"
    },
    {
      "command": "taminator.extractCaseNumber",
      "key": "ctrl+shift+c",
      "mac": "cmd+shift+c",
      "when": "editorTextFocus"
    }
  ]
}
```

---

## Implementation Plan

### Phase 1: Core Extension (Week 1)

**Goals:**
- Basic extension scaffolding
- API client implementation
- Simple analyzer command

**Tasks:**
1. Initialize extension project
   ```bash
   npm install -g yo generator-code
   yo code  # Choose "New Extension (TypeScript)"
   ```

2. Create API client
   - HTTP client with axios
   - Type definitions for API responses
   - Error handling

3. Implement analyze command
   - Get selected text or clipboard
   - Call Taminator API
   - Display results in notification

**Deliverable:** Basic working extension that can analyze emails

### Phase 2: Webview Panel (Week 2)

**Goals:**
- Rich analyzer panel
- Results display with formatting
- Copy/save functionality

**Tasks:**
1. Create webview panel
   - HTML/CSS for analyzer
   - Email input textarea
   - Results display

2. Implement panel communication
   - Extension ↔ Webview messaging
   - State management

3. Add action buttons
   - Copy to clipboard
   - Save to history
   - Provide feedback

**Deliverable:** Full-featured analyzer panel

### Phase 3: Sidebar & History (Week 3)

**Goals:**
- Case history tree view
- Statistics display
- Case detail view

**Tasks:**
1. Create tree view provider
   - Recent cases list
   - Statistics summary
   - Settings link

2. Implement case detail view
   - Click on case → show details
   - View original email
   - Re-analyze option

3. Add refresh functionality
   - Auto-refresh on new analysis
   - Manual refresh button

**Deliverable:** Complete sidebar integration

### Phase 4: Polish & Features (Week 4)

**Goals:**
- Inline decorations
- Context menu integration
- Status bar
- Configuration

**Tasks:**
1. Email detection
   - Pattern matching for emails
   - Inline code lenses
   - Quick actions

2. Context menu
   - Right-click → Analyze
   - Extract case number
   - Check urgency

3. Status bar
   - Connection status
   - Quick stats
   - Click to open panel

4. Settings UI
   - Service URL configuration
   - Feature toggles
   - Default tags

**Deliverable:** Production-ready extension

---

## Testing Strategy

### Unit Tests

```typescript
// src/__tests__/api/taminator-client.test.ts
import { TaminatorClient } from '../api/taminator-client';

describe('TaminatorClient', () => {
  it('should analyze email', async () => {
    const client = new TaminatorClient('http://localhost:8080');
    const result = await client.analyzeEmail('test email');
    expect(result.case_number).toBeDefined();
  });
});
```

### Integration Tests

```typescript
// src/__tests__/commands/analyze.test.ts
import * as vscode from 'vscode';
import { analyzeEmailCommand } from '../commands/analyze';

describe('Analyze Command', () => {
  it('should analyze selected text', async () => {
    // Mock editor with selected text
    // Execute command
    // Verify results displayed
  });
});
```

### Manual Testing

**Test Cases:**
1. Install extension in Cursor IDE
2. Configure service URL
3. Open file with email content
4. Select email text
5. Run "Taminator: Analyze Email"
6. Verify results displayed correctly
7. Test all commands and features

---

## Distribution

### VS Code Marketplace

**Package Extension:**
```bash
npm install -g @vscode/vsce
vsce package
# Creates: taminator-intelligence-1.0.0.vsix
```

**Publish:**
```bash
vsce publish
```

### Manual Installation

**For testing:**
```bash
# Package extension
vsce package

# Install in Cursor IDE
code --install-extension taminator-intelligence-1.0.0.vsix
```

### GitHub Releases

**Automated release:**
```yaml
# .github/workflows/release.yml
name: Release Extension

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm run compile
      - run: vsce package
      - uses: actions/upload-artifact@v3
        with:
          name: extension
          path: '*.vsix'
```

---

## Benefits for TAMs

### 1. Seamless Workflow
- Analyze emails without leaving IDE
- No context switching
- Faster response times

### 2. Persistent History
- All analyses saved automatically
- Easy to reference past cases
- Track accuracy over time

### 3. Keyboard-Driven
- Quick keyboard shortcuts
- Command palette integration
- No mouse required

### 4. Customizable
- Configure service URL
- Toggle features on/off
- Set default tags

### 5. Offline-Capable
- Works with local Taminator service
- No cloud dependency
- Red Hat compliant

---

## Roadmap

### v1.0.0 - Core Features
- Email analysis command
- Webview panel
- Case history sidebar
- Basic configuration

### v1.1.0 - Enhanced UX
- Inline decorations
- Context menu integration
- Status bar
- Auto-detection

### v1.2.0 - Advanced Features
- Bulk analysis
- Custom rules editor
- Export/import data
- Team sharing (optional)

### v2.0.0 - Enterprise
- Multi-service support
- Advanced analytics
- Custom dashboards
- Integration with other TAM tools

---

## Technical Requirements

### Prerequisites

**Development:**
- Node.js 18+
- TypeScript 5+
- VS Code Extension API knowledge
- Cursor IDE for testing

**Runtime:**
- Taminator Intelligence service running (container or desktop)
- Network access to http://localhost:8080
- Cursor IDE or VS Code

### Dependencies

```json
{
  "dependencies": {
    "axios": "^1.6.0",
    "vscode": "^1.85.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/vscode": "^1.85.0",
    "@vscode/test-electron": "^2.3.0",
    "typescript": "^5.3.0",
    "@vscode/vsce": "^2.22.0"
  }
}
```

---

## Security Considerations

### Data Handling
- All data stays local (localhost communication)
- No external API calls
- Customer data never leaves TAM's machine
- Red Hat compliant

### Authentication
- Optional: API token for Taminator service
- Stored in VS Code secret storage
- Never in plain text

### Network
- Default: localhost only
- Optional: Configure remote Taminator service
- HTTPS support for remote connections

---

## Support & Documentation

### User Guide
- Installation instructions
- Configuration guide
- Feature walkthrough
- Troubleshooting

### Developer Guide
- Architecture overview
- API documentation
- Contributing guidelines
- Testing procedures

### Resources
- GitHub repository
- Issue tracker
- Discussion forum
- Video tutorials

---

## Next Steps

1. **Create extension project**
   ```bash
   cd /home/jbyrd/TAMINATOR
   mkdir cursor-extension
   cd cursor-extension
   npm init -y
   ```

2. **Set up TypeScript**
   ```bash
   npm install --save-dev typescript @types/vscode
   npx tsc --init
   ```

3. **Create basic structure**
   - package.json with extension manifest
   - src/extension.ts entry point
   - API client implementation

4. **Implement Phase 1**
   - Basic analyzer command
   - API integration
   - Test in Cursor IDE

---

**Built with ❤️ for Red Hat TAMs**  
**Bringing AI-powered intelligence directly into your IDE**

