# Google Account Integration - Setup Guide

**Tesla Architecture - Google OAuth2 Integration**

---

## 🎯 Overview

Taminator v2.0 includes Google Account integration for TAMs, providing:

- ✅ **Google Sign-In** - OAuth2 authentication with @redhat.com restriction
- ✅ **Gmail Integration** - Read unread emails, search messages
- ✅ **Calendar Integration** - View upcoming meetings
- ✅ **Drive Integration** - Access shared customer documents
- ✅ **Secure Token Storage** - OS-level credential management
- ✅ **Auto Token Refresh** - Seamless re-authentication

---

## 🔧 Setup Instructions

### Step 1: Create Google Cloud Project

1. **Go to Google Cloud Console**  
   https://console.cloud.google.com/

2. **Create New Project**
   - Click "Select a project" → "New Project"
   - Name: `Taminator TAM Tools`
   - Organization: `redhat.com`
   - Click "Create"

3. **Enable Required APIs**
   - Navigate to "APIs & Services" → "Library"
   - Enable these APIs:
     - Google+ API (for user info)
     - Gmail API
     - Google Calendar API
     - Google Drive API

### Step 2: Create OAuth 2.0 Credentials

1. **Navigate to Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"

2. **Configure OAuth Consent Screen** (if first time)
   - User Type: **Internal** (Red Hat users only)
   - App name: `Taminator TAM Tools`
   - User support email: `your-email@redhat.com`
   - Developer contact: `your-email@redhat.com`
   - Scopes: Add the following
     - `.../auth/userinfo.email`
     - `.../auth/userinfo.profile`
     - `.../auth/gmail.readonly`
     - `.../auth/calendar.readonly`
     - `.../auth/drive.readonly`

3. **Create OAuth Client ID**
   - Application type: **Desktop app**
   - Name: `Taminator Desktop`
   - Click "Create"

4. **Download Credentials**
   - Click the download button (⬇️) next to your OAuth client
   - Save as: `google_oauth_credentials.json`

### Step 3: Install Credentials in Taminator

```bash
# Create config directory
mkdir -p ~/.config/taminator

# Copy credentials file
cp ~/Downloads/google_oauth_credentials.json ~/.config/taminator/

# Verify
ls -l ~/.config/taminator/google_oauth_credentials.json
```

### Step 4: First-Time Authentication

1. **Start Taminator**
   ```bash
   ./Taminator-2.0.0.AppImage
   ```

2. **Click "Sign in with Google"** (in settings or OOBE)

3. **Browser Opens** with Google Sign-In
   - Choose your @redhat.com account
   - Grant requested permissions:
     - View email address
     - View basic profile info
     - Read Gmail messages
     - View Calendar events
     - View Drive files

4. **Return to Taminator**
   - Authentication complete
   - Token stored securely

---

## 🔐 Security Features

### Domain Restriction
- Only `@redhat.com` accounts allowed
- Enforced at OAuth consent screen
- Verified server-side

### Token Storage
- Stored in OS keyring (not plain text)
- Linux: Secret Service API / gnome-keyring
- macOS: Keychain
- Windows: Credential Manager

### Token Refresh
- Automatic refresh when expired
- No need to re-authenticate
- Seamless background renewal

### Permissions (Read-Only)
- Gmail: Read only (cannot send/delete)
- Calendar: Read only (cannot create events)
- Drive: Read only (cannot modify files)
- User info: Email and name only

---

## 📋 API Endpoints

### Authentication

```bash
# Get auth status
curl http://127.0.0.1:8765/api/google/status

# Start OAuth flow
curl -X POST http://127.0.0.1:8765/api/google/auth/start?port=8080

# Complete OAuth flow
curl -X POST http://127.0.0.1:8765/api/google/auth/complete \
  -H "Content-Type: application/json" \
  -d '{"authorization_response": "http://localhost:8080/?code=..."}'

# Get user info
curl http://127.0.0.1:8765/api/google/user

# Sign out
curl -X POST http://127.0.0.1:8765/api/google/auth/revoke
```

### Gmail Integration

```bash
# Get unread emails
curl http://127.0.0.1:8765/api/google/gmail/unread?max_results=10
```

---

## 🎨 GUI Integration

### Sign-In Button (Settings Page)

```javascript
// Check auth status
const status = await apiClient.get('/api/google/status');

if (!status.authenticated) {
  // Show "Sign in with Google" button
  showGoogleSignInButton();
} else {
  // Show user info
  showUserInfo(status.user_email, status.user_name);
}
```

### OAuth Flow (Popup Window)

```javascript
// Start OAuth flow
const response = await apiClient.post('/api/google/auth/start', { port: 8080 });

// Open browser to auth_url
window.open(response.auth_url);

// Listen for callback on localhost:8080
// Complete flow when code received
await apiClient.post('/api/google/auth/complete', {
  authorization_response: callbackUrl,
  port: 8080
});
```

---

## 🔄 Usage Examples

### Get Unread Emails

```python
# Backend
from taminator.core.google_auth import get_google_auth_manager

auth_manager = get_google_auth_manager()

if auth_manager.has_valid_token():
    gmail = auth_manager.get_gmail_service()
    
    # Get unread messages
    results = gmail.users().messages().list(
        userId='me',
        q='is:unread',
        maxResults=10
    ).execute()
    
    messages = results.get('messages', [])
```

### Check Calendar Events

```python
# Backend
calendar = auth_manager.get_calendar_service()

# Get today's events
now = datetime.utcnow().isoformat() + 'Z'
events_result = calendar.events().list(
    calendarId='primary',
    timeMin=now,
    maxResults=10,
    singleEvents=True,
    orderBy='startTime'
).execute()

events = events_result.get('items', [])
```

### Search Drive Files

```python
# Backend
drive = auth_manager.get_drive_service()

# Search for customer documents
results = drive.files().list(
    q="name contains 'customer' and mimeType='application/pdf'",
    pageSize=10,
    fields="files(id, name, mimeType, modifiedTime)"
).execute()

files = results.get('files', [])
```

---

## 🧪 Testing

### Test OAuth Flow

```bash
# Start service
./dist/taminator-service --port 8765 &

# Test status endpoint
curl http://127.0.0.1:8765/api/google/status

# Should return:
# {
#   "credentials_configured": false,  # Until you add credentials
#   "authenticated": false,
#   "user_email": null,
#   "user_name": null,
#   "token_path": "~/.config/taminator/google_token.json",
#   "credentials_path": "~/.config/taminator/google_oauth_credentials.json"
# }
```

### Test Gmail Integration

```bash
# After authentication
curl http://127.0.0.1:8765/api/google/gmail/unread?max_results=5
```

---

## 🐛 Troubleshooting

### "Google OAuth credentials not configured"

**Problem**: Credentials file not found

**Solution**:
1. Download credentials from Google Cloud Console
2. Save to: `~/.config/taminator/google_oauth_credentials.json`
3. Restart Taminator

### "Only @redhat.com accounts are allowed"

**Problem**: Non-Red Hat email used

**Solution**:
- Sign in with your @redhat.com Google account
- If you don't have one, contact IT

### "Token expired"

**Problem**: Refresh token invalid

**Solution**:
- Sign out: `curl -X POST http://127.0.0.1:8765/api/google/auth/revoke`
- Sign in again

### "Permission denied"

**Problem**: Required scopes not granted

**Solution**:
1. Go to: https://myaccount.google.com/permissions
2. Find "Taminator TAM Tools"
3. Click "Remove access"
4. Sign in again and grant all permissions

---

## 📚 References

- **Google OAuth2 Documentation**: https://developers.google.com/identity/protocols/oauth2
- **Gmail API**: https://developers.google.com/gmail/api
- **Calendar API**: https://developers.google.com/calendar/api
- **Drive API**: https://developers.google.com/drive/api

---

## 🎯 Future Enhancements

### Phase 1 (Current)
- ✅ Google Sign-In
- ✅ Gmail unread messages
- ✅ OAuth token management

### Phase 2 (Planned)
- [ ] Calendar event creation
- [ ] Gmail send email
- [ ] Drive file upload
- [ ] Google Contacts integration

### Phase 3 (Future)
- [ ] Google Meet integration
- [ ] Google Docs collaboration
- [ ] Shared drive access
- [ ] Admin SDK (for TAM leads)

---

*Google Account Integration for Taminator v2.0 Tesla Architecture*  
*Secure, @redhat.com restricted, read-only by default*

