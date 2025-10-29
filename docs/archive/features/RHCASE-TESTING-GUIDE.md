# rhcase Integration Testing Guide

**Purpose**: Validate that rhcase can connect to Red Hat SupportShell and pull case data  
**Status**: Ready to test  
**Prerequisites**: Red Hat VPN connected, rhcase configured

---

## 🚀 Quick Start

### 1. Start Taminator Service
```bash
cd /home/jbyrd/TAMINATOR/src
python -m taminator.api.main
```

### 2. Run Integration Tests
```bash
# In another terminal
cd /home/jbyrd/TAMINATOR

# Basic API integration test
./test-rhcase-integration.sh

# SupportShell integration test (no case ID)
./test-rhcase-supportshell.sh

# Test with specific case
./test-rhcase-supportshell.sh 04056105
```

---

## 🔍 Debug Logging (NEW!)

**Enable debug logging for rhcase to see detailed execution:**

```bash
# Enable debug for rhcase service
curl -X POST http://127.0.0.1:8765/api/debug/enable \
  -H "Content-Type: application/json" \
  -d '{"module": "taminator.services.rhcase_service"}'

# Check debug status
curl http://127.0.0.1:8765/api/debug/status | jq '.'

# Disable debug
curl -X POST http://127.0.0.1:8765/api/debug/disable \
  -H "Content-Type: application/json" \
  -d '{"module": "taminator.services.rhcase_service"}'

# Enable debug for ALL features (use sparingly!)
curl -X POST http://127.0.0.1:8765/api/debug/enable-all
```

**Available modules for debug:**
- `taminator.services.rhcase_service` - rhcase execution
- `taminator.services.jira_service` - JIRA API
- `taminator.services.portal_service` - Customer Portal
- `taminator.api.routes.rhcase` - rhcase API endpoints
- `taminator.core.token_manager` - Token storage
- `taminator.core.ai_client` - AI integration

---

## 📝 Manual API Testing

### Test rhcase health
```bash
curl http://127.0.0.1:8765/api/rhcase/health | jq '.'
```

**Expected**:
```json
{
  "available": true,
  "path": "/home/jbyrd/.local/bin/rhcase",
  "version": "rhcase 2.9.3",
  "bundled": true
}
```

### Test rhcase doctor (config check)
```bash
curl -X POST http://127.0.0.1:8765/api/rhcase/doctor | jq '.'
```

**Expected**: Shows rhcase configuration status

### List cases for account
```bash
curl -X POST http://127.0.0.1:8765/api/rhcase/list \
  -H "Content-Type: application/json" \
  -d '{"account": "cibc"}' | jq '.'
```

### Analyze specific case
```bash
curl -X POST http://127.0.0.1:8765/api/rhcase/analyze \
  -H "Content-Type: application/json" \
  -d '{"case_id": "04056105"}' | jq '.'
```

### Search KCS articles
```bash
curl -X POST http://127.0.0.1:8765/api/rhcase/kcs/search \
  -H "Content-Type: application/json" \
  -d '{"query": "OpenShift", "limit": 5}' | jq '.'
```

### Search JIRA
```bash
curl -X POST http://127.0.0.1:8765/api/rhcase/jira/search \
  -H "Content-Type: application/json" \
  -d '{"query": "authselect"}' | jq '.'
```

---

## ✅ Success Criteria

### rhcase is properly integrated if:

1. ✅ **Health check passes**
   - rhcase is detected
   - Version is shown
   - Path is correct

2. ✅ **Commands execute via API**
   - No direct shell execution
   - Structured JSON responses
   - Proper error handling

3. ✅ **SupportShell connectivity works**
   - Can list cases
   - Can analyze cases
   - Can search KCS/JIRA
   - Returns real Red Hat data

4. ✅ **Error handling is clear**
   - VPN issues reported
   - Auth failures explained
   - Invalid commands handled

---

## 🐛 Troubleshooting

### Problem: rhcase not found
**Check**:
```bash
which rhcase
rhcase --version
```

**Fix**: Install rhcase from https://gitlab.cee.redhat.com/gvaughn/hatter-pai

### Problem: Authentication failures
**Check**:
```bash
rhcase doctor
```

**Fix**: Run `rhcase config setup` to configure credentials

### Problem: VPN errors
**Symptoms**: "Connection refused", "Network unreachable"  
**Fix**: Connect to Red Hat VPN

### Problem: Service won't start
**Check logs**:
```bash
tail -50 /tmp/taminator-service.log
```

### Problem: API returns 404
**Check**: rhcase routes registered correctly
```bash
curl http://127.0.0.1:8765/docs
# Should show /api/rhcase/* endpoints
```

---

## 📊 Test Results Log

### Date: ___________

| Test | Status | Notes |
|------|--------|-------|
| rhcase health | ⬜ | |
| rhcase doctor | ⬜ | |
| List cases | ⬜ | |
| Analyze case | ⬜ | |
| KCS search | ⬜ | |
| JIRA search | ⬜ | |
| Error handling | ⬜ | |
| Debug logging | ⬜ | |

---

## 🎯 Next Steps After Validation

Once rhcase integration is validated:

1. ✅ Test from GUI (rhcase bot tab)
2. ✅ Test with real customer workflows
3. ✅ Document any issues found
4. ✅ Add to alpha testing checklist

---

**Ready to test? Start with:**
```bash
cd /home/jbyrd/TAMINATOR/src && python -m taminator.api.main
```

Then in another terminal:
```bash
cd /home/jbyrd/TAMINATOR && ./test-rhcase-supportshell.sh
```

