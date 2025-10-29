# Taminator Intelligence - Deployment Options

**Choose the deployment that fits your workflow**

---

## 🎯 Quick Decision Guide

### **I want the simplest option → AppImage**
- Download one file
- Double-click to run
- No setup required
- Works offline

### **I have a home server → Container**
- Run as a service
- Access from any device
- Share with team (optional)
- Centralized database

### **I want both → Hybrid**
- AppImage on laptop (field work)
- Container on server (team sharing)
- Best of both worlds

---

## 📦 Option 1: Desktop AppImage (Recommended)

### **What You Get:**
- Self-contained desktop application
- Embedded intelligence engine
- Local SQLite database (`~/.taminator/intelligence.db`)
- Works completely offline
- No dependencies

### **Installation:**
```bash
# Download from GitLab release
wget https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v2.1.0/downloads/Taminator-2.1.0.AppImage

# Make executable
chmod +x Taminator-2.1.0.AppImage

# Run
./Taminator-2.1.0.AppImage
```

### **Pros:**
- ✅ Simplest setup (download & run)
- ✅ Works offline
- ✅ No server required
- ✅ Desktop GUI
- ✅ Portable (run from USB drive)

### **Cons:**
- ❌ One user per database
- ❌ No team sharing (without manual sync)
- ❌ Linux only (for now)

### **Best For:**
- Individual TAMs
- Laptop/desktop users
- Offline work
- Field engineers
- Quick testing

---

## 🐳 Option 2: Container Service

### **What You Get:**
- Containerized web service
- HTTP API + web interface
- Persistent database (container volume)
- Can run on home server
- Optional team sharing

### **Installation:**

**Quick Start (Docker Compose):**
```bash
cd /path/to/taminator
docker-compose up -d
```

**Or Podman:**
```bash
podman build -t taminator-intelligence:2.1.0 -f Containerfile .
podman run -d --name taminator-intelligence -p 8080:8080 -v taminator-data:/app/data:Z taminator-intelligence:2.1.0
```

### **Pros:**
- ✅ Run as a service (always available)
- ✅ Access from any device
- ✅ Can share with team
- ✅ Centralized database
- ✅ Easy backup/restore
- ✅ Systemd integration

### **Cons:**
- ❌ Requires Docker/Podman
- ❌ Requires server (or always-on machine)
- ❌ More complex setup
- ❌ Needs network access

### **Best For:**
- Home lab users (MiracleMax, etc.)
- Team deployments
- Always-on service
- Web interface preference
- Centralized intelligence

---

## 🔄 Option 3: Hybrid Deployment

### **Best of Both Worlds:**

**Scenario: TAM with Home Server**

1. **Container on MiracleMax:**
   - Runs 24/7 at home
   - Centralized database
   - Team access (optional)
   - Backup automated

2. **AppImage on Laptop:**
   - Use in field
   - Works offline
   - Sync to server when home
   - Local intelligence cache

### **Sync Strategy:**

**Manual Sync:**
```bash
# Export from laptop
sqlite3 ~/.taminator/intelligence.db ".backup /tmp/laptop-backup.db"

# Import to server
podman cp /tmp/laptop-backup.db taminator-intelligence:/app/data/intelligence.db
podman restart taminator-intelligence
```

**Automated Sync (Future):**
```bash
# Planned feature: tam-intelligence sync
tam-intelligence sync --from ~/.taminator/intelligence.db --to http://miraclemax.local:8080
```

### **Pros:**
- ✅ Offline capability
- ✅ Team sharing
- ✅ Centralized + portable
- ✅ Redundancy

### **Cons:**
- ❌ Most complex setup
- ❌ Manual sync required (for now)
- ❌ Two databases to manage

---

## 📊 Feature Comparison

| Feature | AppImage | Container | Hybrid |
|---------|----------|-----------|--------|
| **Setup Complexity** | ⭐ Simple | ⭐⭐⭐ Advanced | ⭐⭐⭐⭐ Complex |
| **Offline Work** | ✅ Yes | ❌ No | ✅ Yes |
| **Team Sharing** | ❌ No | ✅ Yes | ✅ Yes |
| **Always Available** | ❌ No | ✅ Yes | ✅ Yes |
| **Desktop GUI** | ✅ Yes | ❌ No (Web) | ✅ Yes |
| **Web Interface** | ❌ No | ✅ Yes | ✅ Yes |
| **Resource Usage** | Low | Low-Med | Medium |
| **Backup** | Manual | Automated | Both |
| **Portability** | ✅ High | ❌ Low | ⭐ Best |

---

## 🎓 Deployment Examples

### **Example 1: Solo TAM (Laptop Only)**
```
Deployment: AppImage
Location: Laptop
Database: ~/.taminator/intelligence.db
Backup: Manual (copy file)
Access: Desktop GUI
```

### **Example 2: Home Lab TAM (MiracleMax)**
```
Deployment: Container (Podman + Systemd)
Location: MiracleMax server
Database: Container volume
Backup: Automated (Restic)
Access: Web interface (https://taminator.yourdomain.com)
```

### **Example 3: Team Lead (Hybrid)**
```
Deployment: Container (server) + AppImage (laptop)
Location: Both
Database: Synced (server primary)
Backup: Server automated, laptop manual
Access: Both GUI and web
```

### **Example 4: TAM Team (Shared Container)**
```
Deployment: Container (shared server)
Location: Team server
Database: Shared (multi-user)
Backup: Automated with retention
Access: Web interface (VPN required)
Authentication: Add reverse proxy with auth
```

---

## 🔒 Security Considerations

### **AppImage (Local Only):**
- ✅ Database on local filesystem
- ✅ No network exposure
- ✅ User-level permissions
- ⚠️ No encryption at rest (filesystem-level only)

### **Container (Local Service):**
- ✅ Bind to localhost (127.0.0.1:8080)
- ✅ No external access
- ✅ Container isolation
- ⚠️ No authentication (localhost only)

### **Container (Team Sharing):**
- ⚠️ **Add authentication** (reverse proxy)
- ⚠️ **Use TLS** (Let's Encrypt)
- ⚠️ **Restrict access** (VPN, firewall)
- ⚠️ **Audit logs** (who accessed what)
- ⚠️ **Regular backups** (data loss prevention)

---

## 🚀 Migration Paths

### **AppImage → Container:**
```bash
# 1. Backup AppImage database
cp ~/.taminator/intelligence.db /tmp/backup.db

# 2. Deploy container
docker-compose up -d

# 3. Import database
docker cp /tmp/backup.db taminator-intelligence:/app/data/intelligence.db
docker restart taminator-intelligence
```

### **Container → AppImage:**
```bash
# 1. Export from container
docker cp taminator-intelligence:/app/data/intelligence.db /tmp/export.db

# 2. Copy to laptop
cp /tmp/export.db ~/.taminator/intelligence.db

# 3. Run AppImage
./Taminator-2.1.0.AppImage
```

### **Single → Team:**
```bash
# 1. Deploy container on shared server
# 2. Import all TAM databases
# 3. Set up authentication
# 4. Configure VPN access
# 5. Train team on web interface
```

---

## 📈 Scaling Recommendations

### **1-5 TAMs:**
- AppImage (individual)
- Or single container (shared)
- Resource: 0.5 CPU, 256MB RAM

### **5-20 TAMs:**
- Container (shared server)
- Add reverse proxy
- Resource: 1 CPU, 512MB RAM

### **20+ TAMs:**
- Container (dedicated server)
- Load balancer (optional)
- Resource: 2 CPU, 1GB RAM

### **100+ TAMs (Enterprise):**
- Kubernetes deployment
- Multiple replicas
- Shared database (PostgreSQL)
- Redis caching
- *(Future roadmap)*

---

## 🛠️ Troubleshooting

### **AppImage won't start:**
```bash
# Check if FUSE is available
which fusermount

# Try extract and run
./Taminator-2.1.0.AppImage --appimage-extract
./squashfs-root/AppRun
```

### **Container won't start:**
```bash
# Check logs
docker logs taminator-intelligence

# Check port conflict
sudo netstat -tulpn | grep 8080

# Try different port
docker run -p 8081:8080 ...
```

### **Database corruption:**
```bash
# AppImage
sqlite3 ~/.taminator/intelligence.db "PRAGMA integrity_check;"

# Container
docker exec taminator-intelligence sqlite3 /app/data/intelligence.db "PRAGMA integrity_check;"
```

---

## 📚 Documentation Links

- [Container Deployment Guide](CONTAINER-DEPLOYMENT.md)
- [Embedded Intelligence Guide](EMBEDDED-INTELLIGENCE-COMPLETE.md)
- [GUI Integration Spec](GUI-INTEGRATION-SPEC.md)
- [Daily Usage Guide](DAILY-USAGE-GUIDE.md)

---

**Choose what works for you. All options provide the same 89% accuracy intelligence!**

*AppImage for simplicity. Container for flexibility. Hybrid for both.*

