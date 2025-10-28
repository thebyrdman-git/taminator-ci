# Building Taminator on Rocky Linux 9

**Purpose**: Build AppImage on oldest supported platform (Rocky 9) for maximum compatibility  
**Time**: 45 minutes first time, 10 minutes after setup  
**Result**: AppImage that works on Rocky 9+, RHEL 9+, Fedora 38+

---

## 🎯 Why Build on Rocky?

**Rule**: Always build on the **oldest** platform you want to support.

- Build on Rocky 9 → Works on Rocky 9+, RHEL 9+, Fedora 38+
- Build on Fedora 42 → Only works on Fedora 42+ (glibc too new)

**TAMs use RHEL/Rocky** → Must build on Rocky.

---

## 📋 Step 1: Install Build Dependencies (Rocky VM)

**In the Rocky Linux VM, run:**

```bash
# Development tools
sudo dnf groupinstall -y "Development Tools"

# Node.js (required for Electron build)
sudo dnf install -y nodejs npm

# Python build dependencies
sudo dnf install -y python3 python3-pip python3-devel

# AppImage dependencies
sudo dnf install -y fuse fuse-libs

# Additional libraries for PyInstaller
sudo dnf install -y zlib-devel bzip2-devel openssl-devel

# Verify versions
node --version   # Should be v16+
npm --version    # Should be 8+
python3 --version # Should be 3.9+
```

**Expected time**: 5-10 minutes (downloading packages)

---

## 📋 Step 2: Transfer Source Code to VM

**Option A: Create tarball and transfer via HTTP**

**On your laptop (host)**:
```bash
# Create tarball (exclude node_modules, dist, etc.)
cd /home/jbyrd
tar --exclude='TAMINATOR/node_modules' \
    --exclude='TAMINATOR/gui/node_modules' \
    --exclude='TAMINATOR/gui/dist' \
    --exclude='TAMINATOR/.git' \
    -czf TAMINATOR-source.tar.gz TAMINATOR/

# Serve it
cd ~
python3 -m http.server 8001 &
```

**In the Rocky VM**:
```bash
# Download source
cd ~
wget http://192.168.122.1:8001/TAMINATOR-source.tar.gz

# Extract
tar -xzf TAMINATOR-source.tar.gz

# Verify
cd TAMINATOR
ls -la
```

**Option B: SCP (if you prefer)**:
```bash
# On laptop
cd /home/jbyrd
tar czf TAMINATOR-source.tar.gz TAMINATOR/
scp TAMINATOR-source.tar.gz testuser@192.168.122.100:~/
```

---

## 📋 Step 3: Install Python Dependencies

**In the Rocky VM**:

```bash
cd ~/TAMINATOR

# Install Python dependencies
pip3 install --user -r requirements.txt

# Verify key packages
python3 -c "import fastapi; print('FastAPI OK')"
python3 -c "import uvicorn; print('Uvicorn OK')"
python3 -c "import keyring; print('Keyring OK')"
```

**If any imports fail**:
```bash
# Install individually
pip3 install --user fastapi uvicorn keyring httpx pydantic psutil
```

---

## 📋 Step 4: Install Node Dependencies

**In the Rocky VM**:

```bash
cd ~/TAMINATOR

# Install root dependencies (if any)
npm install

# Install GUI dependencies
cd gui
npm install

# This will take 3-5 minutes (downloading packages)
```

**Expected output**: `added XXX packages` (no errors)

---

## 📋 Step 5: Build AppImage

**In the Rocky VM**:

```bash
cd ~/TAMINATOR/gui

# Build (this takes 5-10 minutes)
npm run build

# Watch for errors
# Look for "Build complete" or similar success message
```

**What happens during build**:
1. Webpack bundles frontend (Electron GUI)
2. PyInstaller packages backend (Python service)
3. electron-builder creates AppImage
4. Output: `gui/dist/Taminator-2.0.0.AppImage`

**Common issues**:
- **Out of memory**: Increase VM RAM to 4GB
- **PyInstaller fails**: Check Python deps installed
- **Electron build fails**: Check Node version (need 16+)

---

## 📋 Step 6: Test AppImage

**In the Rocky VM**:

```bash
cd ~/TAMINATOR/gui/dist

# Make executable (if needed)
chmod +x Taminator-2.0.0.AppImage

# Test launch
./Taminator-2.0.0.AppImage

# Check for errors in terminal
# GUI should launch, OOBE wizard should appear
# Backend service should start without glibc errors
```

**Success criteria**:
- ✅ No "GLIBC_ABI_DT_RELR not found" error
- ✅ OOBE wizard appears
- ✅ Backend service starts (check status bar)
- ✅ Can add JIRA token

---

## 📋 Step 7: Transfer AppImage Back to Laptop

**In the Rocky VM**:
```bash
# Start HTTP server in VM
cd ~/TAMINATOR/gui/dist
python3 -m http.server 9000
```

**On your laptop (host)**:
```bash
# Download from VM
cd /home/jbyrd/TAMINATOR/gui/dist
wget http://192.168.122.100:9000/Taminator-2.0.0.AppImage -O Taminator-2.0.0-rocky.AppImage

# Backup old one
mv Taminator-2.0.0.AppImage Taminator-2.0.0-fedora42.AppImage

# Use Rocky-built version
mv Taminator-2.0.0-rocky.AppImage Taminator-2.0.0.AppImage
```

---

## 📋 Step 8: Verify Compatibility

**Check glibc requirements**:

```bash
# Extract AppImage
cd /home/jbyrd/TAMINATOR/gui/dist
./Taminator-2.0.0.AppImage --appimage-extract

# Check service binary dependencies
ldd squashfs-root/resources/bin/taminator-service | grep GLIBC

# Should NOT see GLIBC_ABI_DT_RELR
# Should see GLIBC_2.34 or lower (Rocky 9 compatible)
```

---

## 📋 Complete Build Script (For Future)

**Save as `build-on-rocky.sh` in Rocky VM**:

```bash
#!/bin/bash
# Build Taminator AppImage on Rocky Linux 9

set -e  # Exit on error

echo "=== Taminator Rocky Build Script ==="
echo ""

# Check dependencies
echo "Checking dependencies..."
command -v node >/dev/null || { echo "Node.js not installed"; exit 1; }
command -v npm >/dev/null || { echo "npm not installed"; exit 1; }
command -v python3 >/dev/null || { echo "Python3 not installed"; exit 1; }

echo "✅ Dependencies OK"
echo ""

# Install Python deps
echo "Installing Python dependencies..."
cd ~/TAMINATOR
pip3 install --user -q -r requirements.txt
echo "✅ Python deps installed"
echo ""

# Install Node deps
echo "Installing Node dependencies..."
cd gui
npm install --silent
echo "✅ Node deps installed"
echo ""

# Build
echo "Building AppImage..."
npm run build
echo ""

# Verify
if [ -f "dist/Taminator-2.0.0.AppImage" ]; then
    echo "✅ Build complete!"
    echo "AppImage: ~/TAMINATOR/gui/dist/Taminator-2.0.0.AppImage"
    ls -lh dist/Taminator-2.0.0.AppImage
else
    echo "❌ Build failed - AppImage not found"
    exit 1
fi
```

**Make executable and run**:
```bash
chmod +x build-on-rocky.sh
./build-on-rocky.sh
```

---

## 📋 Troubleshooting

### Issue: "npm ERR! code ELIFECYCLE"

**Cause**: Build script failed

**Solution**:
```bash
# Check detailed logs
cat gui/dist/builder-debug.log

# Common fix: Clean and rebuild
cd gui
rm -rf node_modules dist
npm install
npm run build
```

### Issue: "PyInstaller: command not found"

**Cause**: PyInstaller not in PATH

**Solution**:
```bash
pip3 install --user pyinstaller
export PATH="$HOME/.local/bin:$PATH"
```

### Issue: "Out of memory"

**Cause**: VM doesn't have enough RAM

**Solution**:
- Increase VM RAM to 4GB
- Or close other applications
- Or build with: `NODE_OPTIONS=--max-old-space-size=2048 npm run build`

### Issue: "fuse: device not found"

**Cause**: FUSE not available in VM

**Solution**:
```bash
# Load fuse module
sudo modprobe fuse

# Or run AppImage with --appimage-extract-and-run
./Taminator-2.0.0.AppImage --appimage-extract-and-run
```

---

## 📋 Build Time Estimates

**First time** (cold build):
- Install dependencies: 10 minutes
- Transfer source: 2 minutes
- Install Python deps: 3 minutes
- Install Node deps: 5 minutes
- Build AppImage: 10 minutes
- **Total: ~30 minutes**

**Subsequent builds** (after setup):
- Update source: 1 minute
- Rebuild: 10 minutes
- **Total: ~11 minutes**

---

## 📋 Best Practices

### Before Building
- [ ] Clean previous build artifacts
- [ ] Update dependencies if needed
- [ ] Check disk space (need 2GB free)
- [ ] Verify internet connection (for npm/pip)

### During Building
- [ ] Monitor for errors in terminal
- [ ] Don't interrupt build process
- [ ] Check memory usage (top/htop)

### After Building
- [ ] Test AppImage on Rocky VM first
- [ ] Check glibc requirements (ldd)
- [ ] Test on laptop (optional)
- [ ] Transfer to distribution location

---

## 📋 CI/CD Integration (Future)

**GitLab CI on Rocky 9 runner**:

```yaml
# .gitlab-ci.yml
build-appimage:
  image: rockylinux:9
  
  before_script:
    - dnf groupinstall -y "Development Tools"
    - dnf install -y nodejs npm python3 python3-pip python3-devel
  
  script:
    - pip3 install -r requirements.txt
    - cd gui
    - npm install
    - npm run build
  
  artifacts:
    paths:
      - gui/dist/*.AppImage
    expire_in: 30 days
  
  only:
    - tags
    - main
```

---

## 🎯 Success Criteria

**Build successful when**:
- ✅ AppImage created in `gui/dist/`
- ✅ No glibc errors on Rocky VM
- ✅ Backend service starts correctly
- ✅ OOBE wizard appears
- ✅ Can complete full workflow (JIRA token → Dashboard → Check)

---

**Ready to start?** Follow steps 1-8 above! 🚀

