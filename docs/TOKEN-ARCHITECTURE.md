# Unified Token Architecture - All Credentials in OS Keyring

**Tesla Architecture - Secure Credential Management**

---

## 🎯 Design Decision

**All tokens stored in OS keyring via unified TokenManager.**

### Why Unified Storage?

1. **Single Source of Truth** - All credentials in one secure location
2. **Consistent Security** - OS-level encryption for all tokens
3. **Better UX** - Single authentication status interface
4. **Easier Management** - One API for all credential operations
5. **Audit Trail** - Centralized logging of all token operations

---

## 🔐 Token Types

```python
class TokenType(str, Enum):
    JIRA = "jira"              # JIRA API token
    PORTAL = "portal"          # Customer Portal API token
    GOOGLE_OAUTH = "google_oauth"  # Google OAuth2 credentials (JSON)
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                           │
│  - GUI Settings                                                 │
│  - OOBE Wizard                                                  │
│  - API Routes                                                   │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     TOKEN MANAGER                               │
│  Unified interface for all credentials                          │
│                                                                 │
│  Methods:                                                       │
│  - get_token(TokenType) → str                                   │
│  - set_token(TokenType, str, expires_in_days)                   │
│  - delete_token(TokenType)                                      │
│  - has_token(TokenType) → bool                                  │
│  - get_status() → Dict[TokenType, bool]                         │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     OS KEYRING                                  │
│  Platform-specific secure storage                               │
│                                                                 │
│  Linux:   Secret Service API / gnome-keyring                    │
│  macOS:   Keychain                                              │
│  Windows: Credential Manager                                    │
│                                                                 │
│  Service: "taminator"                                           │
│  Keys:    "jira", "portal", "google_oauth"                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Token Storage Format

### JIRA Token
```
Type: Simple string
Format: Bearer token from JIRA
Storage: OS keyring["taminator"]["jira"]
Example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Portal Token
```
Type: Simple string
Format: API token from Red Hat Customer Portal
Storage: OS keyring["taminator"]["portal"]
Example: "portal_token_abc123..."
```

### Google OAuth
```
Type: JSON string (OAuth2 Credentials)
Format: {
  "token": "ya29.a0...",
  "refresh_token": "1//0e...",
  "token_uri": "https://oauth2.googleapis.com/token",
  "client_id": "...apps.googleusercontent.com",
  "client_secret": "...",
  "scopes": [...]
}
Storage: OS keyring["taminator"]["google_oauth"]
```

---

## 🔄 Token Flow Examples

### JIRA Token Setup
```python
# User enters JIRA token in settings
token_manager.set_token(TokenType.JIRA, "user_token_here")

# Later: JIRA service retrieves token
jira_service = JiraService(token_manager)
token = token_manager.get_token(TokenType.JIRA)  # From OS keyring
```

### Google OAuth Flow
```python
# 1. User starts OAuth flow
auth_manager = GoogleAuthManager(token_manager)
auth_url = auth_manager.start_oauth_flow()

# 2. User authorizes in browser

# 3. Complete flow with authorization code
user_info = auth_manager.complete_oauth_flow(callback_url)

# 4. Token automatically saved to OS keyring
# token_manager.set_token(TokenType.GOOGLE_OAUTH, credentials_json)

# 5. Later: Retrieve and refresh
auth_manager = GoogleAuthManager(token_manager)
if auth_manager.has_valid_token():  # Auto-loads from keyring
    gmail = auth_manager.get_gmail_service()
```

---

## 🎨 Unified Status API

### Single Endpoint for All Auth Status
```bash
GET /health

Response:
{
  "status": "healthy",
  "authentication": {
    "jira": true,          # ✅ JIRA token present
    "portal": false,       # ❌ Portal token missing
    "google_oauth": true   # ✅ Google authenticated
  },
  ...
}
```

### Individual Service Status
```bash
# JIRA status (uses TokenManager)
GET /api/jira/status

# Portal status (uses TokenManager)
GET /api/portal/status

# Google status (uses TokenManager via GoogleAuthManager)
GET /api/google/status
```

---

## 🔒 Security Benefits

### OS Keyring Encryption
- **Linux**: Encrypted with user login keyring
- **macOS**: Protected by Keychain Access
- **Windows**: Windows Data Protection API (DPAPI)

### No Plain Text Storage
- ❌ No tokens in JSON files
- ❌ No tokens in environment variables
- ❌ No tokens in logs
- ❌ No tokens in process arguments
- ✅ All tokens in OS-encrypted storage

### Automatic Token Refresh
```python
# Google OAuth: Auto-refresh when expired
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
    token_manager.set_token(TokenType.GOOGLE_OAUTH, creds.to_json())
```

### Audit Logging
```
[2025-10-28 02:30:15] INFO  token_manager - ✅ Stored jira token securely
[2025-10-28 02:31:20] INFO  token_manager - ✅ Stored google_oauth token securely
[2025-10-28 02:32:45] INFO  token_manager - 🗑️  Deleted portal token
```

---

## 🧪 Testing Token Storage

### Check Token Presence
```bash
# Via API
curl http://127.0.0.1:8765/health | jq '.authentication'

# Via Python
from taminator.core.token_manager import get_token_manager, TokenType

tm = get_token_manager()
print(tm.has_token(TokenType.JIRA))        # True/False
print(tm.has_token(TokenType.PORTAL))      # True/False
print(tm.has_token(TokenType.GOOGLE_OAUTH)) # True/False
```

### Verify Keyring Storage (Linux)
```bash
# Using secret-tool (gnome-keyring)
secret-tool search service taminator

# Should show:
# [/org/freedesktop/secrets/collection/login/1]
# label = taminator:jira
# secret = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Verify Keyring Storage (macOS)
```bash
# Using security command
security find-generic-password -s taminator -a jira

# Should show keyring entry
```

---

## 📋 Migration Path

### Migrating from Old Storage

If you had old token storage (e.g., JSON files), migrate to keyring:

```python
from pathlib import Path
import json
from taminator.core.token_manager import get_token_manager, TokenType

tm = get_token_manager()

# Migrate old Google token file
old_token_file = Path.home() / ".config/taminator/google_token.json"
if old_token_file.exists():
    with open(old_token_file) as f:
        token_data = f.read()
    
    # Store in keyring
    tm.set_token(TokenType.GOOGLE_OAUTH, token_data)
    
    # Delete old file
    old_token_file.unlink()
    print("✅ Migrated Google token to keyring")
```

---

## 🎯 Benefits Summary

### For Users
- ✅ Single sign-in experience
- ✅ Unified authentication status
- ✅ Secure token storage (OS-level encryption)
- ✅ No manual token file management

### For Developers
- ✅ Single API for all tokens
- ✅ Consistent error handling
- ✅ Centralized logging
- ✅ Easier testing

### For Security
- ✅ OS-level encryption
- ✅ No plain text credentials
- ✅ Automatic token expiry
- ✅ Audit trail

---

## 🔮 Future Enhancements

### Token Rotation
- Auto-rotate JIRA/Portal tokens every 90 days
- Warn user when tokens nearing expiry

### Multi-Account Support
- Store multiple Google accounts
- Switch between accounts
- Team-shared tokens (with encryption)

### Token Export/Import
- Backup tokens securely
- Import tokens from another machine
- Team token sharing (encrypted)

---

*Unified Token Architecture for Taminator v2.0 Tesla*  
*All credentials secured in OS keyring, single API interface*

