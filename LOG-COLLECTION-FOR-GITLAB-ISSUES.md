# Log Collection for GitLab Issues

**Purpose**: Make it easy for TAMs to report issues with debug information attached  
**Status**: ✅ Complete and Ready  
**Target**: GitLab at `https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues`

---

## 🎯 Workflow

### For TAMs Reporting Issues

**Step 1: Enable Debug Logging (if issue is reproducible)**
```bash
# Enable debug for the problem area
curl -X POST http://127.0.0.1:8765/api/debug/enable \
  -H "Content-Type: application/json" \
  -d '{"module": "taminator.services.rhcase_service"}'
```

**Step 2: Reproduce the Issue**
- Try the action that fails
- Let it fail (logs will capture it)

**Step 3: Collect Diagnostic Package**
```bash
# Option A: Use CLI tool (easiest)
./tam-collect-logs

# Option B: Use API directly
curl -X POST http://127.0.0.1:8765/api/diagnostics/collect \
  -o taminator-diagnostics.tar.gz
```

**Step 4: Create GitLab Issue**
1. Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues/new
2. Title: Brief description (e.g., "rhcase fails to connect to SupportShell")
3. Description: What happened, what you expected, steps to reproduce
4. **Drag the `.tar.gz` file to attach it**
5. Submit

---

## 📦 What's in the Package?

### Files Included

**1. `system-info.json`**
```json
{
  "timestamp": "2025-10-28T11:00:00",
  "taminator_version": "2.0.0",
  "system": {
    "platform": "Linux",
    "python_version": "3.11.0",
    "machine": "x86_64"
  },
  "rhcase": {
    "available": true,
    "path": "/home/jbyrd/.local/bin/rhcase",
    "version": "rhcase 2.9.3"
  },
  "network": {
    "vpn_reachable": true
  }
}
```

**2. `logs.txt`**
- Last 1000 lines from all log files
- Includes timestamps and log levels
- Shows recent operations

**3. `debug-settings.json`**
- Which debug flags were enabled
- Helps reproduce issue

**4. `README.txt`**
- Instructions for attaching to GitLab
- Privacy notice

---

## 🔒 Privacy & Security

### What's Included
- ✅ System information (OS, Python version)
- ✅ Taminator version
- ✅ rhcase availability
- ✅ Recent log entries
- ✅ Debug settings

### What's NOT Included
- ❌ No passwords or API tokens
- ❌ No customer data (unless in logs)
- ❌ No personal files

### ⚠️ Warning: Review Before Sharing

Logs may contain:
- Customer names
- Case IDs  
- Account names
- Error messages with paths

**Recommendation**: Extract and review `logs.txt` before attaching if concerned about sensitive data:
```bash
tar -xzf taminator-diagnostics-20251028-110000.tar.gz
cat taminator-diagnostics/logs.txt | less
```

---

## 🛠️ CLI Tool: `tam-collect-logs`

### Usage
```bash
# Basic usage (auto-detects if service running)
./tam-collect-logs

# Output
📦 Taminator Log Collection

✅ Service is running - collecting via API
Collecting diagnostics...

✅ Diagnostics package created
   File: taminator-diagnostics-20251028-110515.tar.gz
   Size: 45K

📋 To attach to GitLab issue:
   1. Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues/new
   2. Describe your issue
   3. Drag taminator-diagnostics-20251028-110515.tar.gz to attach
   4. Submit

⚠️  Review the package contents first:
   tar -tzf taminator-diagnostics-20251028-110515.tar.gz
   (contains logs which may have customer names/case IDs)
```

### Where It Saves
- Current directory
- Filename: `taminator-diagnostics-YYYYMMDD-HHMMSS.tar.gz`

---

## 🌐 API Endpoints

### `POST /api/diagnostics/collect`

**Description**: Create diagnostics package

**Parameters**:
- `lines` (optional): Number of log lines to include (default: 1000)

**Returns**: `.tar.gz` file for download

**Example**:
```bash
curl -X POST "http://127.0.0.1:8765/api/diagnostics/collect?lines=2000" \
  -o my-diagnostics.tar.gz
```

### `GET /api/diagnostics/info`

**Description**: Get diagnostic info without creating package

**Returns**: JSON with system info and log file stats

**Example**:
```bash
curl http://127.0.0.1:8765/api/diagnostics/info | jq '.'
```

**Response**:
```json
{
  "success": true,
  "info": {
    "timestamp": "2025-10-28T11:00:00",
    "taminator_version": "2.0.0",
    "system": {...},
    "rhcase": {...},
    "log_files": [
      {
        "name": "taminator.log",
        "size_mb": 2.5,
        "modified": "2025-10-28T10:59:00"
      }
    ]
  }
}
```

---

## 📋 Recommended Issue Template

```markdown
## Issue Description
[Brief description of the problem]

## Steps to Reproduce
1. 
2. 
3. 

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happened]

## Environment
- Taminator Version: [from diagnostics package]
- OS: [from diagnostics package]
- rhcase Version: [from diagnostics package]

## Debug Information
[Attach taminator-diagnostics-YYYYMMDD-HHMMSS.tar.gz]

## Additional Context
[Any other relevant information]
```

---

## 🧪 Testing the Feature

### Test 1: Collect Logs (Service Running)
```bash
# Start service
cd /home/jbyrd/TAMINATOR/src
python -m taminator.api.main &

# Collect logs
cd /home/jbyrd/TAMINATOR
./tam-collect-logs

# Verify package created
ls -lh taminator-diagnostics-*.tar.gz

# Extract and inspect
tar -xzf taminator-diagnostics-*.tar.gz
cat taminator-diagnostics/README.txt
```

### Test 2: Collect Logs (Service Not Running)
```bash
# Stop service
pkill -f taminator.api.main

# Collect logs (should work manually)
./tam-collect-logs
```

### Test 3: API Collection
```bash
curl -X POST http://127.0.0.1:8765/api/diagnostics/collect \
  -o test-diagnostics.tar.gz

# Verify
file test-diagnostics.tar.gz
tar -tzf test-diagnostics.tar.gz
```

---

## 🚀 Future Enhancements

### GUI Integration
Add "Report Issue" button that:
1. Collects logs automatically
2. Opens GitLab issue creation page
3. Shows preview of what's being sent

### Auto-Sanitization
- Remove customer-identifying information
- Redact case IDs
- Hash account names

### Crash Reports
- Automatically collect on crash
- Prompt user to report
- One-click submission

---

## ✅ Benefits

1. **For TAMs**:
   - One command to collect everything
   - No need to find log files manually
   - Easy to attach to issues

2. **For Developers (you)**:
   - Get all needed info in one package
   - System info included automatically
   - Debug settings captured

3. **For Support**:
   - Consistent bug reports
   - All context in one place
   - Faster resolution

---

## 📊 Summary

**Commands**:
```bash
# Collect logs
./tam-collect-logs

# Or via API
curl -X POST http://127.0.0.1:8765/api/diagnostics/collect \
  -o diagnostics.tar.gz
```

**Result**: Ready-to-attach `.tar.gz` file with:
- System info
- Recent logs
- Debug settings
- README with instructions

**GitLab**: https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues/new

---

**Now TAMs can easily report issues with complete debug information!** 🎉

