# Manual Workflow Trigger Instructions

## 🎯 When to Use This

If the workflow doesn't auto-trigger within 2-3 minutes after pushing the tag, manually trigger it.

## 📋 Step-by-Step Instructions

### Method 1: GitHub Web UI (Recommended)

1. **Go to the workflow page**:
   https://github.com/thebyrdman-git/taminator-ci/actions/workflows/release.yml

2. **Click "Run workflow"** button (top right, next to "This workflow has a workflow_dispatch event trigger")

3. **In the dropdown that appears**:
   - **Use workflow from**: Select `main` (or whatever branch has your workflow file)
   - **Version to release**: Type `v1.9.2`

4. **Click the green "Run workflow" button**

5. **Wait ~5 seconds**, then refresh the page. You should see a new workflow run appear.

6. **Click on the workflow run** to watch the progress

### Method 2: GitHub CLI

```bash
cd /home/jbyrd/pai/taminator
chmod +x monitor-build.sh
./monitor-build.sh
```

When prompted, choose `y` to attempt manual trigger via CLI.

### Method 3: Manual gh CLI Command

```bash
gh workflow run release.yml \
  --repo thebyrdman-git/taminator-ci \
  --ref main \
  --field version=v1.9.2
```

Then check status:
```bash
gh run list --repo thebyrdman-git/taminator-ci --limit 5
```

## 🔍 What You'll See

After triggering, the workflow page will show:

```
Build and Release
  ✓ build-linux (3-10 min)
  ✓ build-windows (3-10 min)  
  ✓ build-macos (5-15 min)
  ✓ create-release (1-2 min)
```

**Total time**: ~20-30 minutes

## 📦 Expected Result

A new release at:
https://github.com/thebyrdman-git/taminator-ci/releases/tag/v1.9.2

With these files:
- `Taminator-1.9.2.AppImage` (~118 MB)
- `Taminator-Setup-1.9.2.exe` (~150 MB)
- `Taminator-1.9.2-x64.dmg` (~180 MB)
- `Taminator-1.9.2-arm64.dmg` (~180 MB)

## 🚨 If Build Fails

Click on the failed job to see logs. Common issues:

### Linux build fails
- **Missing dependencies**: Check `requirements.txt` exists
- **Python package errors**: May need to update package versions

### Windows build fails
- **Python install**: Check PowerShell syntax in workflow
- **electron-builder**: Verify Windows config in `gui/package.json`

### macOS build fails
- **Code signing**: May need Apple Developer certificate (can disable)
- **Timeout**: macOS runners are slower, increase timeout if needed

### All builds fail
- **Workflow syntax**: Check YAML syntax in `.github/workflows/release.yml`
- **Missing files**: Verify `gui/package.json` and `requirements.txt` exist

## 💡 Why Auto-Trigger Might Not Work

The most common reason: **The workflow file doesn't exist at the commit the tag points to.**

GitHub looks for `.github/workflows/release.yml` at the exact commit referenced by the tag. If that commit doesn't have the workflow file, nothing triggers.

**Solution**: Use manual trigger, which uses the workflow from `main` branch but builds the `v1.9.2` tag.

## ✅ Success Indicators

You'll know it worked when:

1. ✅ Workflow appears in Actions page
2. ✅ All 3 build jobs start (Linux, Windows, macOS)
3. ✅ Jobs complete successfully (green checkmarks)
4. ✅ Release appears with all 4 files attached
5. ✅ Files are downloadable and correct size

---

**Pro tip**: Bookmark the Actions page for easy monitoring:
https://github.com/thebyrdman-git/taminator-ci/actions

