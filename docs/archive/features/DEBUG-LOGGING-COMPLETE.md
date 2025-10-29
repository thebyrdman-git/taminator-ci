# Debug Logging Feature Complete

**Date**: October 28, 2025  
**Feature**: Per-Feature Debug Logging  
**Status**: ✅ Implemented, Ready to Test

---

## ✨ What Was Built

### Problem
- No way to enable debug logging for specific features
- Either all logs at INFO (miss details) or all at DEBUG (overwhelming)
- Hard to troubleshoot specific components

### Solution
**Per-feature debug logging with API control**

---

## 🎯 Features

### 1. Granular Control
Enable DEBUG level for specific modules without flooding logs:
- ✅ rhcase service
- ✅ JIRA service
- ✅ Portal service  
- ✅ Customer service
- ✅ Token manager
- ✅ AI client
- ✅ All API routes

### 2. Persistent Settings
Debug settings saved to `~/.config/taminator/debug_settings.json`  
Survives service restarts

### 3. API Endpoints
- `GET /api/debug/status` - Show current debug status
- `POST /api/debug/enable` - Enable debug for module
- `POST /api/debug/disable` - Disable debug for module
- `POST /api/debug/enable-all` - Enable all (troubleshooting)
- `POST /api/debug/disable-all` - Disable all

---

## 📝 Usage Examples

### Check Debug Status
```bash
curl http://127.0.0.1:8765/api/debug/status | jq '.'
```

**Response**:
```json
{
  "debug_modules": {
    "taminator.services.rhcase_service": true,
    "taminator.services.jira_service": false
  },
  "available_modules": [
    "taminator.services.rhcase_service",
    "taminator.services.jira_service",
    "taminator.services.portal_service",
    "taminator.services.customer_service",
    "taminator.api.routes.rhcase",
    "taminator.api.routes.jira",
    "taminator.api.routes.portal",
    "taminator.api.routes.customers",
    "taminator.core.token_manager",
    "taminator.core.ai_client"
  ]
}
```

### Enable Debug for rhcase
```bash
curl -X POST http://127.0.0.1:8765/api/debug/enable \
  -H "Content-Type: application/json" \
  -d '{"module": "taminator.services.rhcase_service"}'
```

**Response**:
```json
{
  "success": true,
  "message": "Debug logging enabled for taminator.services.rhcase_service",
  "module": "taminator.services.rhcase_service",
  "debug_enabled": true
}
```

**Service logs will now show**:
```
[2025-10-28 11:00:00] INFO - 🔍 Debug logging enabled for: taminator.services.rhcase_service
[2025-10-28 11:00:05] DEBUG - 🤖 Executing: /home/jbyrd/.local/bin/rhcase analyze 12345
[2025-10-28 11:00:08] DEBUG - Command output: [detailed output here]
[2025-10-28 11:00:08] INFO - ✅ rhcase command succeeded (exit code: 0)
```

### Disable Debug
```bash
curl -X POST http://127.0.0.1:8765/api/debug/disable \
  -H "Content-Type: application/json" \
  -d '{"module": "taminator.services.rhcase_service"}'
```

### Enable All (Nuclear Option)
```bash
# WARNING: Very verbose!
curl -X POST http://127.0.0.1:8765/api/debug/enable-all
```

---

## 🔧 Implementation Details

### Files Created
1. **`src/taminator/core/debug_logging.py`**
   - `DebugLogManager` class
   - Load/save settings
   - Apply log levels dynamically

2. **`src/taminator/api/routes/debug.py`**
   - API endpoints for debug control
   - Request/response models

### Files Modified
1. **`src/taminator/api/main.py`**
   - Register debug router

### Settings File
**Location**: `~/.config/taminator/debug_settings.json`

**Format**:
```json
{
  "taminator.services.rhcase_service": true,
  "taminator.services.jira_service": false,
  "taminator.api.routes.rhcase": true
}
```

---

## 🎯 Use Cases

### 1. Troubleshooting rhcase Issues
```bash
# Enable debug for rhcase
curl -X POST http://127.0.0.1:8765/api/debug/enable \
  -H "Content-Type: application/json" \
  -d '{"module": "taminator.services.rhcase_service"}'

# Run rhcase command
curl -X POST http://127.0.0.1:8765/api/rhcase/analyze \
  -H "Content-Type: application/json" \
  -d '{"case_id": "12345"}'

# Check logs for detailed execution
tail -f ~/.local/state/taminator/log/taminator.log

# Disable when done
curl -X POST http://127.0.0.1:8765/api/debug/disable \
  -H "Content-Type: application/json" \
  -d '{"module": "taminator.services.rhcase_service"}'
```

### 2. Debug JIRA Integration
```bash
curl -X POST http://127.0.0.1:8765/api/debug/enable \
  -H "Content-Type: application/json" \
  -d '{"module": "taminator.services.jira_service"}'

# Now JIRA API calls show full request/response details
```

### 3. Debug Token Issues
```bash
curl -X POST http://127.0.0.1:8765/api/debug/enable \
  -H "Content-Type: application/json" \
  -d '{"module": "taminator.core.token_manager"}'

# See detailed keyring operations
```

---

## 🚀 GUI Integration (Future)

**Settings Page could include:**
```
┌─ Debug Logging ────────────────────────┐
│                                         │
│ ☐ rhcase Service                       │
│ ☐ JIRA Service                         │
│ ☐ Portal Service                       │
│ ☐ Token Manager                        │
│ ☐ AI Client                            │
│                                         │
│ [Enable All] [Disable All]             │
│                                         │
│ Logs location:                          │
│ ~/.local/state/taminator/log/          │
│                                         │
│ [View Logs]                             │
└─────────────────────────────────────────┘
```

---

## ✅ Testing Checklist

- [ ] Enable debug for rhcase service
- [ ] Execute rhcase command
- [ ] Verify DEBUG logs appear
- [ ] Disable debug for rhcase
- [ ] Verify DEBUG logs stop
- [ ] Settings persist after restart
- [ ] Enable-all works
- [ ] Disable-all works

---

## 🎯 Benefits

1. **Faster Troubleshooting**
   - See exactly what rhcase commands are executed
   - Full request/response details
   - No log noise from other features

2. **Better Support**
   - Can ask users to enable debug for specific feature
   - Get detailed logs without overwhelming output
   - Pin point issues quickly

3. **Development**
   - Debug one feature at a time
   - Test fixes in isolation
   - Less log scrolling

---

**Summary**: Now you can enable detailed logging for ANY feature without drowning in logs. Perfect for troubleshooting rhcase SupportShell connectivity!

