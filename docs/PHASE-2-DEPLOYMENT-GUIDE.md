# Taminator Intelligence - Phase 2 Deployment Guide

**Status:** Ready for Deployment ✅  
**Date:** October 29, 2025  
**Target:** MiracleMax (192.168.1.34)

---

## 🎯 What Phase 2 Delivers

### **Self-Hosted Intelligence Infrastructure**

**Breaking Free from Cursor Limitations:**
- ✅ **Persistent Storage** → PostgreSQL database (not lost after 1M tokens)
- ✅ **Auto-Analysis** → Email monitor service (not just interactive)
- ✅ **Self-Healing** → Automatic restart on failure
- ✅ **Background Processing** → Systemd services (24/7 operation)
- ✅ **Metrics Collection** → Track accuracy over time
- ✅ **Automated Backups** → Daily encrypted backups

---

## 📦 What Gets Deployed

### **Infrastructure Stack:**
```
MiracleMax (192.168.1.34)
├── PostgreSQL 16 (taminator-postgres container)
│   ├── Database: taminator_intelligence
│   ├── Tables: 8 (case_intelligence, contacts, accuracy, etc.)
│   ├── Views: 4 (daily_accuracy, customer_summary, etc.)
│   └── Data: /mnt/storage/taminator/postgres
│
├── Redis 7 (taminator-redis container)
│   ├── Cache for fast lookups
│   ├── Session storage
│   └── Data: /mnt/storage/taminator/redis
│
├── Intelligence API (taminator-api.service)
│   ├── FastAPI + Uvicorn
│   ├── Port: 8100
│   ├── Workers: 4
│   └── Auto-restart: Enabled
│
├── Email Monitor (taminator-email-monitor.service)
│   ├── Watch: ~/taminator-emails/new/
│   ├── Process: Auto-analyze emails
│   ├── Move: ~/taminator-emails/processed/
│   └── Auto-restart: Enabled
│
├── Metrics Collection (cron job)
│   ├── Schedule: Every 5 minutes
│   ├── Storage: PostgreSQL
│   └── Dashboard: Phase 3
│
└── Automated Backups (daily cron)
    ├── Schedule: 2 AM daily
    ├── Location: /mnt/backup/taminator/
    ├── Retention: 30 days
    └── Includes: PostgreSQL + Redis
```

---

## 🚀 Deployment Steps

### **Prerequisites:**
```bash
# 1. Ensure Taminator source is present
ls -la /home/jbyrd/TAMINATOR

# 2. Ensure Ansible is installed
ansible --version

# 3. Ensure containers.podman collection is installed
ansible-galaxy collection install containers.podman
```

### **Step 1: Review Configuration**
```bash
cd ~/miraclemax-ansible

# Review default variables
cat roles/taminator_intelligence/defaults/main.yml

# Review inventory
cat inventory/miraclemax.yml
```

### **Step 2: Dry Run (Check Mode)**
```bash
# Test deployment without making changes
ansible-playbook playbooks/deploy-taminator-intelligence.yml --check --diff
```

### **Step 3: Deploy**
```bash
# Full deployment
ansible-playbook playbooks/deploy-taminator-intelligence.yml

# You'll be prompted to confirm:
# "Deploy Taminator Intelligence to miraclemax.local? (yes/no)"
# Type: yes
```

### **Step 4: Verify Deployment**
```bash
# Check services
systemctl status taminator-api
systemctl status taminator-email-monitor

# Check containers
podman ps | grep taminator

# Check API health
curl http://localhost:8100/intelligence/status

# Check logs
journalctl -u taminator-api -f
journalctl -u taminator-email-monitor -f
```

---

## 🧪 Testing the Deployment

### **Test 1: Manual Analysis (CLI)**
```bash
cd /home/jbyrd/TAMINATOR

# Analyze test email
python3 -m taminator.commands.analyze -f tests/test_jpmc_email.txt

# Expected output:
# ✅ Case Number: 04293185 (confidence: 0.95)
# ✅ Customer: JP Morgan Chase (confidence: 0.92)
# ✅ Issue Type: LICENSING (confidence: 0.89)
# ✅ Overall Confidence: HIGH (0.89)
```

### **Test 2: Auto-Analysis (Email Monitor)**
```bash
# Create test email
cat > ~/taminator-emails/new/test_$(date +%s).txt << 'EOF'
From: test@jpmchase.com
Subject: Case 12345678 - Subscription Renewal

Hi Jimmy,

We need help with our Ansible Automation Platform subscription renewal.
It expires on December 31, 2025 and we cannot afford any outages.

Thanks,
Test User
EOF

# Wait 5 seconds for auto-processing
sleep 5

# Check processed directory
ls -la ~/taminator-emails/processed/

# Check email monitor logs
journalctl -u taminator-email-monitor --since "1 minute ago"
```

### **Test 3: Database Connectivity**
```bash
# Connect to database
podman exec -it taminator-postgres psql -U taminator -d taminator_intelligence

# Run queries
SELECT COUNT(*) FROM case_intelligence;
SELECT * FROM daily_accuracy;
SELECT * FROM customer_summary;

# Exit
\q
```

### **Test 4: API Endpoint**
```bash
# Test status endpoint
curl http://localhost:8100/intelligence/status | jq

# Test analysis endpoint (requires API running)
curl -X POST http://localhost:8100/intelligence/analyze-email \
  -H "Content-Type: application/json" \
  -d '{
    "email_text": "Case 12345678 from test@example.com",
    "tags": ["all"]
  }' | jq
```

---

## 📊 Monitoring & Maintenance

### **Check Service Status:**
```bash
# All Taminator services
systemctl status taminator-*

# Individual services
systemctl status taminator-api
systemctl status taminator-email-monitor

# Container status
podman ps -a | grep taminator
```

### **View Logs:**
```bash
# API logs
journalctl -u taminator-api -f

# Email monitor logs
journalctl -u taminator-email-monitor -f

# PostgreSQL logs
podman logs -f taminator-postgres

# Redis logs
podman logs -f taminator-redis
```

### **Restart Services:**
```bash
# Restart API
sudo systemctl restart taminator-api

# Restart email monitor
sudo systemctl restart taminator-email-monitor

# Restart containers
podman restart taminator-postgres
podman restart taminator-redis
```

### **Check Backups:**
```bash
# List backups
ls -lh /mnt/backup/taminator/

# Test backup integrity
gunzip -t /mnt/backup/taminator/taminator-YYYYMMDD-HHMMSS.sql.gz

# Restore from backup (if needed)
gunzip < /mnt/backup/taminator/taminator-YYYYMMDD-HHMMSS.sql.gz | \
  podman exec -i taminator-postgres psql -U taminator -d taminator_intelligence
```

---

## 🔧 Configuration

### **Environment Variables:**
```bash
# Set database password (before deployment)
export TAMINATOR_DB_PASSWORD="your_secure_password_here"

# Or use Ansible Vault
ansible-vault create group_vars/miraclemax/vault.yml
# Add: taminator_db_password: "your_secure_password"
```

### **Customize Settings:**
Edit `~/miraclemax-ansible/roles/taminator_intelligence/defaults/main.yml`:
```yaml
# API configuration
taminator_api_port: 8100  # Change if port conflict
taminator_api_workers: 4  # Adjust based on load

# Email monitor
taminator_monitor_interval: 5  # Seconds between checks

# Backup
taminator_backup_retention_days: 30  # Days to keep backups
```

---

## 🐛 Troubleshooting

### **Problem: API won't start**
```bash
# Check logs
journalctl -u taminator-api -n 50

# Check if port is in use
sudo lsof -i :8100

# Verify database connectivity
podman exec taminator-postgres pg_isready -U taminator
```

### **Problem: Email monitor not processing**
```bash
# Check service status
systemctl status taminator-email-monitor

# Check logs
journalctl -u taminator-email-monitor -f

# Verify directory permissions
ls -la ~/taminator-emails/new/
ls -la ~/taminator-emails/processed/

# Test manually
cd /home/jbyrd/TAMINATOR
python3 src/taminator/services/email_monitor.py
```

### **Problem: Database connection failed**
```bash
# Check container status
podman ps -a | grep taminator-postgres

# Check logs
podman logs taminator-postgres

# Restart container
podman restart taminator-postgres

# Verify port
sudo lsof -i :5432
```

### **Problem: Self-healing not working**
```bash
# Check systemd configuration
systemctl cat taminator-api

# Verify restart policy
systemctl show taminator-api | grep Restart

# Test self-healing
sudo systemctl kill -s KILL taminator-api
sleep 15
systemctl status taminator-api  # Should show "active (running)"
```

---

## 📈 Success Metrics

### **Deployment Success:**
- ✅ All services running (`systemctl status taminator-*`)
- ✅ All containers healthy (`podman ps`)
- ✅ API responding (`curl http://localhost:8100/intelligence/status`)
- ✅ Email monitor processing (`ls ~/taminator-emails/processed/`)
- ✅ Database accessible (`podman exec taminator-postgres pg_isready`)

### **Operational Success:**
- ✅ Auto-analysis working (emails processed within 5 seconds)
- ✅ Self-healing working (services auto-restart after kill)
- ✅ Backups running (daily backups in `/mnt/backup/taminator/`)
- ✅ Metrics collecting (cron job running every 5 minutes)

---

## 🎉 Next Steps After Deployment

### **For You (Daily Usage):**
1. **Start using auto-analysis:**
   ```bash
   vim ~/taminator-emails/new/case_email.txt
   # Paste email, save, wait 5 seconds
   # Check: ls ~/taminator-emails/processed/
   ```

2. **Track accuracy:**
   ```bash
   # Query database for accuracy metrics
   podman exec -it taminator-postgres psql -U taminator -d taminator_intelligence \
     -c "SELECT * FROM daily_accuracy ORDER BY date DESC LIMIT 7;"
   ```

3. **Provide feedback:**
   ```bash
   # Create feedback files
   vim ~/taminator-feedback/case_XXXXXX_feedback.txt
   ```

### **For Development (Phase 3):**
1. **Learning System** - Implement feedback loop
2. **Team Intelligence** - Multi-user support
3. **Metrics Dashboard** - Grafana integration
4. **Red Hat Integration** - SupportShell, Jira, Confluence

---

## 📚 Additional Resources

- **Intelligence Engine Code:** `/home/jbyrd/TAMINATOR/src/taminator/core/intelligence_engine.py`
- **API Routes:** `/home/jbyrd/TAMINATOR/src/taminator/api/routes/intelligence.py`
- **Database Schema:** `~/miraclemax-ansible/roles/taminator_intelligence/templates/schema.sql.j2`
- **Email Monitor:** `~/miraclemax-ansible/roles/taminator_intelligence/templates/email_monitor.py.j2`

---

**Ready to deploy!** 🚀

**Command:**
```bash
cd ~/miraclemax-ansible
ansible-playbook playbooks/deploy-taminator-intelligence.yml
```

**Estimated Time:** 10-15 minutes  
**Complexity:** Medium (Ansible handles everything)  
**Risk:** Low (can rollback if needed)

