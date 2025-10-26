# Vault Setup Testing Guide

Quick guide for testing the Vault Setup flow in Taminator OOBE wizard.

---

## 🚀 Quick Start Testing

### Prerequisites

1. **Vault Server** - You need access to a HashiCorp Vault server
   - URL (e.g., `https://vault.example.com:8200`)
   - Valid token (e.g., `hvs.XXXXXXXXXXXX`)
   - KV mount path (usually `secret`)
   - Secret path where tokens are stored

2. **Taminator Development Mode**
   ```bash
   cd /home/jbyrd/pai/taminator
   npm start -- --dev
   ```

3. **Trigger OOBE Wizard**
   - Delete OOBE state: `rm ~/.config/taminator-gui/oobe-state.json`
   - Restart Taminator
   - Wizard should appear automatically

---

## 📋 Test Scenarios

### ✅ Test 1: Successful Connection

**Steps:**
1. Launch Taminator (OOBE wizard appears)
2. Click "Let's Get Started"
3. Select "Team Setup (Recommended)"
4. Click "Next"
5. Fill in Vault details:
   - URL: `https://your-vault-server:8200`
   - Token: `hvs.YOUR_VALID_TOKEN`
   - Mount: `secret`
   - Path: `taminator/tokens` (or your actual path)
6. Click "Test Connection"

**Expected Result:**
- Spinner appears briefly
- Green success box: "✅ Connection successful! Vault is configured correctly."
- Next button becomes enabled

**Verify:**
```bash
cat ~/.config/taminator-gui/vault-config.json
# Should show your config with timestamp
```

---

### ❌ Test 2: Invalid URL

**Steps:**
1. Enter invalid URL: `not-a-url`
2. Try to submit form

**Expected Result:**
- Browser validation error: "Please enter a valid URL"
- Cannot proceed to test

---

### ❌ Test 3: Wrong Vault Server

**Steps:**
1. Enter URL: `https://wrong-server.example.com:8200`
2. Enter valid token
3. Click "Test Connection"

**Expected Result:**
- Red error box: "❌ Cannot connect to Vault: [error details]"
- Next button stays disabled

---

### ❌ Test 4: Invalid Token

**Steps:**
1. Enter valid Vault URL
2. Enter invalid token: `hvs.WRONG_TOKEN`
3. Click "Test Connection"

**Expected Result:**
- Red error box: "❌ Access denied - check your Vault token permissions"
- Next button stays disabled

---

### ❌ Test 5: Wrong Secret Path

**Steps:**
1. Enter valid Vault URL and token
2. Enter non-existent path: `does/not/exist`
3. Click "Test Connection"

**Expected Result:**
- Red error box: "❌ Secret path not found: does/not/exist"
- Next button stays disabled

---

### 🔄 Test 6: Form State Reset

**Steps:**
1. Fill form with valid details
2. Click "Test Connection" (success)
3. Change any input field (e.g., edit URL)
4. Observe behavior

**Expected Result:**
- Success message disappears
- Must test connection again before proceeding
- Next button becomes disabled

---

### 🔙 Test 7: Navigation

**Steps:**
1. Fill form and test successfully
2. Click "Back" button
3. Should return to "Choose Authentication Method"
4. Select "Team Setup" again
5. Should return to Vault setup
6. Form should be empty (fresh start)

---

## 🛠️ Troubleshooting

### Vault Connection Fails

**Check:**
1. Vault server is running: `curl -k https://your-vault:8200/v1/sys/health`
2. Token is valid: `vault token lookup` (if using Vault CLI)
3. Secret path exists: `vault kv get secret/taminator/tokens`
4. Network connectivity (firewall, VPN)

### Form Doesn't Validate

**Check:**
- Browser console for JavaScript errors (Ctrl+Shift+I)
- Main process logs in terminal
- Check electron version compatibility

### Configuration Not Saved

**Check:**
```bash
ls -la ~/.config/taminator-gui/
# Should show vault-config.json

cat ~/.config/taminator-gui/vault-config.json
# Should show your config
```

### OOBE Wizard Doesn't Appear

**Force reset:**
```bash
rm ~/.config/taminator-gui/oobe-state.json
# Restart Taminator
```

---

## 🔍 Debugging Tips

### Enable DevTools

Already enabled in dev mode:
```bash
npm start -- --dev
```

### View Console Logs

**Frontend (Renderer):**
- Open DevTools (Ctrl+Shift+I)
- Console tab shows UI logs

**Backend (Main Process):**
- Terminal where `npm start` is running
- Shows `[OOBE]` prefixed logs

### Check Network Requests

In DevTools:
1. Network tab
2. Trigger "Test Connection"
3. Look for Vault API calls
4. Check request/response details

---

## 📊 Test Results Template

```markdown
## Test Run: [Date]

### Environment
- Vault URL: [redacted]
- Taminator Version: [version]
- OS: Linux / Fedora 42
- Node Version: [node --version]

### Test Results

| Test | Status | Notes |
|------|--------|-------|
| Successful Connection | ✅ / ❌ | |
| Invalid URL | ✅ / ❌ | |
| Wrong Server | ✅ / ❌ | |
| Invalid Token | ✅ / ❌ | |
| Wrong Path | ✅ / ❌ | |
| Form Reset | ✅ / ❌ | |
| Navigation | ✅ / ❌ | |

### Issues Found
1. [Issue description]
2. [Issue description]

### Recommendations
- [Recommendation]
```

---

## 🚨 Security Testing

### Verify Token Security

**Check 1:** Token not visible in UI
- Open DevTools → Elements
- Inspect password field
- Should show `type="password"` and masked value

**Check 2:** Token not in console logs
- Check browser console
- Check terminal logs
- Token should never be logged

**Check 3:** Config file permissions
```bash
ls -la ~/.config/taminator-gui/vault-config.json
# Should be -rw-r--r-- or better: -rw-------
```

**TODO:** Implement file permission enforcement (chmod 600)

---

## 📝 Example Test Vault Setup

If you need a test Vault instance:

### Using Vault Dev Server

```bash
# Start Vault in dev mode (NOT FOR PRODUCTION)
vault server -dev

# In another terminal:
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'  # Dev mode root token

# Create test secret
vault kv put secret/taminator/tokens \
  jira_token="test-jira-token" \
  portal_token="test-portal-token"

# Verify
vault kv get secret/taminator/tokens
```

**Use in Taminator:**
- URL: `http://127.0.0.1:8200`
- Token: `root`
- Mount: `secret`
- Path: `taminator/tokens`

---

## ✅ Ready for Production?

Before deploying to TAM team:

- [ ] All test scenarios pass
- [ ] Security testing complete
- [ ] Token encryption implemented
- [ ] File permissions enforced
- [ ] Documentation updated
- [ ] Error messages clear and helpful
- [ ] User testing with real TAMs
- [ ] Vault admin documentation

---

**Last Updated:** October 24, 2025  
**Test Status:** Implementation Complete - Ready for Testing

