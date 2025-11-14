# Debugging Taminator with Ansai Development Tools

This guide shows how to use Ansai's development workflow architecture for debugging Taminator.

## 🎯 Quick Start

```bash
cd /home/jbyrd/TAMINATOR
ansible-playbook ansible/playbooks/taminator-dev.yml
```

This launches an interactive menu with 15 development workflows specifically tailored for Taminator.

## 📋 Available Workflows

| # | Workflow | Use Case |
|---|----------|----------|
| 1 | Setup Dev Environment | First-time setup: installs pytest, black, flake8, etc. |
| 2 | Run Tests | Execute Taminator's test suite |
| 3 | Code Quality Check | Lint and format code |
| 4 | Test FastAPI Service | Verify service is running and healthy |
| 5 | Interactive Debug | IPython shell with Taminator modules loaded |
| 6 | Service Logs (Live) | Tail service logs in real-time |
| 7 | Test JIRA Connection | Verify JIRA API accessibility |
| 8 | Test Portal Connection | Verify Red Hat Portal API |
| 9 | Test AI Intelligence | Check AI models and intelligence engine |
| 10 | Database Inspector | Explore SQLite intelligence database |
| 11 | Clear Cache | Remove Python bytecode cache |
| 12 | Service Restart | Instructions to restart FastAPI service |
| 13 | API Test Suite | Test all API endpoints |
| 14 | View Recent Errors | Show error logs from service |
| 15 | Performance Profiling | Profile service performance |

## 🔍 Common Debugging Scenarios

### Scenario 1: Service Won't Start

```bash
ansible-playbook ansible/playbooks/taminator-dev.yml
# Select: 4 (Test FastAPI Service)
```

This checks if the service is running and shows health status.

If offline:
```bash
# Select: 14 (View Recent Errors)
# Then check logs with: 6 (Service Logs Live)
```

### Scenario 2: JIRA Integration Failing

```bash
ansible-playbook ansible/playbooks/taminator-dev.yml
# Select: 7 (Test JIRA Connection)
```

This tests:
- Service availability
- JIRA token validity
- VPN connectivity

### Scenario 3: AI Intelligence Issues

```bash
ansible-playbook ansible/playbooks/taminator-dev.yml
# Select: 9 (Test AI Intelligence)
```

Verifies:
- AI modules can be imported
- Models are accessible
- Intelligence engine is working

Then inspect the database:
```bash
# Select: 10 (Database Inspector)
```

### Scenario 4: Need to Debug API Calls

```bash
ansible-playbook ansible/playbooks/taminator-dev.yml
# Select: 5 (Interactive Debug)
```

This gives you an IPython shell with:

```python
>>> import httpx
>>> # Test health endpoint
>>> response = httpx.get('http://127.0.0.1:8765/health')
>>> response.json()

>>> # Test JIRA endpoint
>>> response = httpx.get('http://127.0.0.1:8765/api/jira/status')
>>> response.json()

>>> # Import and test services directly
>>> from taminator.services.ai_client import AIClient
>>> # ... debug AI client
```

### Scenario 5: Performance Issues

```bash
ansible-playbook ansible/playbooks/taminator-dev.yml
# Select: 15 (Performance Profiling)
```

Follow the instructions to:
- CPU profile with py-spy
- Memory profile with memory_profiler
- Load test with locust

### Scenario 6: Code Quality Before Commit

```bash
ansible-playbook ansible/playbooks/taminator-dev.yml
# Select: 3 (Code Quality Check)
```

Runs:
- Black formatter
- Flake8 linter

Auto-fix formatting:
```bash
cd /home/jbyrd/TAMINATOR
source venv/bin/activate
black src/ bin/
```

### Scenario 7: Test Suite Failures

```bash
ansible-playbook ansible/playbooks/taminator-dev.yml
# Select: 2 (Run Tests)
```

Shows detailed pytest output with failures.

## 🛠️ Manual Debugging Commands

### Service Management

```bash
# Check if service is running
curl http://127.0.0.1:8765/health | jq '.'

# View service logs
tail -f ~/.local/state/taminator/log/taminator.log

# Find service process
ps aux | grep taminator-service

# Restart service
kill <PID>
cd /home/jbyrd/TAMINATOR
./bin/taminator-service &
```

### API Testing

```bash
# Interactive API docs
firefox http://127.0.0.1:8765/docs

# Test endpoints with curl
curl http://127.0.0.1:8765/api/customers | jq '.'
curl http://127.0.0.1:8765/api/jira/status | jq '.'
```

### Database Inspection

```bash
# Find intelligence database
find ~/.config/taminator -name "*.db"

# Open with sqlite3
sqlite3 ~/.config/taminator/intelligence.db

# SQLite commands:
.tables                    # List tables
.schema email_analysis     # Show table schema
SELECT * FROM email_analysis LIMIT 10;  # Query data
```

### Python Debugging

```bash
# Activate venv
cd /home/jbyrd/TAMINATOR
source venv/bin/activate

# Launch IPython with context
export PYTHONPATH=/home/jbyrd/TAMINATOR/src:$PYTHONPATH
ipython

# In IPython:
>>> from taminator.services.ai_client import AIClient
>>> from taminator.services.jira_service import JiraService
>>> import httpx
```

## 🔗 Integration with Ansai Architecture

The Taminator development workflow is modeled after Ansai's development tools:

### Shared Concepts

1. **Interactive Menu** - Same UX pattern as Ansai
2. **Testing Infrastructure** - pytest, black, flake8
3. **Interactive Debugging** - IPython with pre-loaded context
4. **Service Testing** - Connection verification
5. **Log Monitoring** - Real-time log tailing
6. **Performance Profiling** - CPU, memory, API profiling

### Differences

- **Taminator**: FastAPI service, Electron GUI, AI intelligence
- **Ansai**: Plaid/Actual Budget sync, systemd service

But the debugging workflow is the same!

## 📚 Resources

### Taminator Documentation
- Main README: `/home/jbyrd/TAMINATOR/README.md`
- Getting Started: `/home/jbyrd/TAMINATOR/GETTING-STARTED.md`
- API Docs (when running): http://127.0.0.1:8765/docs

### Ansai Documentation (Reference)
- Development Guide: `/home/jbyrd/pai/repositories/pai-personal-finance/DEVELOPMENT.md`
- Dev Workflow: `/home/jbyrd/pai/repositories/pai-personal-finance/ansible/playbooks/ansai-dev.yml`

### Service Locations
- Service Logs: `~/.local/state/taminator/log/taminator.log`
- Config: `~/.config/taminator/`
- Data: `~/taminator-test-data/`
- Intelligence DB: `~/.config/taminator/*.db`

## 🎓 Best Practices

### Before Starting Debugging Session

1. **Check service health**
   ```bash
   ansible-playbook ansible/playbooks/taminator-dev.yml  # Option 4
   ```

2. **View recent errors**
   ```bash
   ansible-playbook ansible/playbooks/taminator-dev.yml  # Option 14
   ```

3. **Clear cache if needed**
   ```bash
   ansible-playbook ansible/playbooks/taminator-dev.yml  # Option 11
   ```

### During Debugging

- Use **Option 5 (Interactive Debug)** for exploratory debugging
- Use **Option 6 (Service Logs Live)** to watch logs while testing
- Use **Option 13 (API Test Suite)** to verify endpoints

### After Fixing Issues

- Run **Option 2 (Run Tests)** to verify fixes
- Run **Option 3 (Code Quality)** before committing
- Check **Option 4 (Service Health)** to ensure service is stable

## 🚀 Quick Reference Card

```bash
# Main entry point
cd /home/jbyrd/TAMINATOR
ansible-playbook ansible/playbooks/taminator-dev.yml

# Common workflows:
# 1  - First-time setup
# 4  - Is service running?
# 5  - Interactive debugging
# 6  - Watch logs
# 7  - Test JIRA
# 9  - Test AI
# 14 - Show errors
```

## 💡 Tips & Tricks

### Tip 1: Keep Logs Open
Open a split terminal with logs while debugging:
```bash
# Terminal 1: Run dev workflow
ansible-playbook ansible/playbooks/taminator-dev.yml

# Terminal 2: Watch logs
tail -f ~/.local/state/taminator/log/taminator.log
```

### Tip 2: Quick API Testing
Use the interactive API docs:
```bash
firefox http://127.0.0.1:8765/docs
```

Try out endpoints directly in the browser.

### Tip 3: Fast Iteration
```bash
# Make code changes
# Then: ansible-playbook ansible/playbooks/taminator-dev.yml
# Select: 4 (test), 2 (run tests), 3 (quality check)
```

### Tip 4: Save Debug Sessions
The interactive debugger supports IPython magic commands:
```python
>>> %save my_session.py 1-50  # Save commands 1-50
>>> %history  # View command history
```

## 🤝 Acknowledgments

This development workflow is based on the Ansai Personal Finance development tools architecture, demonstrating the reusability of well-designed development workflows across different Python projects.

---

**Happy debugging! 🐛🔧**




