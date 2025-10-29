# AppImage Compatibility Issue - GLIBC Version Mismatch

**Date**: October 28, 2025  
**Severity**: CRITICAL BLOCKER  
**Impact**: AppImage won't run on Rocky Linux (or RHEL 8/9, Alma, CentOS Stream)

---

## 🚨 Problem

**Error in VM**:
```
[Service Error] /tmp/.mount_Tamina0s1N53/resources/bin/taminator-service: 
/lib64/libc.so.6: version `GLIBC_ABI_DT_RELR' not found 
(required by /tmp/_MEIwS6M8N/libz.so.1)
```

**Root Cause**:
- AppImage built on **Fedora 42** (glibc 2.40+, bleeding edge)
- Testing on **Rocky Linux 9** (glibc 2.34, stable)
- PyInstaller bundles system libraries from build machine
- `GLIBC_ABI_DT_RELR` only exists in glibc 2.40+ (not in RHEL/Rocky)

---

## 📊 Impact Analysis

### What Works
- ✅ GUI launches (Electron part)
- ✅ OOBE wizard appears
- ✅ Frontend UI loads

### What Fails
- ❌ Backend service won't start (Python/PyInstaller binary)
- ❌ API calls fail (no backend)
- ❌ All functionality broken (JIRA, Portal, rhcase)

### Affected Platforms
- ❌ RHEL 8/9
- ❌ Rocky Linux 8/9
- ❌ AlmaLinux 8/9
- ❌ CentOS Stream 8/9
- ✅ Fedora 40+ (works)
- ✅ Ubuntu 24.04+ (likely works)
- ❓ Debian (unknown)

---

## 🎯 Solutions

### Option 1: Rebuild on Rocky Linux (Best for Alpha)

**Build AppImage on Rocky Linux 9** (oldest supported platform):

```bash
# SSH into Rocky VM or use Rocky container
ssh testuser@rocky-vm

# Install dependencies
sudo dnf install -y npm nodejs python3 python3-pip gcc make

# Clone repo (or transfer)
cd ~/
# (transfer TAMINATOR directory)

# Build on Rocky
cd TAMINATOR
npm install
npm run build

# Result: AppImage compatible with Rocky 9+, RHEL 9+, Fedora 38+
```

**Pros**:
- Works on all target platforms (Rocky, RHEL, Fedora)
- Standard approach for Linux AppImage builds

**Cons**:
- Need to set up build environment on Rocky
- Takes 10-15 minutes first time

---

### Option 2: Docker Build Container (Professional)

**Use manylinux or Rocky container** for reproducible builds:

```bash
# Create build container
docker run -it --rm -v /home/jbyrd/TAMINATOR:/build rockylinux:9 bash

# Inside container
cd /build
dnf install -y npm nodejs python3 python3-pip gcc make
npm install
npm run build

# Result: AppImage in gui/dist/
```

**Pros**:
- Reproducible builds
- Don't need Rocky VM
- Can automate in CI/CD

**Cons**:
- Need Docker setup
- Slightly more complex

---

### Option 3: Test on Fedora VM Instead (Quick Workaround)

**Create Fedora 40+ VM** for testing:

```bash
# Download Fedora 40 or 41
# Install in VM
# Transfer existing AppImage (already built)
# Should work without rebuild
```

**Pros**:
- Existing AppImage works
- No rebuild needed
- Quick test

**Cons**:
- Not testing on target platform (RHEL/Rocky)
- TAMs use RHEL, not Fedora
- Not representative of production

---

### Option 4: Run from Source (Development Only)

**Skip AppImage, run directly** (for testing only):

```bash
# In Rocky VM
cd TAMINATOR

# Install Python deps
pip3 install --user -r requirements.txt

# Install Node deps
npm install

# Start backend manually
cd src
python3 -m taminator.api.main &

# Start frontend manually
npm start
```

**Pros**:
- Bypasses PyInstaller issue
- Can test functionality

**Cons**:
- Not testing AppImage distribution
- Requires Python/Node setup on VM
- Not how TAMs will use it

---

## 🎯 Recommended Approach for Alpha

**1. Rebuild on Rocky Linux 9** (30 minutes):

```bash
# Steps:
1. Fix VM build environment (install gcc, python3-devel, npm)
2. Transfer source to Rocky VM
3. Build on Rocky: npm run build
4. Test AppImage on Rocky
5. Distribute Rocky-built AppImage to TAMs
```

**2. Document Platform Requirements** (5 minutes):

Update README:
```markdown
## Platform Requirements

**Supported**:
- RHEL 9+
- Rocky Linux 9+
- AlmaLinux 9+
- Fedora 38+

**Build Requirements**:
- AppImage MUST be built on oldest supported platform (Rocky 9)
- Do NOT build on Fedora 42 (too new)
```

**3. Add CI/CD Build** (Future):

```yaml
# GitLab CI on Rocky 9 runner
build-appimage:
  image: rockylinux:9
  script:
    - dnf install -y npm nodejs python3 python3-pip gcc
    - npm install
    - npm run build
  artifacts:
    paths:
      - gui/dist/*.AppImage
```

---

## 🔍 Technical Details

### Why This Happens

**PyInstaller behavior**:
1. Bundles Python + dependencies into binary
2. Includes system libraries from build machine
3. `libz.so.1` from Fedora 42 requires `GLIBC_ABI_DT_RELR`
4. Rocky Linux 9 has glibc 2.34 (no `GLIBC_ABI_DT_RELR`)

**GLIBC_ABI_DT_RELR**:
- New ABI for dynamic linker optimizations
- Added in glibc 2.38+ (Fedora 38+)
- Not backported to RHEL 9 (glibc 2.34)

### Verification Commands

**Check glibc version**:
```bash
# On Rocky VM
ldd --version

# Output: ldd (GNU libc) 2.34
```

**Check binary requirements**:
```bash
# Extract AppImage
./Taminator-2.0.0.AppImage --appimage-extract

# Check service binary
ldd squashfs-root/resources/bin/taminator-service

# Shows: GLIBC_ABI_DT_RELR not found
```

---

## 📋 Action Plan

### Immediate (Tonight)

- [ ] **Option A**: Rebuild on Rocky VM (test tonight)
  - Install build deps on Rocky VM
  - Transfer source
  - Build AppImage
  - Test

- [ ] **Option B**: Test on Fedora VM (quick validation)
  - Verify existing AppImage works on Fedora
  - Validates everything else works
  - Plan Rocky rebuild for tomorrow

### Short-Term (Before Alpha Release)

- [ ] Set up Rocky 9 build environment
- [ ] Document build process in README
- [ ] Update GETTING-STARTED with platform requirements
- [ ] Add glibc compatibility check to AppImage startup

### Long-Term (Post-Alpha)

- [ ] GitLab CI/CD on Rocky 9 runner
- [ ] Multi-platform builds (Rocky, Ubuntu, Fedora)
- [ ] Automated compatibility testing
- [ ] Consider static linking for better portability

---

## 🎓 Lessons Learned

### What Went Wrong
- ❌ Built on bleeding-edge Fedora 42
- ❌ Didn't test on target platform (RHEL/Rocky)
- ❌ PyInstaller silently bundles incompatible libraries

### What to Do Next Time
- ✅ **Build on oldest supported platform** (Rocky 9)
- ✅ **Test on target platform first** (not dev machine)
- ✅ **Check glibc requirements** before distributing
- ✅ **CI/CD on target platform** (Rocky 9 runner)

### Industry Best Practice
**AppImage/Linux Distribution**:
- Build on **oldest supported platform**
- Example: Want to support RHEL 8+? Build on RHEL 8.
- Binaries work on same version + newer (not older)

---

## 🚀 Quick Decision Matrix

**Do you need to test Taminator functionality TONIGHT?**

**YES** → Use **Option 4** (run from source in VM)
- Takes 10 minutes
- Tests all features
- Not testing AppImage distribution

**Can wait until tomorrow?**

**YES** → Use **Option 1** (rebuild on Rocky)
- Takes 30 minutes setup + 10 min build
- Tests AppImage distribution
- Production-ready approach

**Want quick validation first?**

**YES** → Use **Option 3** (test on Fedora VM)
- Existing AppImage works
- 15 minutes to set up Fedora VM
- Then do Option 1 tomorrow

---

## 📞 Next Steps

**Recommended Path**:

1. **Tonight**: Run from source (Option 4) to validate functionality
2. **Tomorrow**: Rebuild on Rocky (Option 1) for proper AppImage
3. **This Week**: Document and add to CI/CD

**Or if you want to finish tonight**:

1. Set up Rocky build environment (30 min)
2. Rebuild AppImage on Rocky (10 min)
3. Test (30 min)
4. Total: ~70 minutes

---

**Your call!** What do you want to do?

- **A) Run from source tonight** (quick functional test)
- **B) Rebuild on Rocky tonight** (full test, takes longer)
- **C) Stop for tonight** (tackle tomorrow fresh)
- **D) Test on Fedora VM** (validate AppImage works on compatible platform)

