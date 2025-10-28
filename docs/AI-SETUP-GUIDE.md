# 🤖 AI Features Setup Guide

Taminator includes powerful AI features for TAM productivity. This guide explains why models aren't bundled and how to set them up.

## 🎯 What AI Features Do

### Smart Assistance
- **Email Composition**: Draft professional customer responses
- **Report Analysis**: Extract insights from RFE/Bug reports
- **Issue Prioritization**: Suggest which issues need attention
- **Meeting Notes**: Convert meeting recordings to action items

### Technical Analysis
- **Case Pattern Detection**: Find similar issues across customers
- **Root Cause Suggestions**: Analyze logs and suggest solutions
- **Documentation Search**: Find relevant KB articles automatically

---

## ❓ Why Aren't Models Built-In?

### Size Constraints
```
Granite 8B model:        ~8GB
Mistral 7B model:        ~7GB
Embedding models:        ~2GB each
Total:                   ~20GB+

Current Taminator AppImage:  ~200MB
With models bundled:          ~20GB (100x larger!)
```

**Impact:**
- Download times: 2 minutes → 3+ hours
- Disk space: Minimal → Requires 50GB+ free
- Updates: Download full 20GB every release
- Distribution: Red Hat GitLab would choke

### Model Management
- **Updates**: Red Hat AI team releases model updates monthly
- **Sharing**: LiteLLM proxy shared across all PAI tools (efficiency)
- **Flexibility**: Switch models without reinstalling Taminator
- **Compliance**: Centralized control of AIA-approved models

### Red Hat Compliance
- **Data Protection**: Customer data processed via Red Hat VPN
- **Audit Trail**: Centralized logging of AI usage
- **Model Approval**: AIA approves models separately from tools
- **Network Security**: Models run on Red Hat infrastructure only

---

## ✅ Setup Guide (10 Minutes)

### Prerequisites
- ✅ Red Hat VPN connected
- ✅ Python 3.8+ installed
- ✅ Access to Red Hat internal network

### Option A: PAI Full Install (Recommended)

If you're using the PAI (Personal AI Infrastructure) system:

```bash
# 1. Install PAI tools (includes LiteLLM)
git clone https://github.com/your-org/pai.git ~/pai
cd ~/pai
./install.sh

# 2. Start LiteLLM proxy
pai-litellm-start

# 3. Verify setup
pai-litellm-test
```

**Done!** Restart Taminator and AI features will auto-enable.

---

### Option B: Standalone LiteLLM

If you only want AI for Taminator:

```bash
# 1. Install LiteLLM
pip install litellm

# 2. Create config file
mkdir -p ~/.config/litellm
cat > ~/.config/litellm/config.yaml << 'EOF'
model_list:
  - model_name: granite-3.2-8b-instruct
    litellm_params:
      model: granite-3.2-8b-instruct
      api_base: https://ai.redhat.com/v1  # Red Hat internal endpoint
      api_key: ${REDHAT_AI_TOKEN}

  - model_name: granite-8b-code-instruct
    litellm_params:
      model: granite-8b-code-instruct
      api_base: https://ai.redhat.com/v1
      api_key: ${REDHAT_AI_TOKEN}

  - model_name: mistral-7b-instruct
    litellm_params:
      model: mistral-7b-instruct
      api_base: https://ai.redhat.com/v1
      api_key: ${REDHAT_AI_TOKEN}
EOF

# 3. Set API token (get from Red Hat IT)
export REDHAT_AI_TOKEN="your-token-here"

# 4. Start LiteLLM proxy
litellm --config ~/.config/litellm/config.yaml --port 4000

# 5. Test it works
curl http://localhost:4000/health
```

**Done!** Restart Taminator and AI features will auto-enable.

---

### Option C: Auto-Start LiteLLM (Recommended for Daily Use)

Make LiteLLM start automatically at login:

**Linux (systemd):**
```bash
# Create systemd user service
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/litellm.service << 'EOF'
[Unit]
Description=LiteLLM Proxy for Taminator AI Features
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/litellm --config %h/.config/litellm/config.yaml --port 4000
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

# Enable and start
systemctl --user enable litellm
systemctl --user start litellm
```

**macOS:**
```bash
# Create LaunchAgent
mkdir -p ~/Library/LaunchAgents
cat > ~/Library/LaunchAgents/com.redhat.litellm.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.redhat.litellm</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/litellm</string>
        <string>--config</string>
        <string>~/.config/litellm/config.yaml</string>
        <string>--port</string>
        <string>4000</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Load and start
launchctl load ~/Library/LaunchAgents/com.redhat.litellm.plist
```

---

## 🔍 Verification

### Check Taminator Status

1. **Open Taminator**
2. **Look at status bar** (bottom of window)
3. **Check AI indicator:**
   - ✅ **Green**: AI available (shows model count)
   - ⚠️ **Yellow**: AI degraded (some models unavailable)
   - ❌ **Red**: AI unavailable (click for setup guide)

### Manual Test

```bash
# Test LiteLLM is running
curl http://localhost:4000/health

# Expected output:
# {"status":"healthy"}

# Test models are available
curl http://localhost:4000/models

# Expected output:
# {"data":[{"id":"granite-3.2-8b-instruct",...}]}
```

---

## 🚫 What Works WITHOUT AI Setup?

**Core features work normally:**
- ✅ JIRA issue tracking and updates
- ✅ Customer Portal report posting
- ✅ Report generation (markdown, HTML)
- ✅ Customer onboarding
- ✅ Dashboard and statistics

**AI-enhanced features show "Setup Required":**
- 📧 Email composition (manual drafting still works)
- 📊 Report analysis (manual review still works)
- 🎯 Issue prioritization (manual sorting still works)
- 📝 Meeting notes parsing (manual entry still works)

**Bottom Line:** Taminator is fully functional without AI. AI features are productivity enhancements, not requirements.

---

## 🛠️ Troubleshooting

### "AI Status: Unavailable"

**Check LiteLLM is running:**
```bash
curl http://localhost:4000/health
```

**If error:**
```bash
# Check if process is running
ps aux | grep litellm

# Check logs
journalctl --user -u litellm -f  # Linux
tail -f /var/log/system.log | grep litellm  # macOS
```

**Restart LiteLLM:**
```bash
# Linux
systemctl --user restart litellm

# macOS
launchctl unload ~/Library/LaunchAgents/com.redhat.litellm.plist
launchctl load ~/Library/LaunchAgents/com.redhat.litellm.plist

# Manual
pkill -f litellm
litellm --config ~/.config/litellm/config.yaml --port 4000
```

### "Models Not Found"

**Verify config file:**
```bash
cat ~/.config/litellm/config.yaml
```

**Test Red Hat AI endpoint:**
```bash
curl -H "Authorization: Bearer $REDHAT_AI_TOKEN" \
     https://ai.redhat.com/v1/models
```

**If 401 Unauthorized:**
- Token expired (get new one from Red Hat IT)
- VPN not connected (connect to Red Hat VPN)

### "Connection Timeout"

**VPN Required:**
- Red Hat AI models only accessible via Red Hat VPN
- Connect VPN before starting LiteLLM
- Verify: `ping ai.redhat.com`

---

## 📚 Additional Resources

- **PAI Documentation**: `~/pai/docs/AI-INFRASTRUCTURE.md`
- **LiteLLM Docs**: https://docs.litellm.ai
- **Red Hat AI Portal**: https://ai.redhat.com (internal)
- **Support**: #taminator-support on Slack

---

## 🎓 FAQ

### Q: Can I use external models (OpenAI, Anthropic)?
**A:** No. Red Hat compliance requires all customer data processed via AIA-approved models on Red Hat infrastructure only.

### Q: Can I download models locally instead of using the proxy?
**A:** Technically yes, but not recommended. Models are 8GB+ each, require GPU for good performance, and need regular updates. The proxy is managed and optimized.

### Q: How much does LiteLLM impact system resources?
**A:** Minimal. LiteLLM is a proxy (passthrough), not running the models. Uses ~50MB RAM, negligible CPU when idle.

### Q: What if I'm offline?
**A:** AI features won't work (models require network access). Core Taminator features work offline.

### Q: Can I use models for personal tasks?
**A:** No. Models are for Red Hat customer work only. For personal AI tasks, use approved external services.

---

*Last Updated: 2025-10-28*
*Taminator v2.0 - Tesla Architecture*


