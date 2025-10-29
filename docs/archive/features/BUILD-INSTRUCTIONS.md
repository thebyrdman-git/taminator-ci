# Taminator Build Instructions - v1.10.1+

## Overview

Taminator v1.10.1+ bundles the Python CLI as a standalone binary to eliminate external Python dependencies.

---

## Quick Build (Full Release)

```bash
# 1. Build Python CLI binary
./build-cli-binary.sh

# 2. Build Electron AppImage
cd gui
npm run build

# Output:
# - Binary: bin/tam-rfe (19MB)
# - AppImage: gui/dist/Taminator-1.10.1.AppImage (~130MB)
```

---

## Step-by-Step Build

### 1. Build Python CLI Binary

```bash
# Install PyInstaller (if needed)
pip3 install pyinstaller

# Install Taminator dependencies
pip3 install -r requirements.txt

# Build standalone binary
./build-cli-binary.sh

# Verify binary
./bin/tam-rfe --help
```

**Output:**
- `dist/tam-rfe` - Standalone binary (19MB)
- Automatically copied to `bin/tam-rfe` and `gui/bin/tam-rfe`

**What's Included in Binary:**
- Python 3.9 interpreter
- All Python dependencies (rich, requests, jinja2, pyyaml, cryptography)
- Taminator source code
- Templates

### 2. Build Electron AppImage

```bash
cd gui

# Install Node dependencies (if needed)
npm install

# Build AppImage
npm run build
```

**Output:**
- `gui/dist/Taminator-1.10.1-x86_64.AppImage` (~130MB)
- Includes bundled `tam-rfe` binary
- No external Python dependencies required

---

## Testing the Binary

### Test Standalone Binary

```bash
# Test help
./bin/tam-rfe --help

# Test dashboard (requires JIRA token)
./bin/tam-rfe dashboard

# Test config
./bin/tam-rfe config
```

### Test GUI

```bash
# Run in dev mode
cd gui
npm start

# Or test built AppImage
./gui/dist/Taminator-1.10.1-x86_64.AppImage
```

---

## Architecture Changes (v1.10.1)

### Before (v1.10.0)
```
AppImage
├── gui/ (Electron)
└── src/taminator/ (Python source - UNBUNDLED DEPS!)
    ├── cli.py
    └── commands/
        └── *.py

User System Requirements:
❌ Python 3.9+
❌ pip install rich requests jinja2 pyyaml cryptography
❌ tam-rfe in PATH
```

### After (v1.10.1)
```
AppImage
├── gui/ (Electron)
└── bin/
    └── tam-rfe (Standalone binary - ALL DEPS INCLUDED!)

User System Requirements:
✅ Nothing! (just download and run)
```

---

## File Structure

```
taminator/
├── bin/
│   └── tam-rfe                  # Bundled binary (copied here)
├── gui/
│   ├── bin/
│   │   └── tam-rfe              # Binary bundled in Electron
│   ├── main.js                  # Uses bundled binary
│   └── package.json             # Packages bin/tam-rfe
├── src/taminator/               # Python source (for building)
│   ├── cli.py
│   └── commands/
├── build-cli.spec               # PyInstaller config
├── build-cli-binary.sh          # Build script
└── requirements.txt             # Python deps (for building only)
```

---

## Smart CLI Detection (main.js)

The GUI now tries multiple sources in priority order:

```javascript
function getTamrfeCli() {
  // 1. Bundled binary (production - AppImage/DMG/EXE)
  if (exists('../bin/tam-rfe')) {
    return bundledBinary;
  }
  
  // 2. Python source (development mode)
  if (exists('../src/taminator/cli.py')) {
    return pythonSource;
  }
  
  // 3. System PATH (manual install fallback)
  return 'tam-rfe';
}
```

---

## Troubleshooting

### Binary Build Fails

**Issue:** `ModuleNotFoundError: No module named 'rich'`

**Fix:**
```bash
pip3 install -r requirements.txt
./build-cli-binary.sh
```

### Binary Too Large

**Current Size:** 19MB (acceptable for production)

**To Reduce Size:**
- Remove test dependencies from build
- Use `--strip` in PyInstaller
- Use UPX compression (already enabled)

### GUI Can't Find Binary

**Check:**
```bash
# Binary should exist here
ls -lh gui/bin/tam-rfe

# If missing, copy from dist
cp dist/tam-rfe gui/bin/
chmod +x gui/bin/tam-rfe
```

---

## Platform-Specific Builds

### Linux (x86_64)
```bash
./build-cli-binary.sh
cd gui && npm run build
```

### macOS (Universal)
```bash
# Build x86_64 binary
./build-cli-binary.sh

# Build DMG
cd gui
npm run build
```

### Windows
```bash
# Build on Windows with Python 3.9+
python -m pip install pyinstaller
python -m PyInstaller build-cli.spec

# Build EXE
cd gui
npm run build
```

---

## Release Checklist

- [ ] Build CLI binary: `./build-cli-binary.sh`
- [ ] Test binary: `./bin/tam-rfe --help`
- [ ] Copy to gui: `cp dist/tam-rfe gui/bin/`
- [ ] Update version: `gui/package.json`, `README.md`
- [ ] Build Electron: `cd gui && npm run build`
- [ ] Test AppImage on clean system (no Python)
- [ ] Test all GUI operations (dashboard, check, update, post, onboard)
- [ ] Create GitLab release
- [ ] Update RELEASE-NOTES-v1.10.1.md

---

## Performance

### Binary Startup Time
- Cold start: ~0.5 seconds
- Warm start: ~0.2 seconds
- Same as Python script for users with packages

### AppImage Size Comparison
- v1.10.0: 118 MB (Python source, no deps)
- v1.10.1: 130 MB (standalone binary with all deps)
- Increase: +12 MB (acceptable tradeoff)

---

## Dependencies Bundled in Binary

| Package | Version | Size | Purpose |
|---------|---------|------|---------|
| Python | 3.9 | ~8 MB | Interpreter |
| rich | 13.7.1 | ~2 MB | Terminal UI |
| requests | 2.32.3 | ~1 MB | HTTP/JIRA API |
| jinja2 | 3.1.6 | ~500 KB | Templates |
| pyyaml | 6.0.3 | ~300 KB | Config parsing |
| cryptography | 46.0.3 | ~5 MB | Token encryption |
| pygments | 2.19.2 | ~2 MB | Syntax highlighting |

**Total:** ~19 MB (compressed)

---

## Future Improvements

### Optimization
- [ ] Strip debug symbols (reduce by ~2 MB)
- [ ] Exclude unused modules (reduce by ~3 MB)
- [ ] Alternative: Use Nuitka instead of PyInstaller

### Multi-Arch Support
- [ ] Build ARM64 binary for Apple Silicon
- [ ] Build ARM64 binary for Graviton/Raspberry Pi
- [ ] Automated CI/CD builds for all architectures

### Caching
- [ ] Cache PyInstaller build artifacts
- [ ] Rebuild only when Python code changes
- [ ] Faster iteration during development

---

**Build System:** PyInstaller 6.16.0  
**Target Python:** 3.9+  
**Electron:** 33.2.0  
**Node.js:** 18+

