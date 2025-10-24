# Vault Setup Flow - Visual Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TAMINATOR OOBE WIZARD                                │
│                         Vault Setup Flow (Screen 3a)                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│  Screen 1:      │
│  Welcome        │
│                 │
│  • Intro        │
│  • Features     │
│                 │
└────────┬────────┘
         │ [Next]
         ▼
┌─────────────────┐
│  Screen 2:      │
│  Auth Choice    │
│                 │
│  ○ Team Setup   │◄──────┐
│  ○ Personal     │       │
│                 │       │
└────────┬────────┘       │
         │                │
         ├─────────[Back]─┘
         │
         │ [Next] → Team Setup Selected
         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Screen 3a: Vault Setup                                                      │
│                                                                              │
│  🏢 Connect to HashiCorp Vault                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                              │
│  📝 Form Fields:                                                            │
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │  Vault Server URL                                              │        │
│  │  ┌──────────────────────────────────────────────────────────┐ │        │
│  │  │ https://vault.example.com:8200                           │ │        │
│  │  └──────────────────────────────────────────────────────────┘ │        │
│  │  Example: https://vault.mycompany.com:8200                    │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │  Vault Token                                                   │        │
│  │  ┌──────────────────────────────────────────────────────────┐ │        │
│  │  │ ••••••••••••••••                                         │ │        │
│  │  └──────────────────────────────────────────────────────────┘ │        │
│  │  Your personal Vault access token                             │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │  KV Mount Path                                                 │        │
│  │  ┌──────────────────────────────────────────────────────────┐ │        │
│  │  │ secret                                                   │ │        │
│  │  └──────────────────────────────────────────────────────────┘ │        │
│  │  The KV secrets engine mount path (usually "secret")          │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │  Secret Path                                                   │        │
│  │  ┌──────────────────────────────────────────────────────────┐ │        │
│  │  │ taminator/tokens                                         │ │        │
│  │  └──────────────────────────────────────────────────────────┘ │        │
│  │  Path where your tokens are stored (e.g., taminator/tokens)   │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │                    🔍 Test Connection                          │        │
│  └────────────────────────────────────────────────────────────────┘        │
│         │                                                                    │
│         │ [Click]                                                           │
│         ▼                                                                    │
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │  Result Box (conditional):                                     │        │
│  │                                                                 │        │
│  │  Testing:  ⟳ Testing connection to Vault...                   │        │
│  │  Success:  ✅ Connection successful! Vault configured.         │        │
│  │  Error:    ❌ Connection failed: [error details]               │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                                                              │
│  [← Back]                                          [Next →] (if tested)     │
└──────┬───────────────────────────────────────────────────────┬─────────────┘
       │                                                        │
       │ Back                                                   │ Next (success)
       │                                                        │
       ▼                                                        ▼
  (Return to                                           TODO: Screen 4
   Auth Choice)                                        Token Verification


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BACKEND FLOW (IPC Communication)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Frontend (oobe-wizard.html)                 Backend (main.js)
────────────────────────────────            ─────────────────

[Test Connection Click]
         │
         │ ipcRenderer.invoke('oobe-test-vault-connection', config)
         │
         └──────────────────────────────────────►  Parse Vault URL
                                                   │
                                                   ▼
                                            Test /v1/sys/health
                                                   │
                                                   ├─► ❌ Timeout
                                                   ├─► ❌ Connection Error
                                                   │
                                                   ▼
                                            Test Read from Path
                                            /v1/{mount}/data/{path}
                                                   │
                                                   ├─► ❌ 404 Path Not Found
                                                   ├─► ❌ 403 Access Denied
                                                   ├─► ❌ Invalid Response
                                                   │
                                                   ▼
                                            ✅ Success
         ◄──────────────────────────────────────┤
         │                                       Return:
         │                                       {
Display Result                                     success: true/false,
         │                                         error: "...",
         │                                         message: "..."
         │                                       }
         ▼
[Next Button Click]
         │
         │ ipcRenderer.invoke('oobe-save-vault-config', config)
         │
         └──────────────────────────────────────►  Create config directory
                                                   ~/.config/taminator-gui/
                                                   │
                                                   ▼
                                            Save vault-config.json:
                                            {
                                              "url": "...",
                                              "token": "...",
                                              "mount": "...",
                                              "path": "...",
                                              "lastVerified": "..."
                                            }
                                                   │
                                                   ▼
         ◄──────────────────────────────────────┤ Return { success: true }
         │
         │ ipcRenderer.invoke('oobe-complete-step', 'vaultSetup')
         │
         └──────────────────────────────────────►  Update OOBE state
                                                   │
                                                   ▼
         ◄──────────────────────────────────────┤ Return { success: true }
         │
         ▼
Navigate to Next Screen


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STATE MANAGEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Frontend State Variables:
  • currentScreen: 0, 1, 2 (welcome, auth-choice, vault-setup)
  • screens: ['welcome', 'auth-choice', 'vault-setup']
  • vaultConnectionTested: false → true (after successful test)
  • selectedAuthMethod: null → 'vault' or 'manual'

Backend State Files:
  • ~/.config/taminator-gui/oobe-state.json
      {
        "firstRun": false,
        "authMethod": "vault",
        "completedSteps": ["authMethod", "vaultSetup"],
        "lastScreen": "vault-setup"
      }

  • ~/.config/taminator-gui/vault-config.json
      {
        "url": "https://vault.example.com:8200",
        "token": "hvs.XXXXXXXXXXXX",
        "mount": "secret",
        "path": "taminator/tokens",
        "lastVerified": "2025-10-24T10:30:00.000Z"
      }


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ERROR HANDLING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Connection Test Errors:

1. Network/Connection
   ❌ "Cannot connect to Vault: ECONNREFUSED"
   → Vault server not running or wrong URL

2. Timeout
   ❌ "Connection timeout - Vault server not responding"
   → Server unreachable or firewall blocking

3. Authentication
   ❌ "Access denied - check your Vault token permissions"
   → Invalid token or insufficient permissions (403)

4. Path Not Found
   ❌ "Secret path not found: taminator/tokens"
   → Path doesn't exist in Vault (404)

5. Invalid Response
   ❌ "Invalid response from Vault"
   → Vault returned unexpected data format

6. Form Validation
   ❌ "Please fill out this field" (browser validation)
   → Required field empty

7. URL Validation
   ❌ "Please enter a valid URL" (browser validation)
   → Invalid URL format


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECURITY CONSIDERATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Implemented:
  • Password field for token (not visible in UI)
  • Token never logged in console
  • HTTPS support with self-signed certs
  • 5-second timeout prevents hanging
  • Local-only config storage

⚠️  TODO (Security Enhancements):
  • Encrypt token in vault-config.json
  • Set file permissions to 600 (user-only)
  • Use system keyring instead of file
  • Token rotation/expiration handling
  • Audit logging for config changes
  • Secure delete on reset


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TESTING MATRIX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌──────────────────────────┬─────────────┬──────────────────────────────┐
│ Test Scenario            │ Expected    │ Result                       │
├──────────────────────────┼─────────────┼──────────────────────────────┤
│ Valid Vault + Token      │ ✅ Success  │ Green box, Next enabled      │
│ Invalid URL format       │ ❌ Validate │ Browser validation error     │
│ Wrong Vault server       │ ❌ Error    │ Connection refused           │
│ Invalid token            │ ❌ Error    │ 403 Access denied            │
│ Wrong secret path        │ ❌ Error    │ 404 Path not found           │
│ Network timeout          │ ❌ Error    │ Timeout message              │
│ Change input after test  │ 🔄 Reset    │ Result hidden, retest needed │
│ Back button              │ ← Navigate  │ Return to auth-choice        │
│ Next without test        │ ❌ Block    │ Alert: "Please test first"   │
│ Form submission          │ 💾 Save     │ Config saved to disk         │
└──────────────────────────┴─────────────┴──────────────────────────────┘


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Immediate:
  1. Test with real Vault server
  2. Implement Screen 3b (Manual Setup)
  3. Implement Screen 4 (Token Verification)
  4. Implement Screen 5 (Completion)

Security:
  5. Add token encryption
  6. Enforce file permissions
  7. Add system keyring support

Integration:
  8. Connect Vault config to main app auth system
  9. Use Vault tokens for JIRA/Portal API calls
  10. Add re-configuration option in Settings tab

Documentation:
  11. User guide with screenshots
  12. Admin guide for Vault setup
  13. Troubleshooting guide


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Last Updated:** October 24, 2025  
**Status:** ✅ Implementation Complete - Ready for Testing

