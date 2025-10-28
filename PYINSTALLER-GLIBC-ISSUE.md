# PyInstaller GLIBC Issue - Deeper Analysis

**Status**: Built on Rocky 9, but still getting `GLIBC_ABI_DT_RELR not found`

**Problem**: PyInstaller is bundling a `libz.so.1` that requires glibc 2.40+, even though we're building on Rocky 9 (glibc 2.34).

---

## 🔍 Root Cause

**PyInstaller behavior**:
- Bundles Python + dependencies
- Includes **system libraries** from build machine
- `libz.so.1` (zlib compression library) is being bundled
- **But where is it getting the newer version?**

**Hypothesis**: 
- Rocky 9 has glibc 2.34, but some pip packages may have bundled newer libraries
- Or PyInstaller is finding a newer libz in a virtual environment or pip package

---

## 🔧 Solutions to Try

### Solution 1: Force Static Linking (Recommended)

**Modify PyInstaller spec file to exclude system libraries**:

```python
# In gui/build.spec or wherever PyInstaller spec is

a = Analysis(
    ['your_script.py'],
    ...
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add this to exclude problematic libraries
a.binaries = [x for x in a.binaries if not x[0].startswith('libz')]

# Force PyInstaller to use system libz
# (Rocky's libz, not bundled one)
```

---

### Solution 2: Use Older Python Build

**Install Python from source with older glibc compatibility**:

```bash
# In Rocky VM
sudo dnf install -y gcc make openssl-devel bzip2-devel libffi-devel zlib-devel

# Download Python 3.9 source (older, more compatible)
cd /tmp
wget https://www.python.org/ftp/python/3.9.18/Python-3.9.18.tgz
tar -xzf Python-3.9.18.tgz
cd Python-3.9.18

# Configure with static linking
./configure --enable-optimizations --with-ensurepip=install
make -j$(nproc)
sudo make altinstall

# Use this Python for build
/usr/local/bin/python3.9 -m pip install -r requirements.txt
/usr/local/bin/python3.9 -m pip install pyinstaller
```

---

### Solution 3: Docker with Older Base Image

**Use CentOS 7 or older Rocky container**:

```bash
# On laptop, use Docker with older base
docker run -it --rm -v /home/jbyrd/TAMINATOR:/build rockylinux:8 bash

# Inside container (Rocky 8 has even older glibc)
cd /build
dnf install -y python3 python3-pip gcc make nodejs npm
pip3 install -r requirements.txt
cd gui
npm install
npm run build
```

---

### Solution 4: Manual libz Replacement

**Replace bundled libz with Rocky's system libz**:

```bash
# After build
cd ~/TAMINATOR/gui/dist
./Taminator-2.0.0.AppImage --appimage-extract

# Find bundled libz
find squashfs-root -name "libz.so*"

# Replace with system libz
cp /lib64/libz.so.1 squashfs-root/_internal/libz.so.1

# Repackage AppImage
# (This is hacky but might work)
```

---

### Solution 5: Use AppImage Tool with Older Runtime

**Create AppImage with older runtime**:

```bash
# Download older AppImageTool
wget https://github.com/AppImage/AppImageKit/releases/download/12/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Extract current AppImage
./Taminator-2.0.0.AppImage --appimage-extract

# Rebuild with older runtime
./appimagetool-x86_64.AppImage squashfs-root Taminator-2.0.0-fixed.AppImage
```

---

### Solution 6: Skip PyInstaller, Use Python Directly

**Bundle Python interpreter instead of PyInstaller binary**:

This is more complex but most reliable:

1. Bundle Python 3.9 in AppImage
2. Bundle pip dependencies as `.whl` files
3. Run Python script directly (not compiled binary)

**Pros**: No PyInstaller issues  
**Cons**: Larger AppImage, slower startup

---

## 🎯 Recommended Approach

**Try in this order**:

1. **Solution 3** (Docker with Rocky 8) - 30 minutes
   - Most likely to work
   - Rocky 8 has glibc 2.28 (older than Rocky 9's 2.34)
   - Will definitely work on Rocky 9

2. **Solution 1** (Exclude libz) - 10 minutes
   - Quick to try
   - Might work if libz is the only issue

3. **Solution 6** (Skip PyInstaller) - 2 hours
   - Most reliable long-term
   - No more glibc issues ever
   - But requires refactoring build process

---

## 🔬 Debugging Commands

**Check what glibc symbols are needed**:

```bash
cd ~/TAMINATOR/gui/dist
./Taminator-2.0.0.AppImage --appimage-extract
readelf -V squashfs-root/resources/bin/taminator-service | grep GLIBC
objdump -T squashfs-root/_internal/libz.so.1 | grep GLIBC
```

**Find where libz is coming from**:

```bash
ldd squashfs-root/resources/bin/taminator-service | grep libz
```

---

## 🚨 Quick Decision

**Want to test Taminator functionality tonight?**
→ Use **Solution 6** (skip PyInstaller, run Python directly)

**Want proper AppImage that works?**
→ Use **Solution 3** (Docker with Rocky 8)

**Want quick experiment?**
→ Use **Solution 1** (exclude libz from spec file)

---

What do you want to try?

