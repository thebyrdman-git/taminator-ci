# Taminator Intelligence - Deployment Strategy

**Container-first approach for Red Hat TAMs**

---

## 🎯 Recommended Deployment: Container (Linux)

### **Why Container-First?**

1. **Red Hat Culture** - TAMs are comfortable with containers
2. **Enterprise Standard** - Podman/Docker is standard tooling
3. **Self-Healing** - Automatic restart on failure
4. **Easy Updates** - Pull new image, restart container
5. **Consistent Environment** - Same runtime everywhere
6. **Resource Limits** - Prevent runaway processes
7. **Easy Backup** - Volume snapshots
8. **Systemd Integration** - Run as a service

### **TAM Skill Alignment:**
- ✅ TAMs deploy containers for customers daily
- ✅ Podman is standard on RHEL workstations
- ✅ Familiar with systemd services
- ✅ Comfortable with CLI tools
- ✅ Understand resource limits and health checks

---

## 📦 Primary Deployment: Podman + Systemd

### **Quick Start (Recommended):**

```bash
# 1. Clone repository
git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git
cd taminator

# 2. Build image
podman build -t taminator-intelligence:2.1.0 -f Containerfile .

# 3. Run as systemd service
mkdir -p ~/.config/systemd/user/
cp deployment/taminator-intelligence.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now taminator-intelligence

# 4. Check status
systemctl --user status taminator-intelligence

# 5. Access web interface
firefox http://localhost:8080
```

### **What You Get:**
- ✅ Runs as user service (no root required)
- ✅ Starts on boot
- ✅ Auto-restart on failure
- ✅ Database in `~/.local/share/taminator/intelligence.db`
- ✅ Logs via `journalctl --user -u taminator-intelligence`

---

## 🖥️ Alternative: Desktop AppImage (Optional)

### **When to Use AppImage:**
- Working on non-Linux system (Windows, macOS)
- Prefer traditional desktop GUI
- Don't want to run a service
- Occasional use only

### **Quick Start:**
```bash
# Download and run
wget https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v2.1.0/downloads/Taminator-2.1.0.AppImage
chmod +x Taminator-2.1.0.AppImage
./Taminator-2.1.0.AppImage
```

---

## 🏢 Deployment Patterns

### **Pattern 1: Individual TAM (Laptop Service)**
```yaml
Deployment: Podman container (user service)
Location: TAM laptop
Access: http://localhost:8080
Database: ~/.local/share/taminator/
Backup: Manual or automated (Restic)
Use Case: Daily case analysis
```

**Setup:**
```bash
# Install as user service
systemctl --user enable --now taminator-intelligence

# Access from laptop
curl http://localhost:8080/api/analyze -d '{"email": "..."}'
```

### **Pattern 2: Home Lab (Always-On Service)**
```yaml
Deployment: Podman container (system service)
Location: Home server (MiracleMax, etc.)
Access: https://taminator.yourdomain.com (Traefik)
Database: /mnt/storage/taminator/
Backup: Automated (Restic, daily)
Use Case: Team sharing, always available
```

**Setup:**
```bash
# Install as system service
sudo cp deployment/taminator-intelligence.service /etc/systemd/system/
sudo systemctl enable --now taminator-intelligence

# Configure Traefik reverse proxy
# Add DNS: taminator.yourdomain.com
```

### **Pattern 3: Team Deployment (Shared Server)**
```yaml
Deployment: Podman container (system service)
Location: Team server (VPN required)
Access: https://taminator.team.redhat.com
Database: Shared volume (team intelligence)
Backup: Automated with retention
Use Case: Centralized intelligence, team learning
Authentication: Required (reverse proxy)
```

**Setup:**
```bash
# Deploy on shared server
sudo systemctl enable --now taminator-intelligence

# Add authentication (nginx/Traefik)
# Configure VPN access
# Set up team onboarding
```

---

## 🔧 Systemd Service Configuration

### **User Service (Recommended for TAMs):**

```ini
# ~/.config/systemd/user/taminator-intelligence.service
[Unit]
Description=Taminator Intelligence Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
Restart=always
RestartSec=10s
StartLimitBurst=5
StartLimitIntervalSec=300

# Pull latest image on start
ExecStartPre=/usr/bin/podman pull localhost/taminator-intelligence:2.1.0

# Run container
ExecStart=/usr/bin/podman run --rm \
  --name taminator-intelligence \
  -p 127.0.0.1:8080:8080 \
  -v %h/.local/share/taminator:/app/data:Z \
  taminator-intelligence:2.1.0

# Stop container gracefully
ExecStop=/usr/bin/podman stop -t 10 taminator-intelligence

[Install]
WantedBy=default.target
```

### **System Service (For Servers):**

```ini
# /etc/systemd/system/taminator-intelligence.service
[Unit]
Description=Taminator Intelligence Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=taminator
Group=taminator
Restart=always
RestartSec=10s
StartLimitBurst=5
StartLimitIntervalSec=300

ExecStartPre=/usr/bin/podman pull localhost/taminator-intelligence:2.1.0
ExecStart=/usr/bin/podman run --rm \
  --name taminator-intelligence \
  -p 127.0.0.1:8080:8080 \
  -v /var/lib/taminator:/app/data:Z \
  taminator-intelligence:2.1.0

ExecStop=/usr/bin/podman stop -t 10 taminator-intelligence

[Install]
WantedBy=multi-user.target
```

---

## 📊 Deployment Comparison

| Feature | Container (User) | Container (System) | AppImage |
|---------|------------------|-------------------|----------|
| **Red Hat Alignment** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **TAM Skill Match** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Setup Complexity** | ⭐⭐⭐ Medium | ⭐⭐⭐⭐ Advanced | ⭐ Simple |
| **Root Required** | ❌ No | ✅ Yes | ❌ No |
| **Auto-Start** | ✅ Yes | ✅ Yes | ❌ No |
| **Self-Healing** | ✅ Yes | ✅ Yes | ❌ No |
| **Resource Limits** | ✅ Yes | ✅ Yes | ❌ No |
| **Easy Updates** | ✅ Yes | ✅ Yes | ⭐ Manual |
| **Team Sharing** | ❌ No | ✅ Yes | ❌ No |
| **Offline Work** | ✅ Yes | ✅ Yes | ✅ Yes |

---

## 🚀 Rollout Plan

### **Phase 1: Alpha (Week 1)**
- **Target:** 2-3 TAMs (volunteers)
- **Deployment:** Container (user service)
- **Goal:** Validate container deployment
- **Feedback:** Daily check-ins

### **Phase 2: Beta (Week 2-3)**
- **Target:** 10-15 TAMs
- **Deployment:** Container (user service)
- **Goal:** Identify issues, refine docs
- **Feedback:** Weekly survey

### **Phase 3: General Availability (Week 4)**
- **Target:** All TAMs
- **Deployment:** Container (default), AppImage (optional)
- **Goal:** Full team adoption
- **Support:** Slack channel, office hours

### **Phase 4: Team Deployment (Month 2)**
- **Target:** TAM teams wanting shared intelligence
- **Deployment:** Container (system service, shared server)
- **Goal:** Centralized learning
- **Support:** Dedicated setup assistance

---

## 📈 Success Metrics

### **Adoption Targets:**
- Week 1: 3 TAMs (alpha)
- Week 2: 15 TAMs (beta)
- Week 4: 50+ TAMs (GA)
- Month 3: 100+ TAMs (full adoption)

### **Quality Metrics:**
- Intelligence accuracy: >85%
- Service uptime: >99%
- Restart rate: <1 per week
- User satisfaction: >4/5

### **Usage Metrics:**
- Analyses per TAM per day: 3-5
- Time savings per case: 5-10 minutes
- Database growth: ~1MB per TAM per month

---

## 🛠️ Support Plan

### **Documentation:**
- ✅ Container deployment guide
- ✅ Systemd service setup
- ✅ Troubleshooting guide
- ✅ FAQ
- ✅ Video walkthrough (planned)

### **Support Channels:**
- **Slack:** #taminator-intelligence
- **Email:** jbyrd@redhat.com
- **Office Hours:** Fridays 2-3pm EST
- **GitLab Issues:** Bug reports and feature requests

### **Training:**
- **Self-Service:** Documentation + video
- **Live Demo:** Team call (30 minutes)
- **1-on-1:** Available for complex setups

---

## 🔄 Update Strategy

### **Container Updates:**
```bash
# Pull new image
podman pull localhost/taminator-intelligence:2.1.0

# Restart service (automatic with ExecStartPre)
systemctl --user restart taminator-intelligence

# Or manual
podman stop taminator-intelligence
podman run ...
```

### **Update Frequency:**
- **Patch releases:** Weekly (bug fixes)
- **Minor releases:** Monthly (new features)
- **Major releases:** Quarterly (breaking changes)

### **Rollback:**
```bash
# Tag previous version
podman tag taminator-intelligence:2.1.0 taminator-intelligence:2.1.0-backup

# Pull new version
podman pull taminator-intelligence:2.2.0

# If issues, rollback
podman tag taminator-intelligence:2.1.0-backup taminator-intelligence:latest
systemctl --user restart taminator-intelligence
```

---

## 🎓 TAM Onboarding Checklist

### **New TAM Setup (15 minutes):**

- [ ] Clone repository
- [ ] Build container image
- [ ] Install systemd service
- [ ] Start service
- [ ] Test with sample email
- [ ] Verify database created
- [ ] Join #taminator-intelligence Slack
- [ ] Complete feedback survey

### **Verification:**
```bash
# Service running?
systemctl --user status taminator-intelligence

# Database exists?
ls -lh ~/.local/share/taminator/intelligence.db

# API responding?
curl http://localhost:8080/health

# Analyze test email
curl -X POST http://localhost:8080/api/analyze -d '{"email": "Case 12345678..."}'
```

---

## 🔒 Security & Compliance

### **Red Hat Policy Compliance:**
- ✅ Uses Red Hat UBI9 base image
- ✅ No external API calls (offline capable)
- ✅ Customer data stays local
- ✅ Audit logs in systemd journal
- ✅ No secrets in container image

### **Security Best Practices:**
- ✅ Run as non-root user
- ✅ Bind to localhost only (default)
- ✅ Resource limits enforced
- ✅ Health checks enabled
- ✅ Automatic restart on failure

### **For Team Deployments:**
- ⚠️ Add authentication (reverse proxy)
- ⚠️ Use TLS (Let's Encrypt)
- ⚠️ Restrict network access (VPN)
- ⚠️ Enable audit logging
- ⚠️ Regular security updates

---

## 📝 Next Steps

### **Immediate (This Week):**
1. ✅ Create Containerfile
2. ✅ Create systemd service template
3. ✅ Write deployment documentation
4. ⏳ Test on RHEL 9 workstation
5. ⏳ Create demo video
6. ⏳ Recruit alpha testers

### **Short-Term (Next 2 Weeks):**
1. Alpha deployment (3 TAMs)
2. Gather feedback
3. Refine documentation
4. Beta deployment (15 TAMs)
5. Create Slack channel

### **Long-Term (Next Month):**
1. General availability release
2. Team deployment guide
3. Kubernetes deployment (optional)
4. Integration with existing TAM tools

---

**Container-first deployment aligns with Red Hat culture and TAM expertise.**

*Podman + Systemd = The Red Hat Way™*

