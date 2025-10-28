# Taminator v2.0 - Architecture Redesign

## Problem Statement

**Users keep hitting bugs very quickly after trying to use it.**

### Root Causes (Current Architecture)

```
Current v1.x Architecture:
┌─────────────┐
│ Electron GUI│  ← Single point of failure
└──────┬──────┘
       │ spawn('tam-rfe', args)  ← Unreliable process spawning
       │ parse stdout/stderr     ← Brittle text parsing
       ▼
┌─────────────┐
│ CLI Binary  │  ← Reloads everything on each call
└─────────────┘
```

**Why it breaks:**
1. ❌ **Process spawning fails** → "spawn tam-rfe ENOENT"
2. ❌ **Path hardcoding** → Breaks for different users
3. ❌ **No state management** → "Home tab loading issue"
4. ❌ **Race conditions** → Blank pages, timing issues
5. ❌ **Text parsing breaks** → Format changes cause crashes
6. ❌ **No error boundaries** → One error breaks everything
7. ❌ **No validation** → Errors happen after user clicks, not before

---

## Solution: Service-Based Architecture

### New v2.0 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Electron GUI (Renderer)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │  Check   │  │  Update  │  │   Post   │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       └──────────────┴─────────────┴──────────────┘         │
│                           │                                  │
│                    ┌──────▼──────┐                          │
│                    │ API Client  │  TypeScript SDK          │
│                    │  (axios)    │  Auto-generated          │
│                    └──────┬──────┘                          │
└───────────────────────────┼─────────────────────────────────┘
                            │
                     HTTP + WebSocket
                     (localhost:8765)
                            │
┌───────────────────────────┼─────────────────────────────────┐
│              FastAPI Service (Python Backend)               │
│                           │                                  │
│  ┌────────────────────────▼────────────────────────┐        │
│  │              API Layer (Endpoints)              │        │
│  │  /api/customers/                                │        │
│  │  /api/jira/                                     │        │
│  │  /api/portal/                                   │        │
│  │  /ws  (WebSocket for real-time)                │        │
│  └────────────────────┬────────────────────────────┘        │
│                       │                                      │
│  ┌────────────────────▼────────────────────────────┐        │
│  │           Service Layer (Business Logic)        │        │
│  │  ┌──────────────┐  ┌──────────────┐            │        │
│  │  │  Customer    │  │    JIRA      │            │        │
│  │  │  Service     │  │   Service    │            │        │
│  │  └──────┬───────┘  └──────┬───────┘            │        │
│  │  ┌──────▼───────┐  ┌──────▼───────┐            │        │
│  │  │   Portal     │  │    Report    │            │        │
│  │  │   Service    │  │   Service    │            │        │
│  │  └──────────────┘  └──────────────┘            │        │
│  └────────────────────┬────────────────────────────┘        │
│                       │                                      │
│  ┌────────────────────▼────────────────────────────┐        │
│  │        Core Infrastructure Layer                │        │
│  │  ┌──────────────┐  ┌──────────────┐            │        │
│  │  │    Token     │  │    Config    │            │        │
│  │  │   Manager    │  │   Manager    │            │        │
│  │  └──────────────┘  └──────────────┘            │        │
│  │  ┌──────────────┐  ┌──────────────┐            │        │
│  │  │    Cache     │  │     Logs     │            │        │
│  │  │   Manager    │  │   Manager    │            │        │
│  │  └──────────────┘  └──────────────┘            │        │
│  └─────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Plan

### Phase 1: Service Foundation (Week 1)

#### Day 1-2: FastAPI Service Skeleton
```bash
src/taminator/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── dependencies.py      # Dependency injection
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── customers.py     # Customer endpoints
│   │   ├── jira.py          # JIRA endpoints
│   │   ├── portal.py        # Portal endpoints
│   │   └── health.py        # Health checks
│   └── websocket.py         # WebSocket handlers
```

**Deliverable:**
```python
# src/taminator/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Taminator API", version="2.0.0")

# Allow Electron GUI to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

# More endpoints...
```

#### Day 3-4: Service Layer
```bash
src/taminator/
├── services/
│   ├── __init__.py
│   ├── customer_service.py  # Customer operations
│   ├── jira_service.py      # JIRA API wrapper
│   ├── portal_service.py    # Portal API wrapper
│   └── report_service.py    # Report generation
```

**Deliverable:**
```python
# src/taminator/services/customer_service.py
from typing import List, Optional
from ..models import Customer
from ..core.config_manager import ConfigManager

class CustomerService:
    def __init__(self, config: ConfigManager):
        self.config = config
        self._cache = {}
    
    async def list_customers(self) -> List[Customer]:
        """Get all customers (cached)"""
        if 'customers' in self._cache:
            return self._cache['customers']
        
        customers = self.config.get_customers()
        self._cache['customers'] = customers
        return customers
    
    async def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get single customer"""
        customers = await self.list_customers()
        return next((c for c in customers if c.id == customer_id), None)
    
    async def add_customer(self, customer: Customer) -> Customer:
        """Add new customer"""
        self.config.add_customer(customer)
        self._cache.clear()  # Invalidate cache
        return customer
```

#### Day 5: Core Infrastructure
```bash
src/taminator/
├── core/
│   ├── token_manager.py     # Secure token storage
│   ├── config_manager.py    # Configuration handling
│   ├── cache_manager.py     # Smart caching
│   └── error_handler.py     # Structured errors
```

**Deliverable:**
```python
# src/taminator/core/token_manager.py
import keyring
from typing import Optional
from enum import Enum

class TokenType(str, Enum):
    JIRA = "jira"
    PORTAL = "portal"

class TokenManager:
    SERVICE_NAME = "taminator"
    
    def get_token(self, token_type: TokenType) -> Optional[str]:
        """Get token from secure storage"""
        return keyring.get_password(self.SERVICE_NAME, token_type.value)
    
    def set_token(self, token_type: TokenType, token: str):
        """Store token securely"""
        keyring.set_password(self.SERVICE_NAME, token_type.value, token)
    
    def delete_token(self, token_type: TokenType):
        """Remove token"""
        keyring.delete_password(self.SERVICE_NAME, token_type.value)
    
    def has_token(self, token_type: TokenType) -> bool:
        """Check if token exists"""
        return self.get_token(token_type) is not None
```

---

### Phase 2: API Endpoints (Week 2)

#### Customer Management API
```python
# src/taminator/api/routes/customers.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...services.customer_service import CustomerService
from ...models import Customer, CustomerCreate
from ..dependencies import get_customer_service

router = APIRouter(prefix="/api/customers", tags=["customers"])

@router.get("/", response_model=List[Customer])
async def list_customers(
    service: CustomerService = Depends(get_customer_service)
):
    """Get all customers"""
    return await service.list_customers()

@router.get("/{customer_id}", response_model=Customer)
async def get_customer(
    customer_id: str,
    service: CustomerService = Depends(get_customer_service)
):
    """Get customer by ID"""
    customer = await service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/", response_model=Customer, status_code=201)
async def create_customer(
    customer: CustomerCreate,
    service: CustomerService = Depends(get_customer_service)
):
    """Add new customer"""
    return await service.add_customer(customer)

@router.get("/{customer_id}/dashboard")
async def get_dashboard(
    customer_id: str,
    service: CustomerService = Depends(get_customer_service)
):
    """Get customer dashboard data"""
    customer = await service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Return structured dashboard data
    return {
        "customer": customer,
        "stats": await service.get_stats(customer_id),
        "recent_activity": await service.get_recent_activity(customer_id)
    }
```

#### JIRA Integration API
```python
# src/taminator/api/routes/jira.py
from fastapi import APIRouter, Depends, BackgroundTasks
from ...services.jira_service import JiraService
from ...models import JiraCheckResult, JiraUpdateRequest
from ..dependencies import get_jira_service
from ..websocket import broadcast_progress

router = APIRouter(prefix="/api/jira", tags=["jira"])

@router.post("/{customer_id}/check", response_model=JiraCheckResult)
async def check_jira_status(
    customer_id: str,
    background_tasks: BackgroundTasks,
    service: JiraService = Depends(get_jira_service)
):
    """
    Check JIRA for status changes
    Returns mismatches between saved report and current JIRA state
    """
    # Use background task for progress updates
    background_tasks.add_task(
        broadcast_progress,
        "Fetching JIRA issues...",
        0.2
    )
    
    result = await service.check_customer(customer_id)
    
    background_tasks.add_task(
        broadcast_progress,
        f"Found {len(result.mismatches)} mismatches",
        1.0
    )
    
    return result

@router.post("/{customer_id}/update")
async def update_from_jira(
    customer_id: str,
    request: JiraUpdateRequest,
    service: JiraService = Depends(get_jira_service)
):
    """
    Update report with current JIRA data
    Creates backup and updates the report file
    """
    result = await service.update_customer_report(
        customer_id,
        dry_run=request.dry_run
    )
    return result
```

#### Error Handling (Critical!)
```python
# src/taminator/core/error_handler.py
from enum import Enum
from typing import Optional

class ErrorCode(str, Enum):
    # Authentication
    AUTH_TOKEN_MISSING = "auth_token_missing"
    AUTH_TOKEN_EXPIRED = "auth_token_expired"
    AUTH_TOKEN_INVALID = "auth_token_invalid"
    
    # Customer
    CUSTOMER_NOT_FOUND = "customer_not_found"
    CUSTOMER_INVALID_CONFIG = "customer_invalid_config"
    
    # JIRA
    JIRA_API_ERROR = "jira_api_error"
    JIRA_RATE_LIMIT = "jira_rate_limit"
    
    # Portal
    PORTAL_API_ERROR = "portal_api_error"
    PORTAL_UNAUTHORIZED = "portal_unauthorized"
    
    # File System
    FILE_NOT_FOUND = "file_not_found"
    FILE_PERMISSION_DENIED = "file_permission_denied"

class TaminatorException(Exception):
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        details: Optional[dict] = None,
        retry_after: Optional[int] = None
    ):
        self.code = code
        self.message = message
        self.details = details or {}
        self.retry_after = retry_after
        super().__init__(message)
    
    def to_dict(self):
        return {
            "error": {
                "code": self.code.value,
                "message": self.message,
                "details": self.details,
                "retry_after": self.retry_after
            }
        }

# Usage in services:
if not token_manager.has_token(TokenType.JIRA):
    raise TaminatorException(
        code=ErrorCode.AUTH_TOKEN_MISSING,
        message="JIRA token not configured",
        details={"field": "jira_token", "help_url": "/docs/auth"}
    )
```

---

### Phase 3: GUI API Client (Week 3)

#### TypeScript API Client
```bash
gui/
├── src/                     # New: TypeScript source
│   ├── api/
│   │   ├── client.ts        # Main API client
│   │   ├── customers.ts     # Customer endpoints
│   │   ├── jira.ts          # JIRA endpoints
│   │   ├── portal.ts        # Portal endpoints
│   │   └── websocket.ts     # WebSocket client
│   └── types/
│       └── api.ts           # TypeScript types
```

**Deliverable:**
```typescript
// gui/src/api/client.ts
import axios, { AxiosInstance } from 'axios';

export class TaminatorClient {
  private client: AxiosInstance;
  private ws: WebSocket | null = null;
  
  constructor(baseURL: string = 'http://localhost:8765') {
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    // Setup error interceptor
    this.client.interceptors.response.use(
      response => response,
      error => this.handleError(error)
    );
  }
  
  private handleError(error: any) {
    if (error.response?.data?.error) {
      const apiError = error.response.data.error;
      // Convert API error to user-friendly message
      throw new TaminatorAPIError(
        apiError.code,
        apiError.message,
        apiError.details,
        apiError.retry_after
      );
    }
    throw error;
  }
  
  // Customer operations
  async listCustomers(): Promise<Customer[]> {
    const response = await this.client.get('/api/customers/');
    return response.data;
  }
  
  async getCustomer(customerId: string): Promise<Customer> {
    const response = await this.client.get(`/api/customers/${customerId}`);
    return response.data;
  }
  
  async createCustomer(customer: CustomerCreate): Promise<Customer> {
    const response = await this.client.post('/api/customers/', customer);
    return response.data;
  }
  
  // JIRA operations
  async checkJiraStatus(customerId: string): Promise<JiraCheckResult> {
    const response = await this.client.post(`/api/jira/${customerId}/check`);
    return response.data;
  }
  
  // WebSocket for real-time updates
  connectWebSocket(onProgress: (message: string, percent: number) => void) {
    this.ws = new WebSocket('ws://localhost:8765/ws');
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onProgress(data.message, data.percent);
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }
  
  disconnectWebSocket() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

// Singleton instance
export const taminatorClient = new TaminatorClient();
```

#### GUI Integration (Replace spawn() calls)
```javascript
// OLD (v1.x) - Process spawning
async function checkCustomer(customerId) {
  const process = spawn('tam-rfe', ['check', '--customer', customerId]);
  // Parse stdout, hope for the best...
}

// NEW (v2.0) - API client
async function checkCustomer(customerId) {
  try {
    // Connect WebSocket for progress
    taminatorClient.connectWebSocket((message, percent) => {
      updateProgressBar(message, percent);
    });
    
    // Make API call
    const result = await taminatorClient.checkJiraStatus(customerId);
    
    // Display structured results
    displayCheckResults(result);
    
  } catch (error) {
    if (error.code === 'auth_token_expired') {
      showTokenRefreshDialog('jira');
    } else if (error.code === 'jira_rate_limit') {
      showRateLimitError(error.retry_after);
    } else {
      showGenericError(error.message);
    }
  } finally {
    taminatorClient.disconnectWebSocket();
  }
}
```

---

### Phase 4: Service Lifecycle Management

#### Auto-Start Service with Electron
```javascript
// gui/main.js - Service management
const { spawn } = require('child_process');
const axios = require('axios');

class ServiceManager {
  constructor() {
    this.serviceProcess = null;
    this.serviceUrl = 'http://localhost:8765';
  }
  
  async start() {
    // Check if service is already running
    if (await this.isHealthy()) {
      console.log('[Service] Already running');
      return;
    }
    
    // Start service as child process
    const servicePath = app.isPackaged
      ? path.join(process.resourcesPath, 'bin', 'taminator-service')
      : path.join(__dirname, '../bin/taminator-service');
    
    this.serviceProcess = spawn(servicePath, ['--port', '8765'], {
      stdio: 'pipe',
      detached: false
    });
    
    // Wait for service to be healthy
    await this.waitForHealthy(30000);
    console.log('[Service] Started successfully');
  }
  
  async stop() {
    if (this.serviceProcess) {
      this.serviceProcess.kill();
      this.serviceProcess = null;
    }
  }
  
  async isHealthy() {
    try {
      const response = await axios.get(`${this.serviceUrl}/health`, {
        timeout: 1000
      });
      return response.data.status === 'healthy';
    } catch {
      return false;
    }
  }
  
  async waitForHealthy(timeout = 30000) {
    const start = Date.now();
    while (Date.now() - start < timeout) {
      if (await this.isHealthy()) return true;
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    throw new Error('Service failed to start');
  }
}

// Use in Electron lifecycle
const serviceManager = new ServiceManager();

app.on('ready', async () => {
  try {
    await serviceManager.start();
    createWindow();
  } catch (error) {
    console.error('[Service] Failed to start:', error);
    app.quit();
  }
});

app.on('will-quit', async () => {
  await serviceManager.stop();
});
```

---

## Benefits vs Current Architecture

| Feature | v1.x (Current) | v2.0 (Proposed) |
|---------|----------------|-----------------|
| **Startup Time** | 500ms per command | 10ms API call |
| **State Management** | None (reload each time) | Persistent in-memory |
| **Error Handling** | Generic text parsing | Structured error codes |
| **Real-Time Updates** | ❌ No | ✅ WebSocket streaming |
| **Validation** | After submission | Before submission |
| **Caching** | ❌ No | ✅ Smart caching |
| **Testing** | Slow, brittle | Fast, reliable |
| **Security** | Env vars | Secure token manager |
| **Reliability** | Fails often | Self-healing |

---

## Migration Strategy (Zero Downtime)

### Week 1: Build Service (No Changes to GUI)
- FastAPI service running alongside
- GUI still uses CLI spawning
- Users see no changes

### Week 2: Feature Flags (A/B Testing)
```javascript
const USE_API_SERVICE = process.env.TAMINATOR_USE_API === 'true';

async function checkCustomer(customerId) {
  if (USE_API_SERVICE) {
    return checkCustomerAPI(customerId);  // New way
  } else {
    return checkCustomerCLI(customerId);  // Old way
  }
}
```

### Week 3: Gradual Rollout
- Dashboard → API ✅
- Check → API ✅
- Update → CLI (still works)
- Post → CLI (still works)

### Week 4: Complete Migration
- All operations use API
- CLI kept for backward compatibility
- Service auto-starts with GUI

---

## Testing Strategy

### Unit Tests (Fast)
```python
# Test service layer independently
def test_customer_service_list_customers():
    mock_config = MockConfigManager()
    service = CustomerService(mock_config)
    
    customers = await service.list_customers()
    assert len(customers) == 3
```

### Integration Tests
```python
# Test API endpoints
async def test_customer_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/customers/")
        assert response.status_code == 200
```

### E2E Tests (GUI)
```javascript
// Test GUI with mock service
describe('Dashboard', () => {
  beforeEach(() => {
    mockService.reset();
    mockService.setCustomers([/* test data */]);
  });
  
  it('loads customer data', async () => {
    await dashboard.load();
    expect(dashboard.customerCount).toBe(3);
  });
});
```

---

## Success Criteria

### Week 1 (Service Foundation)
- [ ] FastAPI service runs and responds to health checks
- [ ] Service layer classes implemented
- [ ] Core infrastructure (tokens, config, cache)
- [ ] Basic endpoints working

### Week 2 (API Complete)
- [ ] All customer endpoints
- [ ] All JIRA endpoints
- [ ] All portal endpoints
- [ ] WebSocket streaming
- [ ] Error handling complete

### Week 3 (GUI Integration)
- [ ] TypeScript API client
- [ ] Service manager (auto-start/stop)
- [ ] One feature migrated to API
- [ ] Error boundaries in GUI

### Week 4 (Production Ready)
- [ ] All features use API
- [ ] Tests passing (unit + integration)
- [ ] Documentation complete
- [ ] Performance benchmarks met
- [ ] Zero known bugs

---

## Rollback Plan

If v2.0 has issues:
1. Feature flag: `TAMINATOR_USE_API=false`
2. GUI falls back to CLI spawning
3. Service auto-shutdown
4. Users back to v1.x behavior

**No data loss, seamless rollback.**

---

## Next Steps

1. **Today:** Get approval for v2.0 architecture
2. **Tomorrow:** Start FastAPI service skeleton
3. **Week 1:** Complete service foundation
4. **Week 2-4:** Execute migration plan

**Ready to start building?**


