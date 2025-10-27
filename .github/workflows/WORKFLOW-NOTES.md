# GitHub Actions Workflow Notes - v1.10.1+

## Key Changes from Previous Versions

### v1.10.1 Architecture Change
**Problem:** Python CLI dependencies weren't bundled, causing `spawn tam-rfe ENOENT` errors

**Solution:** Build standalone binary with PyInstaller before building Electron apps

## Build Flow

```
1. build-cli-binary (ubuntu-latest)
   ├─ Install PyInstaller
   ├─ Build standalone tam-rfe binary
   └─ Upload as artifact

2. build-windows (needs: build-cli-binary)
   ├─ Download CLI binary artifact
   ├─ Build Electron with bundled binary
   └─ Create Windows NSIS installer

3. build-macos (needs: build-cli-binary)
   ├─ Download CLI binary artifact
   ├─ Build Electron with bundled binary
   └─ Create macOS DMG

4. build-linux (needs: build-cli-binary)
   ├─ Download CLI binary artifact
   ├─ Build Electron with bundled binary
   └─ Create Linux AppImage (x64 + arm64)
```

## Lessons Learned Applied

### ✅ 1. No npm Cache
**Issue:** `package-lock.json` may not be committed (in `.gitignore`)
**Fix:** Removed `cache: 'npm'` and `cache-dependency-path`
**Result:** Use `npm install` instead of `npm ci` - slightly slower but always works

### ✅ 2. No Python Setup in Electron Builds
**Issue:** v1.10.0 workflow tried to install Python deps that don't exist
**Fix:** Python setup ONLY in `build-cli-binary` job
**Result:** Clean separation of concerns

### ✅ 3. Correct Working Directory
**Issue:** Workflow assumed `gui/` at repo root
**Fix:** Always use `working-directory: gui` (not at root)
**Result:** Commands execute in correct location

### ✅ 4. Use electron-builder CLI
**Issue:** Assumed platform-specific npm scripts existed
**Fix:** Call `npx electron-builder --platform --publish never` directly
**Result:** Works regardless of package.json scripts

### ✅ 5. Repository Field Required
**Issue:** electron-builder needs repository metadata
**Fix:** Already in package.json - no change needed
**Result:** Update info generated correctly

## Binary Build Details

### Why PyInstaller?
- Bundles Python 3.9 interpreter
- Includes all dependencies (rich, requests, jinja2, pyyaml, cryptography)
- Creates 19MB standalone binary
- No external Python installation required

### Binary Artifact Flow
1. Built on ubuntu-latest (Linux x86_64)
2. Uploaded as GitHub Actions artifact
3. Downloaded by each platform build job
4. Placed in `bin/tam-rfe`
5. Packaged by electron-builder into final app

### Binary Compatibility
- Built on Linux, works on Linux ✅
- Windows/macOS builds use Linux binary? ❌
  - **TODO:** Need platform-specific binaries OR
  - **Current:** Linux builds work, Windows/macOS still need system tam-rfe

## Known Limitations

### Current State
- ✅ Linux AppImage: Fully self-contained
- ⚠️ macOS DMG: May need system Python (binary is Linux)
- ⚠️ Windows EXE: May need system Python (binary is Linux)

### Future Improvement
Build platform-specific binaries:
```yaml
build-cli-binary:
  strategy:
    matrix:
      os: [ubuntu-latest, macos-latest, windows-latest]
  runs-on: ${{ matrix.os }}
```

## Trigger Conditions

### Automatic Triggers
- Push to `main` branch
- Push tags matching `v*` pattern
- Pull requests to `main`

### Manual Trigger
- GitHub Actions UI → Run workflow

### Tag-Based Releases
When you push a tag:
```bash
git tag v1.10.1
git push origin v1.10.1
```

Workflow will:
1. Build all platforms
2. Create GitHub Release
3. Upload artifacts to release

## Debugging Failed Builds

### Check Job Logs
1. Go to Actions tab in GitHub
2. Click failed workflow run
3. Click failed job
4. Expand failed step
5. Read ENTIRE error message (not just first line)

### Common Issues

**Issue:** `npm ci` fails
**Fix:** Delete `package-lock.json` from git, use `npm install`

**Issue:** Binary not found
**Fix:** Check artifact download step, verify path

**Issue:** `working-directory` error
**Fix:** Verify directory structure in repo

**Issue:** electron-builder fails
**Fix:** Check that `repository` field exists in package.json

### Testing Locally Before Push

```bash
# Test CLI binary build
./build-cli-binary.sh

# Test Electron build (each platform)
cd gui

# Linux
npx electron-builder --linux --x64 --publish never

# macOS (on macOS only)
npx electron-builder --mac --publish never

# Windows (on Windows only)
npx electron-builder --win --publish never
```

## Artifact Retention

- CLI binary: 1 day (only needed for current build)
- Platform builds: 30 days
- Tagged releases: Permanent (GitHub Releases)

## Security Notes

- `GH_TOKEN` from `secrets.GITHUB_TOKEN` (automatic)
- No custom secrets required
- Binary uploaded as artifact (internal to GitHub Actions)
- Release uploads use same token

## Performance

### Build Times (Approximate)
- build-cli-binary: 3-5 minutes
- build-windows: 8-12 minutes
- build-macos: 10-15 minutes
- build-linux (each arch): 8-12 minutes
- **Total:** ~40-50 minutes for all platforms

### Parallelization
- CLI binary: Sequential (prerequisite)
- Platform builds: Parallel (after CLI ready)
- Linux architectures: Parallel within job

## Version Updates

When releasing new version:
1. Update `gui/package.json` version
2. Update `README.md` version
3. Create release notes
4. Commit changes
5. Tag: `git tag v1.X.X`
6. Push: `git push origin v1.X.X`
7. Workflow auto-triggers
8. Check Actions tab for progress

## Rollback Procedure

If build fails:
```bash
# Delete bad tag locally
git tag -d v1.10.1

# Delete bad tag remotely
git push origin :refs/tags/v1.10.1

# Fix issue, then re-tag
git tag v1.10.1
git push origin v1.10.1
```

## References

- Lessons Learned: `docs/archive/GITHUB-ACTIONS-LESSONS-LEARNED.md`
- Build Instructions: `BUILD-INSTRUCTIONS.md`
- Bug Fix Summary: `BUGFIX-v1.10.1-SUMMARY.md`

