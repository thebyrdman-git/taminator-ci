# AppImage Fix - Missing service-manager.js

## Problem
AppImage failed to launch with error:
```
Error: Cannot find module './service-manager'
```

## Root Cause
`service-manager.js` and `logs-viewer.html` were not included in the electron-builder `files` list in `package.json`.

## Fix Applied
Updated `gui/package.json` to include:
- `service-manager.js` (service lifecycle management)
- `logs-viewer.html` (logs viewer window)

## Rebuild Instructions
```bash
cd /home/jbyrd/TAMINATOR/gui

# Clean previous build
rm -rf dist/

# Rebuild
npm run build

# Test AppImage
./dist/Taminator-2.0.0.AppImage
```

## Verification
The AppImage should now:
1. Launch without errors
2. Auto-start the taminator-service
3. Show the main window
4. Allow opening logs viewer

## Files Added to Bundle
- `service-manager.js` - Service lifecycle management
- `logs-viewer.html` - Logs viewer window
- Already included: `main.js`, `index.html`, `oobe-state.js`, `oobe-wizard.html`, `public/**/*`, `themes/**/*`

