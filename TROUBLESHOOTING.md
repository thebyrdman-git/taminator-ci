# Taminator v2.0 - Troubleshooting Guide

**Common issues and how to fix them**

---

## 🚨 Quick Diagnostics

### Check Service Health

**Status Bar** (bottom of window):
- 🟢 **Green** = Healthy, everything working
- 🟡 **Yellow** = Warning, partial functionality
- 🔴 **Red** = Error, needs attention

**Click status item** → See detailed tooltip

**Check API health**:
```bash
curl http://127.0.0.1:8765/health | jq '.'
```

### Collect Debug Logs

**Via GUI**:
1. Settings → Debug Logging
2. Enable debug for relevant features
3. Reproduce issue
4. Click **"Download Diagnostics"**
5. Attach `.tar.gz` to GitLab issue

**Via Terminal**:
```bash
# View live logs
tail -f ~/.local/state/taminator/log/taminator.log

# Last 100 lines
tail -100 ~/.local/state/taminator/log/taminator.log

# Search logs
grep "ERROR" ~/.local/state/taminator/log/taminator.log
```

---

## Service Issues

### "Service Offline" / Service Won't Start

**Symptoms**:
- Status bar shows "Service: Offline" (red)
- GUI says "Waiting for service..."
- API calls fail with connection error

**Causes & Solutions**:

#### 1. Service Starting Up (Normal)
**Wait**: Service takes 2-5 seconds to start  
**Check**: Status bar will turn green when ready

#### 2. Port 8765 Already in Use
**Diagnosis**:
```bash
lsof -i :8765
```

**Solution**:
```bash
# Kill existing service
pkill -f "taminator.api.main"

# Restart Taminator
```

#### 3. Python Dependencies Missing
**Diagnosis**:
```bash
tail ~/.local/state/taminator/log/taminator.log
# Look for ImportError or ModuleNotFoundError
```

**Solution**:
```bash
# If running from source (not AppImage)
pip install -r requirements.txt
```

#### 4. Service Crashed
**Diagnosis**:
```bash
tail -50 ~/.local/state/taminator/log/taminator.log
# Look for traceback or "Shutting down"
```

**Solution**:
- Service has auto-restart (watchdog)
- Wait 10 seconds for auto-recovery
- If persists, restart Taminator
- If still fails, collect logs and report bug

**Check watchdog status**:
```bash
curl http://127.0.0.1:8765/health/live
```

---

## Authentication Issues

### "JIRA Token Not Configured"

**Symptoms**:
- Dashboard shows "Configure tokens in settings"
- Check/Update/Post operations fail

**Solution**:
1. Settings → Authentication
2. Click **"Add JIRA Token"**
3. Paste token from https://access.redhat.com/management/api
4. Click **"Test Token"**
5. ✅ Green checkmark = success

**Generate new token**:
1. Visit https://access.redhat.com/management/api
2. Click **"Generate Token"**
3. Copy token (looks like `MTE1NjQyMD...`)

### "JIRA Token Invalid" / "JIRA Token Expired"

**Symptoms**:
- Error toast: "🔐 JIRA token expired or invalid"
- Status bar: "Tokens: Missing" (yellow)

**Solution**:
1. Regenerate token at https://access.redhat.com/management/api
2. Settings → Authentication → Update JIRA Token
3. Paste new token
4. Test token

**Why tokens expire**:
- Red Hat API tokens expire after 90 days
- Token may be revoked if security incident
- Check Red Hat SSO status

### "Portal Token Invalid"

**Symptoms**:
- Post to Portal fails
- Error: "📰 Customer Portal authentication failed"

**Solution**:
1. Regenerate at https://access.redhat.com/management/api
2. Settings → Authentication → Update Portal Token
3. Test token

**Note**: Portal token is **optional** (only needed for posting)

---

## Network Issues

### "VPN Not Connected"

**Symptoms**:
- Status bar shows "VPN: Disconnected" (yellow)
- JIRA/Portal operations fail with connection error
- Error: "Cannot connect to JIRA. Check VPN connection."

**Diagnosis**:
```bash
# Test JIRA connectivity
ping issues.redhat.com

# Test Portal connectivity
ping access.redhat.com
```

**Solution**:
1. Connect to Red Hat VPN
2. Verify connection:
   ```bash
   ping issues.redhat.com
   ```
3. Refresh Taminator (Ctrl+R)

**VPN connection help**:
- https://source.redhat.com/groups/public/it-ux/red_hat_it_ux_wiki/vpn

### "Connection Timeout"

**Symptoms**:
- Operations take 30+ seconds then fail
- Error: "Request timed out"

**Causes & Solutions**:

#### 1. Slow Network
**Solution**: Increase timeout in Settings → Advanced → Timeout (future)

#### 2. VPN Disconnected Mid-Request
**Solution**: 
- Reconnect VPN
- Retry operation

#### 3. JIRA/Portal API Slow
**Solution**: 
- Wait and retry
- Check Red Hat status: https://status.redhat.com

### "JIRA Rate Limit Reached"

**Symptoms**:
- Error: "⏱️ API rate limit reached. Retry in 60s"
- Multiple operations fail in quick succession

**Solution**:
- Wait for rate limit to reset (shown in error)
- Taminator will auto-retry after wait period
- Reduce frequency of operations

**Rate limits** (Red Hat JIRA):
- 100 requests per minute per user
- 1000 requests per hour per user

---

## Customer Data Issues

### "Customer Not Found"

**Symptoms**:
- Check/Update/Post fails
- Error: "📁 Customer not found: <customer-id>"

**Solution**:
1. Verify customer is onboarded:
   ```bash
   tam-rfe dashboard
   ```
2. If missing, onboard customer:
   ```bash
   tam-rfe onboard <customer-slug> --account <number> --product <product>
   ```

**Check customer file**:
```bash
ls ~/taminator-test-data/<customer-slug>.md
```

### "No Customers Found"

**Symptoms**:
- Dashboard empty
- Dropdown lists empty

**Solution**:
1. Onboard first customer:
   - GUI: Customers tab → **"+ Add Customer"**
   - CLI: `tam-rfe onboard <slug> --account <number> --product <product>`

2. Verify data directory:
   ```bash
   ls ~/taminator-test-data/
   ```

### "Failed to Parse Customer Data"

**Symptoms**:
- Dashboard shows partial data
- Error: "Failed to load customer: <customer>"

**Diagnosis**:
```bash
# Check report file
cat ~/taminator-test-data/<customer-slug>.md

# Look for:
# - Missing YAML frontmatter (---)
# - Invalid markdown syntax
# - Corrupted file
```

**Solution**:
1. Back up corrupted file:
   ```bash
   cp ~/taminator-test-data/<customer>.md ~/taminator-test-data/<customer>.md.broken
   ```
2. Re-onboard customer:
   ```bash
   tam-rfe onboard <customer> --account <number> --product <product>
   ```

---

## rhcase Integration Issues

### "rhcase Command Not Found"

**Symptoms**:
- rhcase Bot tab shows "rhcase not available"
- Status: rhcase: unavailable

**Diagnosis**:
```bash
# Check if rhcase is bundled
which rhcase

# Check rhcase service health
curl http://127.0.0.1:8765/api/rhcase/health | jq '.'
```

**Solution (AppImage)**:
- rhcase should be bundled automatically
- If missing, report bug

**Solution (Source)**:
```bash
# Clone rhcase repo
git clone https://gitlab.cee.redhat.com/gvaughn/hatter-pai.git
cd hatter-pai/bin

# Copy to system PATH
cp rhcase ~/.local/bin/
chmod +x ~/.local/bin/rhcase

# Verify
rhcase --version
```

### "rhcase Command Failed"

**Symptoms**:
- rhcase command runs but returns error
- Exit code: non-zero

**Diagnosis**:
```bash
# Enable debug logging
# In Settings → Debug Logging
# Enable: taminator.services.rhcase_service

# Reproduce issue
# Check logs for detailed error
```

**Common causes**:
- Invalid account number
- VPN not connected
- SupportShell authentication required
- rhcase service down

**Solution**:
1. Verify VPN: `ping issues.redhat.com`
2. Test rhcase manually:
   ```bash
   rhcase --version
   rhcase list <account-number>
   ```
3. If manual test fails, issue is with rhcase tool itself (not Taminator)

---

## GUI Issues

### "Blank Screen" / "App Won't Load"

**Symptoms**:
- Taminator opens but shows blank white screen
- No content visible

**Solution**:
1. Check service is running:
   ```bash
   curl http://127.0.0.1:8765/health
   ```
2. Open DevTools (dev mode only):
   ```bash
   ./Taminator-2.0.0.AppImage --dev
   ```
3. Check browser console for JavaScript errors
4. Restart Taminator

### "Loading... Never Completes"

**Symptoms**:
- Spinner runs indefinitely
- Operations never complete

**Diagnosis**:
- Check status bar: Is service online?
- Check network: Is VPN connected?
- Check logs: Are there errors?

**Solution**:
1. Refresh dashboard (Ctrl+R)
2. Restart Taminator
3. Check service logs for errors

### "Toast Notifications Don't Dismiss"

**Symptoms**:
- Error toasts stay on screen
- Can't click "Dismiss"

**Solution**:
- Click **"×"** button on right side of toast
- Toasts auto-dismiss after timeout (success: 3s, error: no timeout)
- Refresh page if stuck: Ctrl+R

---

## Performance Issues

### "Taminator is Slow"

**Symptoms**:
- Operations take 10+ seconds
- GUI feels laggy

**Diagnosis**:
```bash
# Check system resources
top | grep taminator

# Check service performance
curl http://127.0.0.1:8765/health | jq '.system'
```

**Solutions**:

#### 1. Too Many Customers
- Paginate dashboard (future feature)
- Archive old customers

#### 2. Slow Network
- Check VPN connection
- Check Red Hat API status

#### 3. Low System Resources
- Close other applications
- Increase RAM allocation (if VM)

### "High Memory Usage"

**Symptoms**:
- Taminator uses >1 GB RAM
- System slows down

**Diagnosis**:
```bash
# Check memory usage
ps aux | grep taminator

# Or
htop | grep taminator
```

**Solution**:
- Restart Taminator (clears cache)
- Report bug if persists

---

## Debug Logging

### Enable Debug Logging

**Via GUI** (recommended):
1. Settings → Debug Logging
2. Find module to debug
3. Click **"Enable Debug"**
4. Reproduce issue
5. Check logs in **"View Logs"**

**Via API**:
```bash
# Enable debug for specific module
curl -X POST http://127.0.0.1:8765/api/debug/enable \
  -H "Content-Type: application/json" \
  -d '{"module": "taminator.services.jira_service"}'

# Check current debug settings
curl http://127.0.0.1:8765/api/debug/settings | jq '.'

# Disable debug
curl -X POST http://127.0.0.1:8765/api/debug/disable \
  -H "Content-Type: application/json" \
  -d '{"module": "taminator.services.jira_service"}'
```

### Debug Modules

| Module | Purpose |
|--------|---------|
| `taminator.services.rhcase_service` | rhcase command execution |
| `taminator.services.jira_service` | JIRA API calls |
| `taminator.services.portal_service` | Customer Portal API |
| `taminator.services.customer_service` | Customer data management |
| `taminator.core.token_manager` | Token storage/retrieval |
| `taminator.api.routes.*` | API endpoint handlers |

### Collect Diagnostics

**For bug reports**:
```bash
# Via GUI
Settings → Debug Logging → "Download Diagnostics"

# Via CLI (future)
./tam-collect-logs

# Manual collection
tar -czf taminator-debug-$(date +%F).tar.gz \
  ~/.local/state/taminator/log/ \
  ~/.config/taminator/ \
  ~/.config/taminator-gui/
```

**Attach to GitLab issue**: https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues/new

---

## Known Issues

### Issue: DevTools Opens in Production

**Status**: Should not happen (fixed in v2.0)  
**Workaround**: Close DevTools window  
**Resolution**: Report bug if DevTools opens without `--dev` flag

### Issue: Service Fails to Auto-Restart

**Status**: Watchdog should restart crashed service  
**Workaround**: Manually restart Taminator  
**Resolution**: Check logs, report bug

### Issue: Tokens Not Persisting

**Status**: OS keyring integration issue  
**Diagnosis**:
```bash
# Check keyring availability
python3 -c "import keyring; print(keyring.get_keyring())"
```
**Workaround**: Use environment variables for tokens  
**Resolution**: Install keyring backend for your OS

### Issue: rhcase Output Truncated

**Status**: Known limitation in v2.0  
**Workaround**: Use `rhcase` CLI directly in terminal  
**Resolution**: Improved output handling in v2.1

---

## Still Having Issues?

### Before Reporting a Bug

**Check these first**:
- ✅ Read this troubleshooting guide
- ✅ Check GitLab issues: https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
- ✅ Verify VPN connection
- ✅ Verify tokens are valid
- ✅ Check service is running (`curl http://127.0.0.1:8765/health`)
- ✅ Review logs (`tail ~/.local/state/taminator/log/taminator.log`)

### Report a Bug

**Required information**:
1. **Taminator version**: Settings → About
2. **Operating system**: Linux (RHEL 9), macOS, Windows
3. **Error message**: Exact text or screenshot
4. **Steps to reproduce**: What did you do?
5. **Expected behavior**: What should have happened?
6. **Actual behavior**: What actually happened?
7. **Logs**: Attach diagnostics file

**Create issue**:
1. Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues/new
2. Fill in template
3. Attach diagnostics
4. Tag with `bug` label
5. Submit

### Get Help

**Contact options**:
- **GitLab Issues**: https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
- **Email**: jbyrd@redhat.com
- **Slack**: *(channel TBD)*

**Response time**:
- Critical bugs: 1-2 business days
- Other issues: 3-5 business days
- Feature requests: Triaged quarterly

---

## Appendix: Error Codes

### Service Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| `service_unavailable` | Backend offline | Wait for auto-restart |
| `network_error` | Network issue | Check VPN |
| `auth_token_missing` | Token not configured | Add token in Settings |
| `auth_token_invalid` | Token expired/wrong | Regenerate token |
| `auth_token_expired` | Token expired | Regenerate token |
| `jira_auth_failed` | JIRA authentication failed | Check JIRA token |
| `portal_auth_failed` | Portal authentication failed | Check Portal token |
| `jira_rate_limit` | Too many requests | Wait for reset |
| `portal_rate_limit` | Too many requests | Wait for reset |
| `customer_not_found` | Customer not onboarded | Onboard customer |
| `rhcase_unavailable` | rhcase tool not found | Install rhcase |
| `rhcase_command_failed` | rhcase error | Check command syntax |

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (check syntax) |
| 401 | Authentication failed |
| 403 | Forbidden (check permissions) |
| 404 | Not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error (report bug) |
| 503 | Service unavailable |

---

**Document Version**: 1.0  
**Last Updated**: October 28, 2025  
**Software Version**: Taminator 2.0.0  
**Status**: Alpha

