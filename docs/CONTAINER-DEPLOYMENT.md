# Taminator Intelligence - Container Deployment

**Deploy Taminator Intelligence as a containerized service**

---

## 🐳 Deployment Options

### **Option A: Desktop AppImage** (Recommended for most TAMs)
- Download and run Taminator AppImage
- Intelligence runs embedded in the app
- No setup required
- Works offline
- Database: `~/.taminator/intelligence.db`

### **Option B: Container Service** (For advanced users)
- Run Taminator Intelligence as a service
- Access via web interface or API
- Can be shared across team (optional)
- Requires Docker/Podman
- Database: Container volume

---

## 📦 Container Deployment

### **Prerequisites:**
- Docker or Podman installed
- Basic container knowledge

### **Quick Start (Docker Compose):**

```bash
# Clone repository
git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git
cd taminator

# Start service
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

### **Quick Start (Podman):**

```bash
# Build image
podman build -t taminator-intelligence:2.1.0 -f Containerfile .

# Run container
podman run -d \
  --name taminator-intelligence \
  --restart unless-stopped \
  -p 8080:8080 \
  -v taminator-data:/app/data:Z \
  taminator-intelligence:2.1.0

# Check status
podman ps

# View logs
podman logs -f taminator-intelligence

# Stop container
podman stop taminator-intelligence
```

---

## 🔧 Configuration

### **Environment Variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `TAMINATOR_DB_PATH` | `/app/data/intelligence.db` | SQLite database path |
| `PYTHONUNBUFFERED` | `1` | Python output buffering |

### **Ports:**

| Port | Protocol | Description |
|------|----------|-------------|
| 8080 | HTTP | Web interface / API |

### **Volumes:**

| Volume | Path | Description |
|--------|------|-------------|
| `taminator-data` | `/app/data` | Intelligence database |

---

## 🌐 Accessing the Service

### **Web Interface:**
```
http://localhost:8080
```

### **API Endpoints:**

**Analyze Email:**
```bash
curl -X POST http://localhost:8080/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "email": "From: customer@example.com\nSubject: Case 12345678\n\nNeed help...",
    "tags": ["all"]
  }'
```

**Get Case History:**
```bash
curl http://localhost:8080/api/history?limit=50
```

**Record Feedback:**
```bash
curl -X POST http://localhost:8080/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "case_number": "04293185",
    "decision": "followed_recommendation",
    "ai_followed": true,
    "notes": "Worked perfectly"
  }'
```

**Get Statistics:**
```bash
curl http://localhost:8080/api/statistics?days=7
```

---

## 🔒 Security Considerations

### **Local Deployment (Single TAM):**
- Bind to localhost only: `-p 127.0.0.1:8080:8080`
- No authentication needed (local access only)
- Database stored in container volume

### **Shared Deployment (Team):**
- **⚠️ Add authentication** (not included by default)
- Use reverse proxy (Traefik, nginx) with TLS
- Restrict network access (firewall, VPN)
- Regular backups of database volume

### **Red Hat Compliance:**
- Container uses Red Hat UBI9 base image
- No external API calls (runs offline)
- Customer data stays in your infrastructure
- Audit logs in container logs

---

## 📊 Monitoring & Health Checks

### **Health Check:**
```bash
# Docker
docker inspect --format='{{.State.Health.Status}}' taminator-intelligence

# Podman
podman healthcheck run taminator-intelligence
```

### **Resource Usage:**
```bash
# Docker
docker stats taminator-intelligence

# Podman
podman stats taminator-intelligence
```

### **Logs:**
```bash
# Docker
docker logs -f --tail 100 taminator-intelligence

# Podman
podman logs -f --tail 100 taminator-intelligence
```

---

## 🔄 Backup & Restore

### **Backup Database:**

**Docker:**
```bash
# Backup to local file
docker cp taminator-intelligence:/app/data/intelligence.db ./backup-$(date +%Y%m%d).db

# Or backup volume
docker run --rm \
  -v taminator_taminator-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/taminator-backup-$(date +%Y%m%d).tar.gz -C /data .
```

**Podman:**
```bash
# Backup to local file
podman cp taminator-intelligence:/app/data/intelligence.db ./backup-$(date +%Y%m%d).db

# Or backup volume
podman run --rm \
  -v taminator-data:/data:Z \
  -v $(pwd):/backup:Z \
  alpine tar czf /backup/taminator-backup-$(date +%Y%m%d).tar.gz -C /data .
```

### **Restore Database:**

**Docker:**
```bash
# Stop container
docker stop taminator-intelligence

# Restore from backup
docker cp ./backup-20251029.db taminator-intelligence:/app/data/intelligence.db

# Start container
docker start taminator-intelligence
```

**Podman:**
```bash
# Stop container
podman stop taminator-intelligence

# Restore from backup
podman cp ./backup-20251029.db taminator-intelligence:/app/data/intelligence.db

# Start container
podman start taminator-intelligence
```

---

## 🚀 Production Deployment (MiracleMax Example)

### **Systemd Service (Podman):**

```ini
# /etc/systemd/system/taminator-intelligence.service
[Unit]
Description=Taminator Intelligence Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=jbyrd
Restart=always
RestartSec=10s
StartLimitBurst=5
StartLimitIntervalSec=300

ExecStartPre=/usr/bin/podman pull localhost/taminator-intelligence:2.1.0
ExecStart=/usr/bin/podman run --rm \
  --name taminator-intelligence \
  -p 127.0.0.1:8080:8080 \
  -v taminator-data:/app/data:Z \
  taminator-intelligence:2.1.0

ExecStop=/usr/bin/podman stop -t 10 taminator-intelligence

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now taminator-intelligence
sudo systemctl status taminator-intelligence
```

### **Traefik Integration:**

```yaml
# Traefik dynamic config
http:
  routers:
    taminator:
      rule: "Host(`taminator.yourdomain.com`)"
      service: taminator
      entryPoints:
        - websecure
      tls:
        certResolver: letsencrypt
  
  services:
    taminator:
      loadBalancer:
        servers:
          - url: "http://localhost:8080"
        healthCheck:
          path: /health
          interval: 30s
          timeout: 10s
```

---

## 🛠️ Troubleshooting

### **Container won't start:**
```bash
# Check logs
docker logs taminator-intelligence

# Check if port is already in use
sudo netstat -tulpn | grep 8080

# Try different port
docker run -p 8081:8080 ...
```

### **Database permission errors:**
```bash
# Fix SELinux context (Podman)
podman run -v taminator-data:/app/data:Z ...

# Or disable SELinux for volume (not recommended)
sudo chcon -Rt svirt_sandbox_file_t /path/to/volume
```

### **Health check failing:**
```bash
# Check database
docker exec taminator-intelligence python3 -c "from taminator.core.database import get_intelligence_database; db = get_intelligence_database(); print(db.get_db_size())"

# Check Python path
docker exec taminator-intelligence python3 -c "import sys; print(sys.path)"
```

---

## 📈 Performance Tuning

### **Resource Limits:**

**Light usage (1-5 TAMs):**
```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 256M
```

**Medium usage (5-20 TAMs):**
```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
```

**Heavy usage (20+ TAMs):**
```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 1G
```

---

## 🎯 When to Use Container vs AppImage

### **Use AppImage if:**
- ✅ You work on a laptop (offline often)
- ✅ You want simplest setup (download & run)
- ✅ You don't need to share with team
- ✅ You prefer desktop GUI

### **Use Container if:**
- ✅ You have a home server (like MiracleMax)
- ✅ You want to share with team
- ✅ You prefer web interface
- ✅ You want centralized database
- ✅ You're comfortable with containers

### **Use Both if:**
- ✅ AppImage on laptop for field work
- ✅ Container on server for team sharing
- ✅ Sync databases periodically

---

## 🔗 Related Documentation

- [Embedded Intelligence Guide](EMBEDDED-INTELLIGENCE-COMPLETE.md)
- [GUI Integration Spec](GUI-INTEGRATION-SPEC.md)
- [Daily Usage Guide](DAILY-USAGE-GUIDE.md)
- [Phase 3 Complete](PHASE-3-COMPLETE.md)

---

**Container deployment gives TAMs flexibility without sacrificing simplicity.**

*Run it your way: Desktop app, container, or both!*

