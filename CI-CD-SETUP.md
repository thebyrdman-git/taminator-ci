# CI/CD Setup - Self-Hosted GitHub Runner

## Architecture

```
GitHub.com (thebyrdman-git/taminator-staging)
    ↓ (Push triggers workflow)
MiracleMax Self-Hosted Runner (RHEL 9.6)
    ↓ (Builds all platforms)
Artifacts Published to GitHub Actions
```

## Self-Hosted Runner

**Location**: MiracleMax server (`miraclemax.local`)  
**Service**: `actions.runner.thebyrdman-git-taminator-staging.miraclemax-taminator.service`  
**Status**: ✅ Connected and listening for jobs

### Check Runner Status
```bash
ssh miraclemax.local
sudo systemctl status actions.runner.thebyrdman-git-taminator-staging.miraclemax-taminator.service
```

## GitHub Actions Workflow

**File**: `.github/workflows/build-all-platforms.yml`

### Triggers
- Push to `main` branch
- Pull requests to `main`
- Manual workflow dispatch

### Jobs

1. **build-linux-x64** - Linux x86_64 AppImage/DEB/RPM
   - Uses self-hosted runner
   - Builds service binary with PyInstaller
   - Builds Electron GUI
   - Creates AppImage, DEB, RPM packages

2. **build-linux-arm64** - Linux ARM64 AppImage
   - Uses Docker buildx multi-arch
   - Cross-compiles for ARM64
   - Creates ARM64 AppImage

3. **build-macos** - macOS Universal DMG
   - Currently placeholder (requires macOS hardware)
   - Documents requirements

4. **build-windows** - Windows NSIS Installer
   - Currently placeholder (requires Windows hardware)
   - Documents requirements

5. **create-release** - Consolidates all artifacts
   - Downloads all build artifacts
   - Creates release summary
   - Publishes combined artifacts

## Build Artifacts

All builds are saved as GitHub Actions artifacts (30 day retention):

- `taminator-linux-x64` - AppImage, DEB, RPM
- `taminator-linux-arm64` - ARM64 AppImage
- `taminator-macos-placeholder` - Setup instructions
- `taminator-windows-placeholder` - Setup instructions
- `release-summary` - Combined release notes

## Triggering Builds

### Automatic (on push to main)
```bash
cd /home/jbyrd/TAMINATOR
git add .
git commit -m "feat: your changes"
git push github main
```

### Manual Trigger
1. Go to: https://github.com/thebyrdman-git/taminator-staging/actions
2. Select "Build Taminator v2.0 - All Platforms"
3. Click "Run workflow"
4. Select branch: `main`
5. Click "Run workflow"

## Monitoring Builds

### Via GitHub UI
https://github.com/thebyrdman-git/taminator-staging/actions

### Via Runner Logs (SSH to MiracleMax)
```bash
ssh miraclemax.local
sudo journalctl -u actions.runner.thebyrdman-git-taminator-staging.miraclemax-taminator.service -f
```

## Downloading Artifacts

### Via GitHub UI
1. Go to workflow run: https://github.com/thebyrdman-git/taminator-staging/actions
2. Click on completed workflow
3. Scroll to "Artifacts" section
4. Download desired artifacts

### Via GitHub CLI
```bash
# Install gh CLI if needed
gh auth login

# List artifacts
gh run list --repo thebyrdman-git/taminator-staging

# Download artifacts from specific run
gh run download <RUN_ID> --repo thebyrdman-git/taminator-staging
```

## Platform-Specific Notes

### Linux x86_64
✅ **Working** - Built on self-hosted runner
- AppImage (universal Linux binary)
- DEB package (Debian/Ubuntu)
- RPM package (Fedora/RHEL)

### Linux ARM64
🟡 **Cross-compile via Docker** - Builds using buildx
- ARM64 AppImage
- Requires Docker buildx support on runner
- Tested on ARM64 hardware recommended

### macOS
⏳ **Placeholder** - Requires native macOS hardware
- Options:
  1. Use macOS self-hosted runner
  2. Use GitHub macOS runners ($$$)
  3. Local build on macOS machine

### Windows
⏳ **Placeholder** - Requires Windows hardware or Wine
- Options:
  1. Use Windows self-hosted runner
  2. Use GitHub Windows runners ($$$)
  3. Wine + electron-builder on Linux (experimental)
  4. Local build on Windows machine

## Local Testing (Before Push)

### Test Service Build
```bash
cd /home/jbyrd/TAMINATOR
PYTHONPATH=src python3 -m PyInstaller taminator-service.spec --clean
./dist/taminator-service --version
```

### Test GUI Build
```bash
cd /home/jbyrd/TAMINATOR/gui
npm run build
./dist/Taminator-2.0.0.AppImage
```

### Test Full Pipeline Locally
```bash
cd /home/jbyrd/TAMINATOR
./test-tesla-integration.sh
```

## Troubleshooting

### Runner Not Picking Up Jobs
```bash
# Check runner status
ssh miraclemax.local
sudo systemctl status actions.runner.thebyrdman-git-taminator-staging.miraclemax-taminator.service

# Restart runner
sudo systemctl restart actions.runner.thebyrdman-git-taminator-staging.miraclemax-taminator.service

# Check logs
sudo journalctl -u actions.runner.thebyrdman-git-taminator-staging.miraclemax-taminator.service -n 100
```

### Build Fails
1. Check workflow logs in GitHub UI
2. Look for specific error messages
3. Test locally first with same commands
4. Verify dependencies installed on runner

### ARM64 Build Issues
1. Verify Docker buildx installed on runner
2. Check multiarch builder exists
3. Test ARM64 image locally:
   ```bash
   docker buildx build --platform linux/arm64 -f Dockerfile.arm64 .
   ```

### Artifacts Not Uploading
1. Check file paths in workflow match actual build output
2. Verify artifact names are unique
3. Check GitHub Actions artifact size limits (500MB per artifact)

## Future Enhancements

### macOS Native Builds
- Deploy macOS runner (Mac Mini or cloud macOS)
- Update workflow to use `runs-on: macos-latest` or `macos-runner`

### Windows Native Builds
- Deploy Windows runner (VM or bare metal)
- Install Node.js, Python, NSIS
- Update workflow to use `runs-on: windows-latest` or `windows-runner`

### Automated Releases
- Add GitHub Release creation on tag push
- Auto-publish to GitHub Releases
- Generate changelog automatically

### Testing
- Add unit tests
- Add integration tests
- Add E2E tests with Playwright

## Reference

- **GitHub Workflow**: `.github/workflows/build-all-platforms.yml`
- **Runner Setup**: `/home/jbyrd/pai/miraclemax-infrastructure/GITHUB-RUNNER-SUCCESS.md`
- **Ansible Deployment**: `/home/jbyrd/pai/miraclemax-infrastructure/ansible/playbooks/github-runner.yml`

