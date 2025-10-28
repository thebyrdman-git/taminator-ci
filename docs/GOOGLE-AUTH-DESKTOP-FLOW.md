# Google OAuth Flow - Desktop Application

**How Taminator handles Google authentication in an Electron desktop app**

---

## 🎯 User Experience

**What the user sees:**

1. User clicks "Sign In with Google" in Taminator desktop app
2. Browser tab opens with Google login page
3. User authenticates with @redhat.com account in browser
4. Browser shows "Authentication complete! Return to Taminator"
5. User returns to Taminator desktop app
6. Desktop app shows "✅ Signed in as jbyrd@redhat.com"

**Everything stays in the desktop app except the authentication step.**

---

## 🔄 Technical Flow

### Step-by-Step Process

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User clicks "Sign In with Google" in Electron app       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Electron calls API: POST /api/google/auth/start         │
│    Response: { auth_url: "https://accounts.google.com..." }│
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Electron opens browser: shell.openExternal(auth_url)    │
│    Browser window opens with Google login page             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. User authenticates in browser (Google's page)           │
│    - Enter @redhat.com credentials                          │
│    - Accept permissions                                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Browser redirects to: http://localhost:8080/callback    │
│    API receives callback with authorization code            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. API exchanges code for tokens, stores in OS keyring     │
│    Browser shows: "✅ Authentication complete!"             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Electron polls API: GET /api/google/status (every 2s)   │
│    When authenticated: Show success in desktop app          │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Code Implementation

### 1. Electron GUI (Desktop App)

**File**: `gui/google-auth-handler.js`

```javascript
// User clicks "Sign In with Google"
async function signIn() {
    // Step 1: Get OAuth URL from API
    const response = await api.request('/api/google/auth/start', {
        method: 'POST',
        body: JSON.stringify({ port: 8080 })
    });
    
    // Step 2: Open browser with OAuth URL
    const { shell } = require('electron');
    shell.openExternal(response.auth_url);
    
    // Step 3: Show "waiting for authentication" in desktop app
    showWaitingModal();
    
    // Step 4: Poll API until authentication completes
    await pollForCompletion();
    
    // Step 5: Show success in desktop app
    showSuccess();
}
```

### 2. FastAPI Backend

**File**: `src/taminator/api/routes/google_auth.py`

```python
@router.post("/auth/start")
async def start_auth_flow(port: int = 8080):
    """
    Start OAuth flow
    
    Returns:
        auth_url: URL for user to open in browser
    """
    auth_manager = get_google_auth_manager()
    
    # Generate OAuth URL
    auth_url = auth_manager.start_oauth_flow(port)
    
    return {
        "auth_url": auth_url,
        "message": "Open this URL in your browser to authenticate"
    }

# Browser callback (automatic)
@router.get("/auth/callback")
async def oauth_callback(code: str, state: str):
    """
    OAuth callback endpoint
    
    This is called by browser after user authenticates
    """
    auth_manager = get_google_auth_manager()
    
    # Exchange code for tokens
    auth_manager.complete_oauth_flow(code, state)
    
    # Store tokens in OS keyring
    auth_manager.save_tokens()
    
    return {
        "message": "✅ Authentication complete! You can close this window."
    }

@router.get("/status")
async def get_status():
    """Check if user is authenticated"""
    auth_manager = get_google_auth_manager()
    
    if auth_manager.has_valid_token():
        user_info = auth_manager.get_user_info()
        return {
            "authenticated": True,
            "user_email": user_info['email'],
            "user_name": user_info['name']
        }
    else:
        return {"authenticated": False}
```

### 3. Google OAuth Manager

**File**: `src/taminator/core/google_auth.py`

```python
def start_oauth_flow(self, port: int = 8080) -> str:
    """
    Start OAuth flow
    
    Returns:
        Authorization URL for user to open
    """
    flow = Flow.from_client_secrets_file(
        self.credentials_path,
        scopes=self.SCOPES,
        redirect_uri=f'http://localhost:{port}/api/google/auth/callback'
    )
    
    # Generate authorization URL
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    # Store flow for later
    self._current_flow = flow
    
    return auth_url
```

---

## 🖼️ GUI Flow

### Desktop App Screens

**Before Authentication:**
```
╔═══════════════════════════════════════════════════════════╗
║  🔐 Google Account                                        ║
╠═══════════════════════════════════════════════════════════╣
║  🔒 Not Connected                                         ║
║  Sign in to unlock Google Workspace features             ║
║                                                           ║
║  Why Sign In?                                            ║
║                                                           ║
║  ☁️ Google Drive          📧 Gmail Drafts                ║
║  Unlimited storage        AI-powered emails              ║
║                                                           ║
║  [🔐 Sign In with Google]                                ║
║                                                           ║
║  ⓘ Only @redhat.com accounts allowed                     ║
║    Authentication opens in your browser                   ║
╚═══════════════════════════════════════════════════════════╝
```

**During Authentication (Modal):**
```
╔═══════════════════════════════════════════════════════════╗
║  🔐 Authenticating with Google                           ║
║                                                           ║
║         [Spinning animation]                             ║
║                                                           ║
║  Please complete authentication in your browser.         ║
║                                                           ║
║  A browser tab has opened for you to sign in with your   ║
║  @redhat.com account.                                    ║
║                                                           ║
║  [Cancel]                                                ║
╚═══════════════════════════════════════════════════════════╝
```

**After Authentication:**
```
╔═══════════════════════════════════════════════════════════╗
║  🔐 Google Account                                        ║
╠═══════════════════════════════════════════════════════════╣
║  ✅ Connected to Google                                   ║
║  Signed in as jbyrd@redhat.com                           ║
║                                                           ║
║  Account Information:                                    ║
║  Name:    Jimmy Byrd                                     ║
║  Email:   jbyrd@redhat.com                               ║
║  Storage: OS Keyring                                     ║
║                                                           ║
║  Connected Services:                                     ║
║  ☁️ Google Drive   ✅ [Configure]                        ║
║  📧 Gmail          ✅ [Open Clippy]                       ║
║  📅 Calendar       ✅ [Coming Soon]                       ║
║                                                           ║
║  [🚪 Sign Out]                                            ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 🔐 Security Features

### Why Browser for OAuth?

**Security reasons:**
1. ✅ **No password in app** - Taminator never sees your password
2. ✅ **Google's security** - 2FA, device verification, etc.
3. ✅ **Token exchange** - App only gets authorization code
4. ✅ **Standard practice** - All desktop apps use this flow (VS Code, Slack, etc.)

### Token Storage

**Where tokens are stored:**
- **Linux**: Secret Service API (GNOME Keyring, KWallet)
- **macOS**: Keychain
- **Windows**: Credential Locker

**Never stored in:**
- ❌ Config files
- ❌ Environment variables
- ❌ Log files
- ❌ Process memory (after authentication)

### Domain Restriction

**Only @redhat.com accounts allowed:**
```python
def complete_oauth_flow(self, code: str, state: str):
    # Get user info
    user_info = get_user_from_token()
    email = user_info['email']
    
    # Enforce domain restriction
    if not email.endswith('@redhat.com'):
        raise ValueError(
            f"Only @redhat.com accounts allowed. Got: {email}"
        )
    
    # Continue with token storage
    self.save_tokens()
```

---

## 🧪 Testing the Flow

### Manual Test

1. **Start service:**
   ```bash
   cd /home/jbyrd/TAMINATOR
   ./bin/taminator-service
   ```

2. **Open desktop app:**
   ```bash
   cd gui
   npm start
   ```

3. **Navigate to Google Settings:**
   - Click Settings → Google Account

4. **Click "Sign In with Google":**
   - Browser opens with Google login
   - Sign in with @redhat.com account
   - Accept permissions
   - Browser shows "Authentication complete"

5. **Return to desktop app:**
   - Desktop app shows "✅ Signed in as jbyrd@redhat.com"
   - All Google features now unlocked

### API Test

```bash
# 1. Start auth flow
curl -X POST http://localhost:8765/api/google/auth/start \
  -H "Content-Type: application/json" \
  -d '{"port": 8080}'

# Response:
# {
#   "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?..."
# }

# 2. Open auth_url in browser and authenticate

# 3. Check status (should show authenticated)
curl http://localhost:8765/api/google/status

# Response:
# {
#   "authenticated": true,
#   "user_email": "jbyrd@redhat.com",
#   "user_name": "Jimmy Byrd"
# }
```

---

## 🎯 Key Points

### What Stays in Desktop App
✅ **Main interface** - All customer data, dashboards, reports  
✅ **Drive storage UI** - Upload/download controls  
✅ **Clippy assistant** - Email draft generation  
✅ **Settings** - All configuration  
✅ **User info display** - Show authenticated user  

### What Opens in Browser
⚠️ **Only Google authentication** - Login page only  
⚠️ **Callback page** - Shows "Authentication complete"  
⚠️ **Nothing else** - All other features in desktop app  

### User Experience
- ✅ **Seamless** - Browser opens automatically
- ✅ **Secure** - Standard OAuth flow
- ✅ **Fast** - Polling detects completion in 2 seconds
- ✅ **Clear** - Desktop app shows status throughout

---

## 📝 Implementation Checklist

✅ **Electron integration**
- `google-auth-handler.js` for OAuth flow
- `shell.openExternal()` to open browser
- Polling for completion

✅ **GUI components**
- Settings page for Google Account
- Modal for "waiting for auth"
- Success/error messages

✅ **API endpoints**
- `/api/google/auth/start` - Get OAuth URL
- `/api/google/auth/callback` - Receive code
- `/api/google/status` - Check authentication

✅ **Security**
- Token storage in OS keyring
- Domain restriction (@redhat.com)
- No passwords in app

---

**The desktop app is always the main interface. Only authentication uses the browser for security.**

*This is the same pattern used by VS Code, Slack, Discord, and all modern desktop apps.*

---

*Google OAuth Desktop Flow - Taminator v2.0*  
*Secure authentication without leaving the desktop experience*

