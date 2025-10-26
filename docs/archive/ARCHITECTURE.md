# Taminator Architecture Documentation

**Product:** Taminator v1.10.0  
**Document Type:** Technical Architecture  
**Audience:** Developers, System Administrators, Technical Leaders  
**Last Updated:** October 25, 2025

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagrams](#architecture-diagrams)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Technology Stack](#technology-stack)
6. [Design Decisions](#design-decisions)
7. [Security Architecture](#security-architecture)
8. [Performance Considerations](#performance-considerations)

---

## System Overview

Taminator is a dual-interface (GUI + CLI) automation tool built on Electron and Python, designed to streamline Red Hat TAM workflows for RFE and Bug tracking.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
├─────────────────────────┬───────────────────────────────────────┤
│   Electron GUI App      │         Python CLI                    │
│   (Desktop Application) │         (tam-rfe command)             │
└────────────┬────────────┴───────────────┬───────────────────────┘
             │                            │
             │         IPC Bridge         │
             └────────────┬───────────────┘
                          │
             ┌────────────▼────────────┐
             │   Taminator Core        │
             │   (Python Backend)      │
             │                         │
             │  • Authentication       │
             │  • JIRA Integration     │
             │  • Portal Integration   │
             │  • Report Management    │
             │  • Customer Data        │
             └────────────┬────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼─────┐    ┌─────▼──────┐   ┌─────▼────────┐
   │   JIRA   │    │  Customer  │   │  Red Hat     │
   │   API    │    │  Portal    │   │  VPN         │
   │          │    │  API       │   │              │
   └──────────┘    └────────────┘   └──────────────┘
```

---

## Architecture Diagrams

### 1. Component Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Presentation Layer                        │
├──────────────────────────┬───────────────────────────────────────┤
│   Electron Renderer      │      CLI Interface                    │
│   ├─ HTML/CSS/JS        │      ├─ argparse (CLI router)         │
│   ├─ PatternFly UI      │      ├─ Rich (terminal formatting)    │
│   ├─ OOBE Wizard        │      └─ Click handlers                │
│   └─ Dashboard/Tabs     │                                        │
└──────────────────────────┴───────────────────────────────────────┘
                          │
                   IPC / subprocess
                          │
┌──────────────────────────▼───────────────────────────────────────┐
│                      Application Layer                           │
├──────────────────────────────────────────────────────────────────┤
│   Python Backend (taminator/)                                    │
│   ├─ commands/                                                   │
│   │   ├─ dashboard.py    (Customer overview + JIRA stats)       │
│   │   ├─ onboard.py      (Customer onboarding)                  │
│   │   ├─ check.py        (Report vs JIRA comparison)            │
│   │   ├─ update.py       (Report synchronization)               │
│   │   ├─ post.py         (Portal publishing)                    │
│   │   └─ config.py       (Token management)                     │
│   ├─ core/                                                       │
│   │   ├─ auth_box.py     (Authentication manager)               │
│   │   ├─ auth_types.py   (Token metadata)                       │
│   │   └─ jira_client.py  (JIRA API wrapper)                     │
│   └─ cli.py              (Command router)                        │
└──────────────────────────────────────────────────────────────────┘
                          │
                   HTTP/REST APIs
                          │
┌──────────────────────────▼───────────────────────────────────────┐
│                      Integration Layer                           │
├──────────────────────────┬───────────────────────────────────────┤
│   JIRA REST API          │   Customer Portal API                 │
│   • Search (JQL)         │   • Case queries                      │
│   • Issue details        │   • Group posting                     │
│   • Custom fields        │   • Attachment upload                 │
│   • Status tracking      │   • Access control                    │
└──────────────────────────┴───────────────────────────────────────┘
```

---

### 2. Data Flow - Check Workflow

```
User Action: "tam-rfe check jpmc"
     │
     ├─ CLI Router (cli.py) parses command
     │
     ├─ check.py loads customer metadata
     │   ├─ Read: ~/taminator-test-data/jpmc.md
     │   └─ Extract: account number, product, existing RFEs/Bugs
     │
     ├─ auth_box.get_token('jira-token')
     │   ├─ Check environment: $JIRA_TOKEN_API_TOKEN
     │   └─ Fallback: ~/.config/taminator/tokens.json
     │
     ├─ jira_client.query()
     │   ├─ Build JQL: account + SBR group filter
     │   ├─ HTTP GET → https://issues.redhat.com/rest/api/2/search
     │   └─ Parse response: issues[], custom fields
     │
     ├─ Compare: Saved report vs Live JIRA
     │   ├─ Match by issue key (AAP-12345)
     │   ├─ Detect status changes
     │   └─ Find case linkages
     │
     └─ Display results (Rich table format)
         ├─ Green: No changes
         ├─ Yellow: Status changes detected
         └─ Red: Errors or failures
```

---

### 3. OOBE Wizard Flow

```
┌─────────────┐
│   Launch    │
│  Taminator  │
└──────┬──────┘
       │
       ├─ Check: ~/.config/taminator-gui/oobe-state.json
       │
   ┌───▼────┐
   │ Exists?│
   └───┬────┘
       │
    NO │              YES
       │               └──> Skip OOBE, load Dashboard
       │
┌──────▼──────────┐
│  OOBE Screen 1  │
│   (Welcome)     │
│  • Feature demo │
│  • Value prop   │
└──────┬──────────┘
       │
┌──────▼──────────┐
│  OOBE Screen 2  │
│ (Auth Choice)   │
│  • Manual setup │
│  • Vault setup  │
└──────┬──────────┘
       │
┌──────▼──────────┐
│  OOBE Screen 3  │
│ (Token Config)  │
│  • JIRA token   │
│  • Portal token │
│  • Test tokens  │
└──────┬──────────┘
       │
┌──────▼──────────┐
│  OOBE Screen 4  │
│   (Customer)    │
│  • Add first    │
│  • Or skip      │
└──────┬──────────┘
       │
┌──────▼──────────┐
│  OOBE Screen 5  │
│  (Completion)   │
│  • Summary      │
│  • Finish       │
└──────┬──────────┘
       │
       └──> Save state, load Dashboard
```

---

### 4. Authentication Flow

```
┌───────────────────┐
│  Token Request    │
│  (JIRA, Portal)   │
└─────────┬─────────┘
          │
    ┌─────▼──────┐
    │ Check ENV  │
    │ Variables  │
    └─────┬──────┘
          │
       Found? ──YES──> Return token
          │
         NO
          │
    ┌─────▼──────┐
    │ Check File │
    │ tokens.json│
    └─────┬──────┘
          │
       Found? ──YES──> Return token
          │
         NO
          │
    ┌─────▼──────┐
    │   Error    │
    │ "Not       │
    │ configured"│
    └────────────┘
```

---

## Component Details

### Electron GUI (gui/)

**Purpose:** Desktop application interface

**Technology:**
- **Framework:** Electron 27.x
- **UI Library:** PatternFly 4.x (Red Hat design system)
- **IPC:** electron.ipcMain/ipcRenderer
- **Build Tool:** electron-builder

**Key Files:**
- `main.js` - Main process (window management, IPC handlers)
- `index.html` - Main application UI
- `oobe-wizard.html` - First-run wizard
- `oobe-state.js` - OOBE state management

**Responsibilities:**
1. Window lifecycle management
2. IPC communication with Python backend
3. User input validation
4. UI state management
5. Settings persistence

---

### Python Backend (src/taminator/)

**Purpose:** Core business logic and API integration

**Technology:**
- **Language:** Python 3.9+
- **HTTP Client:** requests 2.31+
- **CLI Framework:** argparse + Rich
- **Configuration:** JSON files

**Key Modules:**

#### `commands/dashboard.py`
- Aggregates customer data
- Queries JIRA for live stats
- Supports JSON output for GUI

#### `commands/check.py`
- Compares saved reports vs JIRA
- Detects status changes
- Identifies new/closed issues

#### `commands/update.py`
- Synchronizes reports with JIRA
- Creates automatic backups
- Preserves custom formatting

#### `commands/post.py`
- Publishes to Customer Portal
- Handles authentication
- Supports dry-run mode

#### `core/auth_box.py`
- Centralized token management
- Multi-source token resolution (ENV → file)
- Token validation

---

### External Integrations

#### JIRA API Integration

**Endpoint:** `https://issues.redhat.com/rest/api/2/search`  
**Authentication:** HTTP Basic Auth (username + API token)  
**Query Language:** JQL (JIRA Query Language)

**Example JQL Query:**
```jql
project in (AAP, AAPRFE, RHEL) 
AND "Red Hat Account" = 334224 
AND "SBR Group" = "SBR Ansible" 
AND status != Closed 
AND status != Done
```

**Response Format:**
```json
{
  "total": 12,
  "issues": [
    {
      "key": "AAP-12345",
      "fields": {
        "summary": "Feature request for X",
        "status": {"name": "In Progress"},
        "issuetype": {"name": "RFE"},
        "customfield_12316840": "03891234"  // Support case
      }
    }
  ]
}
```

---

#### Customer Portal API Integration

**Endpoint:** `https://api.access.redhat.com/rs/cases`  
**Authentication:** Bearer token  
**Purpose:** Case linkage verification, group posting

**Example Request:**
```bash
curl -H "Authorization: Bearer $TOKEN" \
  https://api.access.redhat.com/rs/cases?count=10
```

---

## Technology Stack

### Frontend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Electron** | 27.x | Desktop application framework |
| **Node.js** | 18.x LTS | JavaScript runtime |
| **PatternFly** | 4.x | Red Hat UI component library |
| **HTML5/CSS3** | - | Markup and styling |
| **Vanilla JavaScript** | ES6+ | UI logic (no framework overhead) |

### Backend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.9+ | Core business logic |
| **requests** | 2.31+ | HTTP client |
| **Rich** | 13.7+ | Terminal formatting |
| **argparse** | stdlib | CLI argument parsing |

### Build & Distribution

| Technology | Version | Purpose |
|------------|---------|---------|
| **electron-builder** | 24.x | AppImage, DMG, NSIS |
| **GitLab CI** | - | Linux builds, releases |
| **GitHub Actions** | - | Windows/macOS builds |
| **NSIS** | 3.x | Windows installer |

---

## Design Decisions

### Decision 1: Electron vs Native Apps

**Chosen:** Electron (cross-platform)

**Rationale:**
- ✅ Single codebase for Linux/macOS/Windows
- ✅ Rapid development with web technologies
- ✅ PatternFly integration (Red Hat design)
- ✅ Easy IPC with Python backend
- ❌ Larger binary size (acceptable trade-off)

**Alternatives Considered:**
- Native Qt/GTK (Linux-only, high development cost)
- Web app (requires server infrastructure)
- Java Swing (outdated, poor UX)

---

### Decision 2: Python Backend vs JavaScript

**Chosen:** Python backend with subprocess IPC

**Rationale:**
- ✅ Rich ecosystem for CLI tools (argparse, Rich)
- ✅ Mature HTTP/REST libraries (requests)
- ✅ TAMs familiar with Python
- ✅ Existing Red Hat Python tooling
- ❌ IPC overhead (negligible for our use case)

**Alternatives Considered:**
- Pure JavaScript (lacks Red Hat Python ecosystem)
- Go (overkill for CLI tool, learning curve)

---

### Decision 3: Token Storage Strategy

**Chosen:** Config file (`~/.config/taminator/tokens.json`) with chmod 600

**Rationale:**
- ✅ Simple, no external dependencies
- ✅ Same security model as aws-cli, gh, kubectl
- ✅ Easy backup and portability
- ✅ Environment variable override support
- ❌ Not OS keyring (over-engineered for our use case)

**Alternatives Considered:**
- OS Keyring (platform-specific, dependency issues)
- HashiCorp Vault (team use case, optional)
- Encrypted database (overkill)

---

### Decision 4: CLI/GUI Parity

**Chosen:** Full parity - every feature accessible via CLI and GUI

**Rationale:**
- ✅ Automation-friendly (cron, scripts)
- ✅ Choice for TAM preference
- ✅ Switch workflows mid-stream (tam-rfe gui)
- ✅ Red Hat CLI design pattern

**Implementation:**
- GUI calls CLI via subprocess
- CLI supports `--json` output for machine parsing
- CLI supports `--non-interactive` for automation

---

## Security Architecture

### Threat Model

| Threat | Mitigation |
|--------|------------|
| **Token Theft** | File permissions (chmod 600), environment variables |
| **Customer Data Leak** | No customer data in Git, .gitignore enforcement |
| **Man-in-the-Middle** | HTTPS only, Red Hat VPN required |
| **Code Injection** | Input validation, subprocess sanitization |
| **Secrets in Logs** | Token redaction in log output |

---

### Authentication Security

**Token Storage:**
- Location: `~/.config/taminator/tokens.json`
- Permissions: `0600` (owner read/write only)
- Format: JSON with service name keys

**Token Transmission:**
- JIRA API: HTTP Basic Auth over HTTPS
- Portal API: Bearer token over HTTPS
- No tokens in URL query parameters

**Environment Variables (Alternative):**
```bash
export JIRA_TOKEN_API_TOKEN="..."
export PORTAL_TOKEN_API_TOKEN="..."
```

---

### Network Security

**Required Endpoints:**
| Endpoint | Protocol | Port | Purpose |
|----------|----------|------|---------|
| `issues.redhat.com` | HTTPS | 443 | JIRA queries |
| `api.access.redhat.com` | HTTPS | 443 | Portal API |

**Firewall Rules:**
- Outbound HTTPS (443) required
- Red Hat VPN connection required
- No inbound connections needed

---

## Performance Considerations

### GUI Performance

**Startup Time:**
- Target: < 5 seconds (cold start)
- Actual: ~3 seconds on recommended hardware
- Bottleneck: Electron initialization

**Dashboard Load:**
- Target: < 3 seconds for 10 customers
- Actual: ~2 seconds with JIRA queries
- Bottleneck: JIRA API response time

**Optimization:**
- Lazy-load tabs (only active tab rendered)
- Cache JIRA responses (configurable TTL)
- Debounce user input (search, filters)

---

### CLI Performance

**Command Execution:**
| Command | Target | Actual | Notes |
|---------|--------|--------|-------|
| `tam-rfe config` | < 1s | ~0.5s | Local file read |
| `tam-rfe dashboard` | < 10s | ~5s | 5 customers, JIRA queries |
| `tam-rfe check` | < 5s | ~3s | Single JIRA query |
| `tam-rfe update` | < 5s | ~4s | File write + backup |
| `tam-rfe post` | < 10s | ~6s | Portal API call |

---

### Scalability

**Current Limits:**
- **Customers:** 50+ supported (tested with 10)
- **RFEs per Customer:** 100+ (JIRA default maxResults)
- **Concurrent Users:** Unlimited (local tool, no server)

**Future Optimizations:**
- Parallel JIRA queries (asyncio)
- Background refresh (systemd timer)
- Database caching (SQLite)

---

## File System Layout

```
~/.config/taminator/           # Configuration directory
├── tokens.json                # API tokens (chmod 600)
└── logs/                      # Application logs
    └── taminator.log

~/.config/taminator-gui/       # GUI-specific state
└── oobe-state.json            # OOBE completion tracking

~/taminator-test-data/         # Customer reports
├── jpmc.md                    # Customer report
├── jpmc.md.backup             # Automatic backup
└── test-customer.md           # Example customer

/opt/taminator/                # System-wide install (optional)
└── Taminator-1.10.0-x86_64.AppImage
```

---

## Monitoring & Observability

### Logging

**Log Levels:**
- `DEBUG` - Verbose output (enabled with `TAMINATOR_DEBUG=1`)
- `INFO` - Standard operations
- `WARNING` - Recoverable issues
- `ERROR` - Failures requiring attention

**Log Format:**
```
2025-10-25 10:30:45 [INFO] Dashboard: Loading customer data
2025-10-25 10:30:46 [INFO] JIRA Query: account=334224, product=Ansible
2025-10-25 10:30:48 [INFO] Found 12 open issues (8 RFEs, 4 Bugs)
```

---

### Metrics (Future)

**Planned Metrics:**
- Command execution time
- JIRA API response time
- Error rates by operation
- Customer report update frequency
- Token validation success rate

---

## Deployment Architecture

### Single-User Deployment

```
┌─────────────────────┐
│   User Workstation  │
│                     │
│  ┌───────────────┐ │
│  │  Taminator    │ │
│  │  (AppImage)   │ │
│  └───────┬───────┘ │
│          │         │
│  ┌───────▼───────┐ │
│  │ Local Config  │ │
│  │ tokens.json   │ │
│  └───────────────┘ │
└──────────┬──────────┘
           │
      Red Hat VPN
           │
   ┌───────▼────────┐
   │  JIRA / Portal │
   │      APIs      │
   └────────────────┘
```

---

### Team Deployment (with Vault)

```
┌─────────────────────┐     ┌─────────────────────┐
│  TAM Workstation 1  │     │  TAM Workstation 2  │
│  ┌───────────────┐  │     │  ┌───────────────┐  │
│  │  Taminator    │  │     │  │  Taminator    │  │
│  └───────┬───────┘  │     │  └───────┬───────┘  │
└──────────┼──────────┘     └──────────┼──────────┘
           │                           │
           └───────────┬───────────────┘
                       │
               ┌───────▼────────┐
               │ HashiCorp Vault│
               │  (Team Tokens) │
               └───────┬────────┘
                       │
                  Red Hat VPN
                       │
               ┌───────▼────────┐
               │  JIRA / Portal │
               │      APIs      │
               └────────────────┘
```

---

## Extension Points

### Future Architecture Enhancements

1. **Plugin System**
   - Custom report formatters
   - Additional API integrations
   - Custom workflows

2. **Database Layer**
   - SQLite for local caching
   - Query history
   - Offline mode support

3. **Web Dashboard**
   - Team-wide visibility
   - Metrics and analytics
   - Central reporting

4. **API Server Mode**
   - REST API for automation
   - Webhook support
   - Integration with other tools

---

**Document Version:** 1.0  
**Architecture Version:** v1.10.0  
**Status:** Current  
**Next Review:** Q1 2026

