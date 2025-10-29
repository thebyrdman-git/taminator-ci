# Taminator Intelligence - Deployment Files

**Quick deployment templates for Red Hat TAMs**

---

## 📦 Files in This Directory

- `taminator-intelligence.service` - Systemd user service (recommended)
- `taminator-intelligence-system.service` - Systemd system service (servers)
- `install.sh` - Quick install script
- `uninstall.sh` - Uninstall script

---

## 🚀 Quick Install (Recommended)

### **Prerequisites:**
- RHEL 8/9 or Fedora
- Podman installed
- Git installed

### **Install:**
```bash
# 1. Clone repository
git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git
cd taminator

# 2. Run install script
./deployment/install.sh

# 3. Check status
systemctl --user status taminator-intelligence

# 4. Access web interface
firefox http://localhost:8080
```

### **Manual Install:**
```bash
# 1. Build image
podman build -t taminator-intelligence:2.1.0 -f Containerfile .

# 2. Install service
mkdir -p ~/.config/systemd/user/
cp deployment/taminator-intelligence.service ~/.config/systemd/user/
systemctl --user daemon-reload

# 3. Enable and start
systemctl --user enable --now taminator-intelligence

# 4. Verify
systemctl --user status taminator-intelligence
journalctl --user -u taminator-intelligence -f
```

---

## 🛠️ Common Commands

### **Service Management:**
```bash
# Start service
systemctl --user start taminator-intelligence

# Stop service
systemctl --user stop taminator-intelligence

# Restart service
systemctl --user restart taminator-intelligence

# Check status
systemctl --user status taminator-intelligence

# View logs
journalctl --user -u taminator-intelligence -f

# Enable on boot
systemctl --user enable taminator-intelligence

# Disable
systemctl --user disable taminator-intelligence
```

### **Container Management:**
```bash
# List running containers
podman ps

# View container logs
podman logs -f taminator-intelligence

# Execute command in container
podman exec -it taminator-intelligence python3 -c "from taminator.core.database import get_intelligence_database; print(get_intelligence_database().get_db_size())"

# Inspect container
podman inspect taminator-intelligence

# Stop container manually
podman stop taminator-intelligence
```

### **Database Management:**
```bash
# Check database size
ls -lh ~/.local/share/taminator/intelligence.db

# Backup database
cp ~/.local/share/taminator/intelligence.db ~/taminator-backup-$(date +%Y%m%d).db

# Restore database
cp ~/taminator-backup-20251029.db ~/.local/share/taminator/intelligence.db
systemctl --user restart taminator-intelligence

# Check database integrity
sqlite3 ~/.local/share/taminator/intelligence.db "PRAGMA integrity_check;"
```

---

## 🔄 Updates

### **Update to New Version:**
```bash
# 1. Pull latest code
cd ~/taminator
git pull

# 2. Rebuild image
podman build -t taminator-intelligence:2.1.0 -f Containerfile .

# 3. Restart service (will use new image)
systemctl --user restart taminator-intelligence
```

### **Automatic Updates:**
```bash
# Uncomment ExecStartPre in service file
# This pulls latest image on every restart
sed -i 's/# ExecStartPre=\/usr\/bin\/podman pull/ExecStartPre=\/usr\/bin\/podman pull/' ~/.config/systemd/user/taminator-intelligence.service

systemctl --user daemon-reload
systemctl --user restart taminator-intelligence
```

---

## 🗑️ Uninstall

### **Complete Removal:**
```bash
# 1. Stop and disable service
systemctl --user stop taminator-intelligence
systemctl --user disable taminator-intelligence

# 2. Remove service file
rm ~/.config/systemd/user/taminator-intelligence.service
systemctl --user daemon-reload

# 3. Remove container and image
podman rm -f taminator-intelligence
podman rmi taminator-intelligence:2.1.0

# 4. (Optional) Remove database
rm -rf ~/.local/share/taminator/
```

---

## 🔧 Troubleshooting

### **Service won't start:**
```bash
# Check service status
systemctl --user status taminator-intelligence

# Check logs
journalctl --user -u taminator-intelligence -n 50

# Check if port is in use
ss -tulpn | grep 8080

# Try manual run
podman run --rm -p 8080:8080 -v ~/.local/share/taminator:/app/data:Z taminator-intelligence:2.1.0
```

### **Database permission errors:**
```bash
# Fix permissions
chmod 755 ~/.local/share/taminator
chmod 644 ~/.local/share/taminator/intelligence.db

# Fix SELinux context
restorecon -Rv ~/.local/share/taminator
```

### **Container crashes:**
```bash
# Check container logs
podman logs taminator-intelligence

# Check resource usage
podman stats taminator-intelligence

# Try with more resources
# Edit service file, add: --memory=1g --cpus=2
```

---

## 📚 Documentation

- [Deployment Strategy](../docs/DEPLOYMENT-STRATEGY.md)
- [Container Deployment Guide](../docs/CONTAINER-DEPLOYMENT.md)
- [Deployment Options](../docs/DEPLOYMENT-OPTIONS.md)

---

**Questions? Slack: #taminator-intelligence**

