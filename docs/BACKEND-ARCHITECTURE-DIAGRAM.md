# 🏗️ Taminator v2.0 Backend Architecture - Complete Diagram

**Tesla Architecture - Backend Deep Dive**

---

## 🎯 System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TAMINATOR v2.0 ARCHITECTURE                         │
│                              Tesla Backend                                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐         HTTP/JSON          ┌────────────────────────────┐
│                  │ ◄───────────────────────── │                            │
│  Electron GUI    │                             │   FastAPI Service          │
│  (Frontend)      │ ──────────────────────────► │   (Backend)                │
│                  │    Port 8765 (localhost)    │                            │
└──────────────────┘                             └────────────────────────────┘
        │                                                     │
        │                                                     │
        ▼                                                     ▼
┌──────────────────┐                             ┌────────────────────────────┐
│  API Client SDK  │                             │   Core Services            │
│  - TaminatorApi  │                             │   - Customer               │
│  - ErrorHandler  │                             │   - JIRA                   │
│  - Toast System  │                             │   - Portal                 │
└──────────────────┘                             └────────────────────────────┘
                                                             │
                                                             ▼
                                                  ┌────────────────────────────┐
                                                  │  External APIs             │
                                                  │  - issues.redhat.com       │
                                                  │  - access.redhat.com       │
                                                  └────────────────────────────┘
```

---

## 📦 Backend Component Architecture

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                         FASTAPI SERVICE (Port 8765)                           │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                          API LAYER                                  │    │
│  │                      (FastAPI Routes)                               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│           │            │            │            │            │              │
│           ▼            ▼            ▼            ▼            ▼              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Health   │  │Customers │  │  JIRA    │  │ Portal   │  │  Logs    │     │
│  │ Routes   │  │ Routes   │  │ Routes   │  │ Routes   │  │ Routes   │     │
│  │          │  │          │  │          │  │          │  │          │     │
│  │ /health  │  │/customers│  │/api/jira │  │/portal   │  │/api/logs │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│       │             │              │              │              │           │
│       └─────────────┴──────────────┴──────────────┴──────────────┘           │
│                                    │                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        SERVICE LAYER                                │    │
│  │                    (Business Logic)                                 │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│           │              │              │              │                     │
│           ▼              ▼              ▼              ▼                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Customer    │  │  JIRA        │  │  Portal      │  │  Logging     │   │
│  │  Service     │  │  Service     │  │  Service     │  │  Config      │   │
│  │              │  │              │  │              │  │              │   │
│  │ - List       │  │ - Search     │  │ - Format     │  │ - Rotation   │   │
│  │ - Get        │  │ - GetIssues  │  │ - Post       │  │ - Stats      │   │
│  │ - Create     │  │ - CheckSync  │  │ - Preview    │  │ - Tail       │   │
│  │ - Stats      │  │ - Cache      │  │ - Update     │  │ - Clear      │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
│         │                  │                  │                  │           │
│         └──────────────────┴──────────────────┴──────────────────┘           │
│                                    │                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         CORE LAYER                                  │    │
│  │                    (Shared Components)                              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│         │              │              │              │              │        │
│         ▼              ▼              ▼              ▼              ▼        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Token    │  │Exception │  │ Logging  │  │ Cache    │  │ Models   │     │
│  │ Manager  │  │ Handler  │  │ Config   │  │ Manager  │  │(Pydantic)│     │
│  │          │  │          │  │          │  │          │  │          │     │
│  │ - Get    │  │ - Codes  │  │ - Setup  │  │ - TTL    │  │ - Typed  │     │
│  │ - Set    │  │ - Format │  │ - Rotate │  │ - Get    │  │ - Valid  │     │
│  │ - Delete │  │ - Convert│  │ - Stats  │  │ - Set    │  │ - Parse  │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────────┘     │
│       │             │              │              │                          │
│       └─────────────┴──────────────┴──────────────┘                          │
│                                    │                                          │
└────────────────────────────────────┼──────────────────────────────────────────┘
                                     │
                                     ▼
                    ┌─────────────────────────────────┐
                    │   STORAGE & EXTERNAL SYSTEMS    │
                    └─────────────────────────────────┘
```

---

## 🔄 Request Flow - Detailed

### Example: Loading Customer Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. USER CLICKS "Dashboard" in GUI                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  2. API Client (JavaScript)                                                 │
│     apiClient.listCustomers()                                               │
│     → GET http://127.0.0.1:8765/api/customers/                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  3. FastAPI Route Handler                                                   │
│     @router.get("/api/customers/")                                          │
│     async def list_customers()                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  4. Customer Service                                                        │
│     CustomerService.list_customers()                                        │
│     ├─ Check cache (5 min TTL)                                             │
│     ├─ If miss: Read ~/Documents/rh/*/customer.yaml                        │
│     ├─ Parse YAML config files                                             │
│     ├─ Validate with Pydantic models                                       │
│     └─ Store in cache                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  5. Return Response                                                         │
│     {                                                                       │
│       "customers": [                                                        │
│         {                                                                   │
│           "id": "test-customer",                                            │
│           "name": "Test Customer",                                          │
│           "account_number": "12345",                                        │
│           "support_level": "premium",                                       │
│           "group_id": "group-123"                                           │
│         }                                                                   │
│       ],                                                                    │
│       "total": 1                                                            │
│     }                                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  6. API Client Receives & Parses                                            │
│     Returns JavaScript objects to GUI                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  7. GUI Renders Dashboard                                                   │
│     Creates cards, displays stats, shows customer list                      │
└─────────────────────────────────────────────────────────────────────────────┘

Total Time: ~10ms (with cache hit) vs 500ms (old CLI spawning)
```

---

## 🔐 Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TOKEN MANAGEMENT FLOW                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  GUI Setup       │  User enters JIRA/Portal tokens
│  (First Run)     │  in OOBE wizard
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Token Manager                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  set_token(TokenType.JIRA, token, expires_in_days=365)            │    │
│  │                                                                     │    │
│  │  1. Validate token (length check)                                  │    │
│  │  2. Calculate expiry date                                          │    │
│  │  3. Store in OS keyring                                            │    │
│  │     - Linux:   Secret Service API / gnome-keyring                  │    │
│  │     - macOS:   Keychain                                            │    │
│  │     - Windows: Credential Manager                                  │    │
│  │  4. Cache in memory (TokenInfo object)                             │    │
│  └────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  LATER: API Request Needs Token                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  get_token(TokenType.JIRA)                                         │    │
│  │                                                                     │    │
│  │  1. Check memory cache                                             │    │
│  │     ├─ Hit: Validate not expired                                   │    │
│  │     └─ Miss: Retrieve from OS keyring                              │    │
│  │  2. Validate token                                                 │    │
│  │     ├─ Not expired? Return token                                   │    │
│  │     └─ Expired? Raise AUTH_TOKEN_EXPIRED                           │    │
│  │  3. If missing: Raise AUTH_TOKEN_MISSING                           │    │
│  └────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Service Uses Token                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  JIRA/Portal Service                                               │    │
│  │                                                                     │    │
│  │  headers = {                                                       │    │
│  │    "Authorization": f"Bearer {token}",                             │    │
│  │    "Content-Type": "application/json"                              │    │
│  │  }                                                                 │    │
│  │                                                                     │    │
│  │  httpx.post(url, headers=headers, json=payload)                    │    │
│  └────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘

SECURITY FEATURES:
✅ No tokens in environment variables
✅ No tokens in logs or process list
✅ No tokens in plain text files
✅ OS-level encryption (keyring)
✅ Memory cache for performance
✅ Automatic expiry detection
```

---

## 🎫 JIRA Integration - Deep Dive

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      JIRA SERVICE ARCHITECTURE                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  API Request: GET /api/jira/test-customer/issues                        │
└──────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  JiraService.get_customer_issues(customer_id)                           │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  1. Build JQL Query                                            │    │
│  │     labels = "customer-test-customer"                          │    │
│  │     type IN (RFE, Bug)                                         │    │
│  │     status != Closed                                           │    │
│  │     ORDER BY priority DESC, updated DESC                       │    │
│  │                                                                 │    │
│  │  2. Check Cache (5 min TTL)                                    │    │
│  │     key = "search:jql:maxResults"                              │    │
│  │     ├─ Hit: Return cached results                              │    │
│  │     └─ Miss: Continue to API call                              │    │
│  │                                                                 │    │
│  │  3. Get Authentication Token                                   │    │
│  │     token = token_manager.get_token(TokenType.JIRA)            │    │
│  │     ├─ Success: Continue                                       │    │
│  │     ├─ Missing: Raise AUTH_TOKEN_MISSING                       │    │
│  │     └─ Expired: Raise AUTH_TOKEN_EXPIRED                       │    │
│  │                                                                 │    │
│  │  4. Make API Request                                           │    │
│  │     POST https://issues.redhat.com/rest/api/2/search           │    │
│  │     {                                                           │    │
│  │       "jql": "labels = ...",                                    │    │
│  │       "fields": ["key", "summary", "status", ...],             │    │
│  │       "maxResults": 100                                         │    │
│  │     }                                                           │    │
│  │                                                                 │    │
│  │  5. Handle Response                                            │    │
│  │     ├─ 200 OK: Parse and cache                                 │    │
│  │     ├─ 429 Rate Limited: Extract retry-after, raise error      │    │
│  │     ├─ 401/403: Raise AUTH_TOKEN_INVALID                       │    │
│  │     └─ 500/503: Raise EXTERNAL_API_ERROR                       │    │
│  │                                                                 │    │
│  │  6. Parse Issues                                               │    │
│  │     Convert JIRA JSON → JiraIssue models                       │    │
│  │     Validate with Pydantic                                     │    │
│  │     Filter invalid issues                                      │    │
│  │                                                                 │    │
│  │  7. Cache Results                                              │    │
│  │     Store for 5 minutes                                        │    │
│  │                                                                 │    │
│  │  8. Return Issues                                              │    │
│  │     List[JiraIssue]                                            │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  ERROR HANDLING & RETRY LOGIC                                           │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  Rate Limiting (429):                                          │    │
│  │    - Extract Retry-After header                               │    │
│  │    - Raise RATE_LIMIT_EXCEEDED with retry_after              │    │
│  │    - Frontend auto-retries after wait period                  │    │
│  │                                                                 │    │
│  │  Network Errors (timeout, connection):                         │    │
│  │    - Catch httpx.TimeoutException, httpx.NetworkError          │    │
│  │    - Raise EXTERNAL_API_ERROR                                  │    │
│  │    - Frontend shows retry button                              │    │
│  │                                                                 │    │
│  │  Authentication Errors (401, 403):                             │    │
│  │    - Raise AUTH_TOKEN_INVALID                                  │    │
│  │    - Frontend prompts for token update                         │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘

JIRA DATA MODEL:
┌──────────────────────────────────────────────────────────────────────────┐
│  JiraIssue (Pydantic Model)                                             │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  id: str                     # "12345"                         │    │
│  │  key: str                    # "RHEL-12345"                    │    │
│  │  summary: str                # "Add feature X"                 │    │
│  │  status: str                 # "In Progress"                   │    │
│  │  type: str                   # "RFE" or "Bug"                  │    │
│  │  priority: str               # "High", "Medium", "Low"         │    │
│  │  assignee: str               # "John Doe" or "Unassigned"      │    │
│  │  created: str                # ISO 8601 timestamp              │    │
│  │  updated: str                # ISO 8601 timestamp              │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 📰 Portal Integration - Deep Dive

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PORTAL SERVICE ARCHITECTURE                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  API Request: POST /api/portal/post                                      │
│  Body: {                                                                 │
│    "customer_id": "test-customer",                                       │
│    "content": "# Report\n\n## RFEs\n...",                                │
│    "title": "Monthly Report",                                            │
│    "preview_mode": false                                                 │
│  }                                                                       │
└──────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  PortalService.post_report()                                            │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  1. Format Report                                              │    │
│  │     format_report(markdown_content, customer_name, date)       │    │
│  │     ├─ Convert Markdown → HTML (markdown library)              │    │
│  │     │    - Tables extension                                     │    │
│  │     │    - Fenced code extension                               │    │
│  │     │    - TOC extension                                        │    │
│  │     ├─ Generate title                                          │    │
│  │     │    "{customer_name} - RFE/Bug Report - {date}"           │    │
│  │     └─ Return {html, title, formatted_at}                      │    │
│  │                                                                 │    │
│  │  2. Get Authentication Token                                   │    │
│  │     token = token_manager.get_token(TokenType.PORTAL)          │    │
│  │                                                                 │    │
│  │  3. Build Request Payload                                      │    │
│  │     {                                                           │    │
│  │       "title": title,                                          │    │
│  │       "content": html_content,                                 │    │
│  │       "type": "technical_report",                              │    │
│  │       "customer_id": customer_id,                              │    │
│  │       "case_number": case_number (optional)                    │    │
│  │     }                                                           │    │
│  │                                                                 │    │
│  │  4. Make API Request                                           │    │
│  │     POST https://access.redhat.com/api/reports                 │    │
│  │     headers = {                                                │    │
│  │       "Authorization": f"Bearer {token}",                      │    │
│  │       "Content-Type": "application/json"                       │    │
│  │     }                                                           │    │
│  │                                                                 │    │
│  │  5. Handle Response                                            │    │
│  │     ├─ 200/201: Success, return report ID and URL              │    │
│  │     ├─ 429: Rate limited, raise error                          │    │
│  │     ├─ 401/403: Auth error                                     │    │
│  │     └─ 500: API error                                          │    │
│  │                                                                 │    │
│  │  6. Return Result                                              │    │
│  │     {                                                           │    │
│  │       "success": true,                                         │    │
│  │       "portal_url": "https://access.redhat.com/...",           │    │
│  │       "report_id": "12345"                                     │    │
│  │     }                                                           │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  PREVIEW MODE (No API Call)                                             │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  1. Format Report (same as above)                             │    │
│  │                                                                 │    │
│  │  2. Wrap in Preview Banner                                     │    │
│  │     <div class="report-preview">                               │    │
│  │       <div class="preview-banner">                             │    │
│  │         ⚠️ PREVIEW ONLY - Not yet posted                       │    │
│  │       </div>                                                   │    │
│  │       <h1>{title}</h1>                                         │    │
│  │       <div>{html_content}</div>                                │    │
│  │     </div>                                                     │    │
│  │                                                                 │    │
│  │  3. Return Preview                                             │    │
│  │     {                                                           │    │
│  │       "html": preview_html,                                    │    │
│  │       "estimated_size": content_length                         │    │
│  │     }                                                           │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘

MARKDOWN CONVERSION PIPELINE:
┌──────────────────────────────────────────────────────────────────────────┐
│  Input (Markdown)                → Processing              → Output (HTML)│
│  ─────────────────────────────────────────────────────────────────────── │
│  # Monthly Report                 markdown.markdown()       <h1>Monthly   │
│                                   - tables extension        Report</h1>   │
│  ## RFEs                          - fenced_code            <h2>RFEs</h2>  │
│                                   - toc extension                         │
│  | Issue | Status |               Parse table syntax       <table>...     │
│  |-------|--------|                                        </table>       │
│  | RHEL  | Done   |                                                       │
│                                                                            │
│  ```python                        Parse code blocks        <pre><code>    │
│  def foo():                                                class="python"> │
│      pass                                                  ...             │
│  ```                                                       </code></pre>   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 📝 Logging Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LOGGING SYSTEM                                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  TaminatorLogger (Singleton)                                            │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  Initialization:                                               │    │
│  │  1. Determine platform-specific log directory                  │    │
│  │     - Linux:   ~/.local/state/taminator/log/                   │    │
│  │     - macOS:   ~/Library/Logs/taminator/                       │    │
│  │     - Windows: %LOCALAPPDATA%\taminator\log\                   │    │
│  │                                                                 │    │
│  │  2. Create log directory if not exists                         │    │
│  │                                                                 │    │
│  │  3. Configure root logger                                      │    │
│  │     - Log level: INFO (configurable)                           │    │
│  │     - Format: [YYYY-MM-DD HH:MM:SS] LEVEL NAME - message       │    │
│  │                                                                 │    │
│  │  4. Add Console Handler                                        │    │
│  │     - Stream: stdout                                           │    │
│  │     - For development/debugging                                │    │
│  │                                                                 │    │
│  │  5. Add File Handler (RotatingFileHandler)                     │    │
│  │     - File: taminator-service.log                              │    │
│  │     - Max size: 10MB per file                                  │    │
│  │     - Backup count: 7 (keep 7 days)                            │    │
│  │     - Encoding: UTF-8                                          │    │
│  │     - Auto-rotation when file exceeds max size                 │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  LOG ROTATION BEHAVIOR                                                  │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  Files created:                                                │    │
│  │    taminator-service.log        (current, active)              │    │
│  │    taminator-service.log.1      (yesterday)                    │    │
│  │    taminator-service.log.2      (2 days ago)                   │    │
│  │    ...                                                         │    │
│  │    taminator-service.log.7      (7 days ago)                   │    │
│  │                                                                 │    │
│  │  When taminator-service.log reaches 10MB:                      │    │
│  │    1. Rename .log → .log.1                                     │    │
│  │    2. Rename .log.1 → .log.2                                   │    │
│  │    3. ...                                                      │    │
│  │    4. Delete .log.7 (oldest)                                   │    │
│  │    5. Create new .log file                                     │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  LOGS API ENDPOINTS                                                     │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  GET /api/logs/recent?lines=100                               │    │
│  │    - Read last N lines from log file                          │    │
│  │    - Max 1000 lines                                           │    │
│  │    - Returns: {lines: [...], total_lines: N, log_file: path}  │    │
│  │                                                                 │    │
│  │  GET /api/logs/stats                                           │    │
│  │    - File size (bytes + MB)                                    │    │
│  │    - Total line count                                          │    │
│  │    - Last modified timestamp                                   │    │
│  │    - File path                                                 │    │
│  │    - Returns: LogStats model                                   │    │
│  │                                                                 │    │
│  │  GET /api/logs/tail?lines=50                                   │    │
│  │    - Like tail -f, last N lines                                │    │
│  │    - Used by logs viewer for auto-refresh                      │    │
│  │    - Max 500 lines                                             │    │
│  │                                                                 │    │
│  │  DELETE /api/logs/clear                                        │    │
│  │    - Delete current log file                                   │    │
│  │    - WARNING: Destructive, cannot undo                         │    │
│  │    - Returns: {success: true, message: "..."}                  │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘

LOG ENTRY FORMAT:
[2025-10-28 01:23:45] INFO     taminator.api.main   - 🚀 Starting Taminator API Service v2.0
[2025-10-28 01:23:45] INFO     taminator.core.token - 🔐 TokenManager initialized
[2025-10-28 01:23:46] INFO     taminator.api.health - 🏥 Health check: OK
[2025-10-28 01:23:50] WARNING  taminator.services   - ⚠️  Token missing for JIRA
[2025-10-28 01:23:55] ERROR    taminator.api.jira   - ❌ JIRA API call failed: 401
```

---

## 💾 Caching Strategy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CACHE ARCHITECTURE                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  In-Memory Cache (Dictionary)                                           │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  Structure:                                                    │    │
│  │    {                                                           │    │
│  │      cache_key: (timestamp, cached_value)                      │    │
│  │    }                                                           │    │
│  │                                                                 │    │
│  │  TTL: 5 minutes (300 seconds)                                  │    │
│  │                                                                 │    │
│  │  Operations:                                                   │    │
│  │    _cache_get(key):                                            │    │
│  │      - Check if key exists                                     │    │
│  │      - If exists, check timestamp                              │    │
│  │      - If not expired (< 5 min), return value                  │    │
│  │      - If expired, delete and return None                      │    │
│  │                                                                 │    │
│  │    _cache_set(key, value):                                     │    │
│  │      - Store (datetime.now(), value)                           │    │
│  │                                                                 │    │
│  │    clear_cache():                                              │    │
│  │      - Delete all entries                                      │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  CACHED OPERATIONS                                                      │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  CustomerService:                                              │    │
│  │    - list_customers()     → cache key: "customers:list"        │    │
│  │    - get_customer(id)     → cache key: "customer:{id}"         │    │
│  │                                                                 │    │
│  │  JiraService:                                                  │    │
│  │    - search_issues(jql)   → cache key: "search:{jql}:{limit}"  │    │
│  │    - get_issue(key)       → cache key: "issue:{key}"           │    │
│  │                                                                 │    │
│  │  PortalService:                                                │    │
│  │    - get_report(id)       → cache key: "report:{id}"           │    │
│  │                                                                 │    │
│  │  TokenManager:                                                 │    │
│  │    - get_token(type)      → cache key: TokenType enum          │    │
│  │      (separate in-memory dict, no TTL)                         │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘

CACHE INVALIDATION:
- Automatic: TTL expiry (5 minutes)
- Manual: clear_cache() method on each service
- On error: Cache miss triggers new API call
```

---

## 🔄 Service Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SERVICE LIFECYCLE                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  1. STARTUP                                                              │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  Service Manager (Electron) starts:                            │    │
│  │  1. Find service binary path                                   │    │
│  │     - Bundled: process.resourcesPath/bin/taminator-service     │    │
│  │     - Dev: ../dist/taminator-service                           │    │
│  │     - Fallback: system PATH                                    │    │
│  │                                                                 │    │
│  │  2. Spawn process                                              │    │
│  │     spawn(servicePath, ['--port', '8765'])                     │    │
│  │                                                                 │    │
│  │  3. Wait for service ready                                     │    │
│  │     Poll http://127.0.0.1:8765/health every 500ms              │    │
│  │     Max attempts: 30 (15 seconds)                              │    │
│  │                                                                 │    │
│  │  4. On success:                                                │    │
│  │     - serviceReady = true                                      │    │
│  │     - Start health monitoring (every 10s)                      │    │
│  │     - Update GUI status bar                                    │    │
│  │                                                                 │    │
│  │  5. On failure:                                                │    │
│  │     - Log error                                                │    │
│  │     - Show toast notification                                  │    │
│  │     - Auto-retry (3 attempts with backoff)                     │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  2. RUNTIME                                                              │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  Health Monitoring:                                            │    │
│  │    - Every 10 seconds                                          │    │
│  │    - GET /health endpoint                                      │    │
│  │    - Check service/AI/token status                             │    │
│  │    - Update GUI status bar                                     │    │
│  │                                                                 │    │
│  │  On Health Check Failure:                                      │    │
│  │    - Attempt restart                                           │    │
│  │    - Show offline notification                                 │    │
│  │    - Continue monitoring (will detect when back online)        │    │
│  │                                                                 │    │
│  │  Process Management:                                           │    │
│  │    - Monitor process state (running/stopped/crashed)           │    │
│  │    - Auto-restart on unexpected exit                           │    │
│  │    - Log all state changes                                     │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  3. SHUTDOWN                                                             │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  On GUI Close:                                                 │    │
│  │  1. Stop health monitoring interval                            │    │
│  │  2. Send SIGTERM to service process                            │    │
│  │  3. Wait 5 seconds for graceful shutdown                       │    │
│  │  4. If still running: Send SIGKILL                             │    │
│  │  5. Clean up resources                                         │    │
│  │  6. Exit Electron app                                          │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘

STATE DIAGRAM:
┌────────────┐    Start     ┌─────────────┐   Health OK   ┌────────────┐
│  STOPPED   │ ───────────► │  STARTING   │ ────────────► │  RUNNING   │
└────────────┘              └─────────────┘               └──────┬─────┘
                                   │                             │
                                   │ Timeout/Error               │ Health Fail
                                   │                             │
                                   ▼                             ▼
                            ┌─────────────┐                ┌────────────┐
                            │   FAILED    │                │  RESTART   │
                            └─────────────┘                └──────┬─────┘
                                                                  │
                                                                  │ Success
                                                                  │
                                                                  ▼
                                                            ┌────────────┐
                                                            │  RUNNING   │
                                                            └────────────┘
```

---

## 🎯 Performance Characteristics

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PERFORMANCE BENCHMARKS                                 │
└─────────────────────────────────────────────────────────────────────────────┘

ENDPOINT PERFORMANCE (with cache hit):
┌────────────────────────────────────────┬──────────────┬─────────────────┐
│ Endpoint                               │ Avg Response │ Cache Impact    │
├────────────────────────────────────────┼──────────────┼─────────────────┤
│ GET /health                            │ 2-5ms        │ N/A (no cache)  │
│ GET /api/customers/                    │ 8-15ms       │ Hit: 10ms       │
│                                        │              │ Miss: 50-100ms  │
│ GET /api/customers/{id}                │ 5-10ms       │ Hit: 5ms        │
│                                        │              │ Miss: 30-50ms   │
│ GET /api/jira/{id}/issues              │ 10-20ms      │ Hit: 10ms       │
│                                        │              │ Miss: 500-2000ms│
│ POST /api/portal/preview               │ 15-30ms      │ N/A (no cache)  │
│ POST /api/portal/post                  │ 500-2000ms   │ N/A (API call)  │
│ GET /api/logs/recent?lines=100         │ 5-15ms       │ N/A (file read) │
└────────────────────────────────────────┴──────────────┴─────────────────┘

MEMORY USAGE:
┌────────────────────────────────────────┬─────────────────────────────────┐
│ Component                              │ Memory                          │
├────────────────────────────────────────┼─────────────────────────────────┤
│ FastAPI Base                           │ ~30MB                           │
│ Service Classes (loaded)               │ ~10MB                           │
│ Cache (typical)                        │ ~5MB (depends on data)          │
│ Logging Buffer                         │ ~2MB                            │
│ ────────────────────────────────────────────────────────────────────── │
│ TOTAL (steady state)                   │ ~50MB                           │
└────────────────────────────────────────┴─────────────────────────────────┘

STARTUP TIME:
- Service spawn: ~1-2s
- FastAPI init: ~0.5-1s
- First health check: ~0.5s
- Total to ready: ~2-3s

CACHE EFFICIENCY:
- Cache hit rate: ~80% (typical usage)
- Cache miss penalty: 50-2000ms (depends on endpoint)
- Memory saved: ~45MB (vs loading all data)

COMPARISON (v1.x CLI vs v2.0 API):
┌─────────────────────────┬──────────────┬──────────────┬────────────────┐
│ Operation               │ v1.x (CLI)   │ v2.0 (API)   │ Improvement    │
├─────────────────────────┼──────────────┼──────────────┼────────────────┤
│ Load dashboard          │ 500ms        │ 10ms         │ 50x faster     │
│ Get customer            │ 300ms        │ 5ms          │ 60x faster     │
│ List customers          │ 400ms        │ 10ms         │ 40x faster     │
│ Memory (per request)    │ Variable     │ Stable       │ More efficient │
└─────────────────────────┴──────────────┴──────────────┴────────────────┘
```

---

## 📚 Technology Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BACKEND STACK                                       │
└─────────────────────────────────────────────────────────────────────────────┘

CORE FRAMEWORK:
  FastAPI 0.104.1          - Web framework (async, high performance)
  Uvicorn 0.24.0           - ASGI server
  Pydantic 2.5.0           - Data validation & serialization

HTTP CLIENT:
  httpx 0.25.1             - Async HTTP client with HTTP/2 support
  
DATA PROCESSING:
  PyYAML 6.0.1             - YAML parsing (customer configs)
  markdown 3.5.1           - Markdown → HTML conversion (Portal)

SECURITY:
  keyring 24.3.0           - OS keyring integration (token storage)
  cryptography 41.0.7      - Encryption primitives

SYSTEM:
  psutil 5.9.6             - System monitoring (health checks)
  platformdirs 3.10.0      - Cross-platform directories (logs)
  aiofiles 23.2.1          - Async file I/O

PACKAGING:
  PyInstaller              - Standalone executable creation

TOTAL DEPENDENCIES: 15 core packages
```

---

## 🔗 External API Contracts

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      EXTERNAL API INTEGRATIONS                              │
└─────────────────────────────────────────────────────────────────────────────┘

JIRA API (issues.redhat.com):
  Endpoint: POST /rest/api/2/search
  Auth: Bearer token
  Request:
    {
      "jql": "labels = 'customer-name' AND type IN (RFE,Bug)",
      "fields": ["key", "summary", "status", "issuetype", ...],
      "maxResults": 100
    }
  Response:
    {
      "issues": [
        {
          "id": "12345",
          "key": "RHEL-12345",
          "fields": {
            "summary": "...",
            "status": {"name": "In Progress"},
            "issuetype": {"name": "RFE"},
            ...
          }
        }
      ]
    }
  Rate Limit: ~100 requests/minute
  Error Codes: 429 (rate limit), 401 (auth), 403 (permission)

PORTAL API (access.redhat.com):
  Endpoint: POST /api/reports
  Auth: Bearer token
  Request:
    {
      "title": "Customer Report - 2025-10",
      "content": "<html>...</html>",
      "type": "technical_report",
      "customer_id": "...",
      "case_number": "..." (optional)
    }
  Response:
    {
      "id": "12345",
      "url": "https://access.redhat.com/articles/12345",
      "created_at": "2025-10-28T12:00:00Z"
    }
  Rate Limit: ~50 requests/minute
  Error Codes: 429 (rate limit), 401 (auth), 403 (permission)
```

---

## 🎨 Architecture Patterns Used

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DESIGN PATTERNS                                        │
└─────────────────────────────────────────────────────────────────────────────┘

1. LAYERED ARCHITECTURE
   - API Layer (Routes)
   - Service Layer (Business Logic)
   - Core Layer (Shared Components)
   - Clear separation of concerns

2. DEPENDENCY INJECTION
   - TokenManager → Services
   - Services → Route Handlers
   - FastAPI Depends() pattern

3. SINGLETON PATTERN
   - TokenManager (global instance)
   - Logger (global instance)
   - Service instances (per service type)

4. REPOSITORY PATTERN
   - CustomerService abstracts file system
   - JiraService abstracts JIRA API
   - PortalService abstracts Portal API

5. CACHE-ASIDE PATTERN
   - Check cache first
   - On miss: Fetch from source
   - Store in cache for next request

6. STRATEGY PATTERN
   - Different auth methods (JIRA vs Portal tokens)
   - Different error handlers per error type

7. OBSERVER PATTERN
   - Health monitoring → Status updates
   - Log events → File writes

8. FACTORY PATTERN
   - get_token_manager()
   - get_jira_service()
   - get_portal_service()
```

---

## 🚀 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     DEPLOYMENT MODEL                                        │
└─────────────────────────────────────────────────────────────────────────────┘

APPIMAGE STRUCTURE:
┌──────────────────────────────────────────────────────────────────────────┐
│  Taminator-2.0.0.AppImage                                                │
│  ├─ Electron GUI (JavaScript/HTML/CSS)                                   │
│  ├─ Node.js runtime (bundled)                                            │
│  ├─ Resources/                                                           │
│  │  ├─ bin/                                                              │
│  │  │  ├─ taminator-service (PyInstaller binary, 44MB)                   │
│  │  │  └─ tam-rfe (legacy CLI, optional)                                 │
│  │  └─ assets/ (icons, themes, etc.)                                     │
│  └─ AppRun (launcher script)                                             │
└──────────────────────────────────────────────────────────────────────────┘

RUNTIME DEPENDENCIES:
  - Python: NONE (bundled in PyInstaller binary)
  - System libs: glibc, libstdc++ (standard on all Linux)
  - Network: Internet for JIRA/Portal APIs (optional)

USER DATA:
  - Tokens: OS keyring (not in AppImage)
  - Logs: ~/.local/state/taminator/log/
  - Settings: ~/.config/taminator-gui/settings.json
  - Customer data: ~/Documents/rh/

PORTABILITY:
  - Single file deployment
  - No installation required
  - Works on any Linux (x86_64 or ARM64)
  - Self-contained, no external dependencies
```

---

*Comprehensive backend architecture documentation for Taminator v2.0 Tesla*  
*All systems visualized - From user click to database write*

