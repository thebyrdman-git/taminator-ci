# Google Functionality - Local Testing Guide

**Objective**: Test all Google Workspace integrations end-to-end on your local machine.

**What We're Testing**:
1. Google OAuth flow (browser → desktop → token storage)
2. Drive storage (upload/download files)
3. Gmail Clippy assistant (draft creation)
4. Token storage in system keyring
5. Token refresh (automatic)
6. Sign out (cleanup)

**Time Required**: 30-45 minutes

---

## 🔧 Prerequisites

### 1. Google OAuth Credentials
You need OAuth credentials from Google Cloud Console.

**Check if you have them**:
```bash
ls -la ~/.config/pai/secrets/google_oauth_credentials.json
```

**If missing, create them**:
1. Go to https://console.cloud.google.com/
2. Create project: "Taminator Local Testing"
3. Enable APIs:
   - Gmail API
   - Google Drive API
   - Google Calendar API (optional)
4. Create OAuth 2.0 credentials:
   - Application type: Desktop app
   - Name: "Taminator Desktop"
5. Download JSON → save as `~/.config/pai/secrets/google_oauth_credentials.json`

**Important**: The redirect URI must be `http://localhost:8080/` for local testing.

---

### 2. Python Dependencies
```bash
cd /home/jbyrd/TAMINATOR

# Check if dependencies installed
python3 -c "import google.auth; print('✅ google-auth installed')"
python3 -c "import googleapiclient; print('✅ google-api-python-client installed')"
python3 -c "import keyring; print('✅ keyring installed')"

# If any missing:
pip3 install --user -r requirements-service.txt
```

---

### 3. Start the Service
```bash
cd /home/jbyrd/TAMINATOR

# Start FastAPI service (required for OAuth callback)
python3 src/taminator/api/main.py

# Service should start on http://localhost:8765
# Look for: "🚀 Starting Taminator API Service v2.0"
```

**Keep this terminal open** - service must run during OAuth flow.

---

## 🧪 Test 1: Google OAuth Flow

### Step 1: Trigger OAuth Flow
Open a new terminal:
```bash
cd /home/jbyrd/TAMINATOR

# Test OAuth flow
python3 -c "
import sys
sys.path.insert(0, 'src')
from taminator.core.google_auth import get_google_auth_manager
from taminator.core.token_manager import get_token_manager

tm = get_token_manager()
gauth = get_google_auth_manager(tm)

print('🔐 Starting Google OAuth flow...')
print('Your browser should open automatically.')
print('Sign in with your @redhat.com account.')
print('')

# Start flow
success = gauth.authenticate()

if success:
    print('✅ SUCCESS: Google authentication complete!')
    print(f'Token stored securely in keyring')
    
    # Get user info
    info = gauth.get_user_info()
    print(f'Authenticated as: {info.get(\"email\")}')
else:
    print('❌ FAIL: Authentication failed')
    sys.exit(1)
"
```

### Expected Behavior:
1. ✅ Browser opens automatically to Google sign-in
2. ✅ You see "Choose a Google account" page
3. ✅ After selecting @redhat.com account:
   - Consent screen (first time only)
   - Shows scopes: Gmail, Drive, Calendar
4. ✅ Browser shows success message
5. ✅ Terminal shows "✅ SUCCESS"
6. ✅ Displays your email address

### Troubleshooting:
- ❌ **Browser doesn't open**: Check `xdg-open` works: `xdg-open https://google.com`
- ❌ **Port 8080 conflict**: Change port in `google_auth.py` → `REDIRECT_PORT = 8081`
- ❌ **Credentials error**: Verify JSON file exists and is valid
- ❌ **Redirect URI mismatch**: Add `http://localhost:8080/` to Google Cloud Console

---

## 🧪 Test 2: Token Storage & Retrieval

### Verify Token in Keyring:
```bash
cd /home/jbyrd/TAMINATOR

python3 -c "
import sys
sys.path.insert(0, 'src')
from taminator.core.token_manager import get_token_manager, TokenType

tm = get_token_manager()

# Check if token exists
has_token = tm.has_token(TokenType.GOOGLE_OAUTH)

if has_token:
    print('✅ Token stored in keyring')
    
    # Try to retrieve (will be JSON string)
    token_data = tm.get_token(TokenType.GOOGLE_OAUTH)
    print(f'✅ Token retrieved: {len(token_data)} bytes')
    
    # Verify it's valid JSON
    import json
    try:
        creds = json.loads(token_data)
        print(f'✅ Token has access_token: {\"access_token\" in creds}')
        print(f'✅ Token has refresh_token: {\"refresh_token\" in creds}')
    except:
        print('❌ Token is not valid JSON')
else:
    print('❌ No token found in keyring')
    print('Run Test 1 first')
"
```

### Expected Output:
```
✅ Token stored in keyring
✅ Token retrieved: 1234 bytes
✅ Token has access_token: True
✅ Token has refresh_token: True
```

---

## 🧪 Test 3: Gmail API Access

### Test Gmail Connection:
```bash
cd /home/jbyrd/TAMINATOR

python3 -c "
import sys
sys.path.insert(0, 'src')
from taminator.core.gmail_assistant import get_gmail_assistant

assistant = get_gmail_assistant()

print('📧 Testing Gmail API access...')

try:
    # List drafts (doesn't create anything)
    drafts = assistant.list_drafts(max_results=5)
    
    print(f'✅ SUCCESS: Gmail API working')
    print(f'You have {len(drafts)} draft(s) in Gmail')
    
    for draft in drafts[:3]:
        print(f'  - Draft ID: {draft[\"id\"]}')
        print(f'    Preview: {draft[\"snippet\"][:50]}...')
    
except Exception as e:
    print(f'❌ FAIL: Gmail API error: {e}')
    sys.exit(1)
"
```

### Expected Output:
```
📧 Testing Gmail API access...
✅ SUCCESS: Gmail API working
You have 2 draft(s) in Gmail
  - Draft ID: r1234567890
    Preview: Hi team, just wanted to follow up on...
```

---

## 🧪 Test 4: Clippy Email Draft Generation

### Test AI-Powered Draft Creation:
```bash
cd /home/jbyrd/TAMINATOR

python3 tests/test_clippy_local.py
```

**Create the test file** (`tests/test_clippy_local.py`):
```python
#!/usr/bin/env python3
"""
Test Clippy Gmail Assistant Locally

Tests:
1. Context detection
2. Draft generation (with/without AI)
3. Gmail draft creation
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from taminator.core.gmail_assistant import get_gmail_assistant


async def test_clippy():
    """Test Clippy end-to-end"""
    
    print("=" * 60)
    print("CLIPPY GMAIL ASSISTANT - LOCAL TEST")
    print("=" * 60)
    print()
    
    # Test content (realistic TAM scenario)
    clipboard_content = """
    Customer: TD Bank
    Issue: RHEL-12345 - Request for Performance Monitoring Feature
    
    Customer is requesting a new performance monitoring feature for RHEL 9.
    They need real-time CPU and memory metrics exposed via REST API.
    
    This would help them integrate with their internal monitoring systems.
    Priority: High
    Expected timeline: Q2 2025
    """
    
    assistant = get_gmail_assistant()
    
    # Test 1: Context Detection
    print("📋 Test 1: Context Detection")
    print("-" * 60)
    context = await assistant._detect_context(clipboard_content)
    
    print(f"Email Type: {context['type']}")
    print(f"Customer: {context.get('customer', 'N/A')}")
    print(f"Issue Keys: {context.get('issue_keys', [])}")
    print(f"Urgency: {context['urgency']}")
    print()
    
    # Test 2: Draft Generation
    print("🤖 Test 2: Draft Generation")
    print("-" * 60)
    
    draft = await assistant._generate_draft(clipboard_content, context)
    
    print(f"Subject: {draft['subject']}")
    print()
    print("Body Preview:")
    print(draft['body'][:400])
    print()
    
    # Test 3: Save to Gmail (optional)
    print("💾 Test 3: Save Draft to Gmail?")
    response = input("Save this draft to Gmail? (y/n): ")
    
    if response.lower() == 'y':
        try:
            draft_id = await assistant._save_to_gmail(draft)
            print(f"✅ Draft saved! ID: {draft_id}")
            print(f"View: https://mail.google.com/mail/u/0/#drafts/{draft_id}")
            print()
            print("📧 Check Gmail to verify draft")
        except Exception as e:
            print(f"❌ Failed to save draft: {e}")
    else:
        print("Skipped Gmail save")
    
    print()
    print("=" * 60)
    print("✅ CLIPPY TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_clippy())
```

### Expected Output:
```
====================================================
CLIPPY GMAIL ASSISTANT - LOCAL TEST
====================================================

📋 Test 1: Context Detection
------------------------------------------------------------
Email Type: rfe_update
Customer: TD Bank
Issue Keys: ['RHEL-12345']
Urgency: high

🤖 Test 2: Draft Generation
------------------------------------------------------------
Subject: RFE Update: RHEL-12345 - Performance Monitoring Feature

Body Preview:
Hi,

I wanted to update you on RHEL-12345, the performance monitoring feature request for RHEL 9.

Your request for real-time CPU and memory metrics via REST API has been reviewed...

💾 Test 3: Save Draft to Gmail?
Save this draft to Gmail? (y/n): y
✅ Draft saved! ID: r9876543210
View: https://mail.google.com/mail/u/0/#drafts/r9876543210

📧 Check Gmail to verify draft

====================================================
✅ CLIPPY TEST COMPLETE
====================================================
```

---

## 🧪 Test 5: Google Drive Storage

### Test Drive API Access:
```bash
cd /home/jbyrd/TAMINATOR

python3 -c "
import sys
sys.path.insert(0, 'src')
from taminator.core.drive_storage import get_drive_storage

storage = get_drive_storage()

print('☁️  Testing Google Drive API access...')

try:
    # List files (just to test connection)
    files = storage.list_files(max_results=5)
    
    print(f'✅ SUCCESS: Drive API working')
    print(f'Found {len(files)} file(s) in Drive')
    
    for f in files[:3]:
        print(f'  - {f[\"name\"]} (ID: {f[\"id\"]})')
    
except Exception as e:
    print(f'❌ FAIL: Drive API error: {e}')
    import traceback
    traceback.print_exc()
"
```

---

## 🧪 Test 6: Sign Out & Cleanup

### Test Token Removal:
```bash
cd /home/jbyrd/TAMINATOR

python3 -c "
import sys
sys.path.insert(0, 'src')
from taminator.core.google_auth import get_google_auth_manager
from taminator.core.token_manager import get_token_manager, TokenType

tm = get_token_manager()
gauth = get_google_auth_manager(tm)

print('🚪 Testing sign out...')

# Check if signed in
if not tm.has_token(TokenType.GOOGLE_OAUTH):
    print('⚠️  Not signed in')
    sys.exit(0)

# Revoke and delete
success = gauth.revoke_credentials()

if success:
    print('✅ Token revoked from Google')
else:
    print('⚠️  Could not revoke (token may be expired)')

# Delete from keyring
tm.delete_token(TokenType.GOOGLE_OAUTH)

# Verify deleted
if not tm.has_token(TokenType.GOOGLE_OAUTH):
    print('✅ Token deleted from keyring')
    print('Sign out complete')
else:
    print('❌ Token still in keyring')
"
```

---

## 📊 Full Test Suite

### Run All Tests:
```bash
cd /home/jbyrd/TAMINATOR

# Create comprehensive test script
cat > tests/test_google_full.sh << 'EOF'
#!/bin/bash
set -e

echo "🔐 GOOGLE INTEGRATION - FULL TEST SUITE"
echo "========================================"
echo ""

# Check service running
if ! curl -s http://localhost:8765/health > /dev/null; then
    echo "❌ Service not running"
    echo "Start with: python3 src/taminator/api/main.py"
    exit 1
fi

echo "✅ Service running"
echo ""

# Test 1: OAuth Flow
echo "Test 1: OAuth Flow"
echo "------------------"
python3 -c "
import sys
sys.path.insert(0, 'src')
from taminator.core.google_auth import get_google_auth_manager
from taminator.core.token_manager import get_token_manager

tm = get_token_manager()
gauth = get_google_auth_manager(tm)

if not tm.has_token('google_oauth'):
    print('Starting OAuth flow...')
    gauth.authenticate()
else:
    print('✅ Already authenticated')
"
echo ""

# Test 2: Token Storage
echo "Test 2: Token Storage"
echo "---------------------"
python3 -c "
import sys
sys.path.insert(0, 'src')
from taminator.core.token_manager import get_token_manager, TokenType

tm = get_token_manager()
has_token = tm.has_token(TokenType.GOOGLE_OAUTH)
print(f'Token in keyring: {\"✅\" if has_token else \"❌\"}')
"
echo ""

# Test 3: Gmail API
echo "Test 3: Gmail API"
echo "-----------------"
python3 -c "
import sys
sys.path.insert(0, 'src')
from taminator.core.gmail_assistant import get_gmail_assistant

assistant = get_gmail_assistant()
drafts = assistant.list_drafts(max_results=1)
print(f'Gmail API: ✅ ({len(drafts)} drafts)')
" 2>/dev/null || echo "Gmail API: ❌"
echo ""

# Test 4: Drive API
echo "Test 4: Drive API"
echo "-----------------"
python3 -c "
import sys
sys.path.insert(0, 'src')
from taminator.core.drive_storage import get_drive_storage

storage = get_drive_storage()
files = storage.list_files(max_results=1)
print(f'Drive API: ✅ ({len(files)} files)')
" 2>/dev/null || echo "Drive API: ❌"
echo ""

echo "========================================"
echo "✅ GOOGLE INTEGRATION TEST COMPLETE"
echo "========================================"
EOF

chmod +x tests/test_google_full.sh
./tests/test_google_full.sh
```

---

## 🐛 Troubleshooting

### Issue: Browser doesn't open
```bash
# Test browser opening
xdg-open https://google.com

# If fails, set browser explicitly
export BROWSER=firefox
# or
export BROWSER=google-chrome
```

### Issue: "Redirect URI mismatch"
**Fix**: Add `http://localhost:8080/` to Google Cloud Console:
1. Go to https://console.cloud.google.com/apis/credentials
2. Click your OAuth client ID
3. Add to "Authorized redirect URIs": `http://localhost:8080/`
4. Save

### Issue: "Invalid scope"
**Fix**: Enable APIs in Google Cloud Console:
1. Go to https://console.cloud.google.com/apis/library
2. Enable: Gmail API, Drive API, Calendar API
3. Wait 1-2 minutes for propagation

### Issue: Keyring errors on Linux
```bash
# Install keyring backend
sudo dnf install gnome-keyring  # Fedora/RHEL
# or
sudo apt install gnome-keyring  # Debian/Ubuntu

# Unlock keyring
gnome-keyring-daemon --unlock
```

### Issue: Token expired
```bash
# Tokens auto-refresh, but if that fails:
python3 -c "
import sys
sys.path.insert(0, 'src')
from taminator.core.google_auth import get_google_auth_manager
from taminator.core.token_manager import get_token_manager

tm = get_token_manager()
gauth = get_google_auth_manager(tm)

# Force re-authentication
gauth.revoke_credentials()
gauth.authenticate()
"
```

---

## ✅ Test Checklist

Before declaring Google integration "ready for alpha":

- [ ] OAuth flow works (browser opens, callback succeeds)
- [ ] Token stored in keyring (survives app restart)
- [ ] Gmail API works (can list drafts)
- [ ] Clippy can create drafts (saves to Gmail)
- [ ] Drive API works (can list files)
- [ ] Token refresh works (test with expired token)
- [ ] Sign out works (token removed from keyring)
- [ ] Error messages helpful (not stack traces)
- [ ] Works on fresh system (test in VM)
- [ ] GUI integration works (test from Electron app)

---

## 📝 Notes for Alpha Testing

**What to tell TAMs**:
1. "You need Google OAuth credentials (I'll help you set up)"
2. "Sign in with your @redhat.com account"
3. "Browser will open for authentication"
4. "Token stored securely in your keyring"
5. "Clippy needs Gmail access to create drafts"

**Known Limitations** (document for alpha):
- OAuth flow requires browser (no headless mode yet)
- Redirect URI must be `localhost:8080` (not configurable in v2.0)
- Token storage uses system keyring (requires gnome-keyring on Linux)
- Clippy requires LiteLLM proxy for AI features (graceful fallback if unavailable)

---

*Google Integration - Local Testing Guide*  
*Test everything before alpha. Earn user trust through reliability.*

