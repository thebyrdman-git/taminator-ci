# Installation

## Prerequisites

!!! warning "Internal Red Hat Access Required"
    Taminator is an **internal Red Hat TAM tool**. Access requires:
    
    - ✅ Red Hat employee
    - ✅ Red Hat VPN connection
    - ✅ GitLab CEE access (`gitlab.cee.redhat.com`)
    - ✅ TAM team membership (recommended)

### System Requirements

**Minimum:**
- **OS**: RHEL 9+, Fedora 38+, Ubuntu 22.04+ (Linux) / macOS 11+ / Windows 10+
- **RAM**: 2 GB
- **Disk**: 500 MB free
- **Network**: Red Hat VPN for downloads and JIRA/Portal access

**Recommended:**
- **OS**: RHEL 9 or Fedora (latest)
- **RAM**: 4 GB
- **Disk**: 1 GB free
- **Container Runtime**: Podman 4.0+ (for container deployment)

---

## Download Options

All downloads are available through **GitLab CEE** (requires Red Hat VPN):

**📦 [GitLab CEE Releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases)**

### Available Builds

| Platform | Build Type | Size | Best For |
|----------|------------|------|----------|
| Linux x86_64 | AppImage | ~180 MB | Desktop users |
| Linux x86_64 | DEB | ~145 MB | Debian/Ubuntu |
| Linux ARM64 | AppImage | ~175 MB | ARM workstations |
| macOS (Intel) | DMG | ~120 MB | Intel Macs |
| macOS (Apple Silicon) | DMG | ~115 MB | M1/M2/M3 Macs |
| Windows x64 | EXE | ~130 MB | Windows users |
| Container | Source + Containerfile | - | Servers, power users |

---

## Installation Methods

### Option 1: Container + Systemd (Recommended for Linux)

**Best for:** Linux servers, power users, always-on services

#### Step 1: Clone Repository

```bash
# Connect to Red Hat VPN first
# Then clone from GitLab CEE
git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git
cd taminator
```

#### Step 2: Run One-Line Installer

```bash
# Installs container and systemd service
./deployment/install.sh

# Follow prompts:
# - Choose user service (default) or system service
# - Container will be built automatically
# - Service will be enabled and started
```

#### Step 3: Verify Installation

```bash
# Check service status
systemctl --user status taminator-intelligence

# Check health
curl http://localhost:8080/health

# Access web interface
firefox http://localhost:8080
```

**What gets installed:**
- Container image: `taminator-intelligence:2.1.2`
- Systemd service: `~/.config/systemd/user/taminator-intelligence.service`
- Database: `~/.local/share/taminator/intelligence.db`
- Logs: `journalctl --user -u taminator-intelligence`

---

### Option 2: AppImage (Linux Desktop)

**Best for:** Linux desktop users, occasional use, no container setup

!!! warning "v2.1.2 Preview Release"
    Current version is a **preview release**. Backend service not bundled in AppImage.
    Wait for v2.1.3 for full functionality, or use container deployment instead.

#### Step 1: Download

1. **Connect to Red Hat VPN** (required)
2. Go to **[GitLab CEE Releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases)**
3. Download latest AppImage:
   - `Taminator-2.1.2.AppImage` (x86_64)

#### Step 2: Make Executable and Run

```bash
# Make executable
chmod +x Taminator-2.1.2.AppImage

# Run
./Taminator-2.1.2.AppImage

# Optional: Move to Applications
mkdir -p ~/Applications
mv Taminator-2.1.2.AppImage ~/Applications/
```

#### Step 3: (Optional) Desktop Integration

```bash
# Create desktop entry
cat > ~/.local/share/applications/taminator.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=TAMINATOR
Comment=AI-Augmented TAM Assistant
Exec=/home/YOUR_USERNAME/Applications/Taminator-2.1.2.AppImage
Icon=taminator
Terminal=false
Categories=Development;Utility;
EOF

# Update desktop database
update-desktop-database ~/.local/share/applications/
```

---

### Option 3: macOS (DMG)

**Best for:** Mac users

!!! warning "v2.1.2 Preview Release"
    Current version is a **preview release**. Backend service not bundled.
    Wait for v2.1.3 for full functionality.

#### Step 1: Download

1. **Connect to Red Hat VPN** (required)
2. Go to **[GitLab CEE Releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases)**
3. Download DMG:
   - `Taminator-2.1.2.dmg` (Universal)

#### Step 2: Install

```bash
# Open DMG
open Taminator-2.1.2.dmg

# Drag Taminator to Applications folder
```

#### Step 3: First Launch

```bash
# macOS Gatekeeper will block first launch
# Right-click Taminator in Applications
# Select "Open"
# Click "Open" in security dialog
```

---

### Option 4: Windows (EXE Installer)

**Best for:** Windows users

!!! warning "Windows Not Available"
    **Windows builds are not available for v2.1.2.**
    
    - ✅ Linux: Available
    - ✅ macOS: Available
    - ⏳ Windows: Coming in v2.1.3
    
    Check [GitLab CEE Releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases) for updates.

#### Step 1: Download

1. **Connect to Red Hat VPN** (required)
2. Go to **[GitLab CEE Releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases)**
3. Download: `Taminator Setup 2.1.2.exe` (when available)

#### Step 2: Install

1. Run `Taminator Setup 2.1.2.exe`
2. Follow installation wizard
3. Choose installation directory
4. Create desktop shortcut (optional)
5. Click "Install"

#### Step 3: Launch

- From Start Menu: "TAMINATOR"
- From Desktop: Double-click Taminator icon

---

## Post-Installation

### First Launch: OOBE Wizard

Taminator includes an Out-of-Box Experience wizard on first launch:

1. **Welcome Screen** - Overview of features
2. **Token Setup** - Configure JIRA API token (required)
3. **Portal Token** - Configure Customer Portal token (optional)
4. **Customer Onboarding** - Add your first customer (optional)
5. **Complete** - Start using Taminator!

### Configure Tokens

#### JIRA API Token (Required)

1. Go to: [Red Hat API Management](https://access.redhat.com/management/api)
2. Generate new API token
3. Copy token
4. In Taminator: **Settings → Authentication → Add JIRA Token**
5. Paste token and save

#### Customer Portal Token (Optional)

1. Same process as JIRA token
2. In Taminator: **Settings → Authentication → Add Portal Token**

### Verify Installation

```bash
# Health check (container/AppImage with service)
curl http://localhost:8765/health

# Check database
ls -lh ~/.local/share/taminator/intelligence.db

# View logs (container deployment)
journalctl --user -u taminator-intelligence -n 50

# Test intelligence engine
# Open Taminator GUI → Intelligence Analyzer
# Paste test email → Click "Analyze"
```

---

## Troubleshooting

### "Cannot connect to Red Hat VPN"

**Solution:**
- Verify VPN connection: `ping gitlab.cee.redhat.com`
- Reconnect VPN and try again
- Contact IT if issues persist

### "403 Forbidden" from GitLab CEE

**Solution:**
- Verify you're logged in to GitLab CEE
- Check you have access to `jbyrd/taminator` repository
- Contact repository owner for access

### Container Build Fails

**Solution:**
```bash
# Check Podman version
podman --version  # Should be 4.0+

# Try rebuilding
cd ~/taminator
podman build -t taminator-intelligence:2.1.2 -f Containerfile .

# Check logs for specific errors
```

### AppImage Won't Run

**Solution:**
```bash
# Install FUSE (if needed)
sudo dnf install fuse fuse-libs  # RHEL/Fedora
sudo apt install fuse libfuse2   # Ubuntu

# Check permissions
chmod +x Taminator-2.1.2.AppImage

# Run with --appimage-extract-and-run (workaround)
./Taminator-2.1.2.AppImage --appimage-extract-and-run
```

### macOS "Unidentified Developer"

**Solution:**
- Right-click Taminator in Applications
- Select "Open"
- Click "Open" in security dialog
- This only needed once

### Windows SmartScreen Warning

**Solution:**
- Click "More info"
- Click "Run anyway"
- This is expected for internal tools

---

## Next Steps

- ✅ [First Launch Guide](first-launch.md) - Complete OOBE wizard
- ✅ [Your First Analysis](first-analysis.md) - Analyze your first email
- ✅ [User Guide](../user-guide/index.md) - Learn all features
- ✅ [Configuration](../administration/configuration.md) - Customize settings

---

## Update Process

### Container Deployment

```bash
cd ~/taminator
git pull
./deployment/install.sh  # Rebuilds and restarts
```

### AppImage/Native Builds

1. Download new version from [GitLab CEE Releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases)
2. Replace old file
3. Launch new version

Database and settings automatically migrate to new versions.

---

## Support

- **GitLab Issues**: [Report a Bug](https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues)
- **Email**: jbyrd@redhat.com
- **Slack**: #taminator-intelligence (Red Hat internal)
- **Documentation**: [taminator.dev](https://taminator.dev)

---

**Welcome to the TAMINATOR community!** 🎉

