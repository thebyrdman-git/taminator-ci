# Git LFS Rules for Taminator

## Critical Configuration (MANDATORY)

### Always Upload One File at a Time

**WHY:** Red Hat GitLab LFS transfers timeout with concurrent uploads of large files (100+ MB AppImages).

**RULE:** Before ANY push to GitLab, set:

```bash
git config lfs.concurrenttransfers 1
```

**Verify:**
```bash
git config -l | grep lfs.concurrenttransfers
# Should show: lfs.concurrenttransfers=1
```

## When This Applies

- ✅ **EVERY** push to `git@gitlab.cee.redhat.com:jbyrd/taminator.git`
- ✅ Pushing release tags (e.g., `git push origin v1.10.3`)
- ✅ Pushing branches with new AppImage builds
- ✅ Any commit that includes files in `releases/`

## Symptoms of Missing This Configuration

```
# Push hangs or times out
Uploading LFS objects:  50% (1/2), 118 MB | 0 B/s
# ... connection timeout
```

## Standard Workflow

```bash
# 1. Configure LFS (once per repo clone)
cd /home/jbyrd/TAMINATOR
git config lfs.concurrenttransfers 1

# 2. Build release
cd gui
npm run build

# 3. Copy to releases
mkdir -p ../releases/v1.x.x
cp dist/Taminator-1.x.x.AppImage ../releases/v1.x.x/

# 4. Commit and tag
git add -f releases/v1.x.x/
git commit -m "Release v1.x.x"
git tag v1.x.x

# 5. Push (with LFS config active)
git push origin main
git push origin v1.x.x

# 6. Create GitLab release
glab release create v1.x.x releases/v1.x.x/Taminator-1.x.x.AppImage \
  --name "v1.x.x - Release Title" \
  --notes "Release notes here"
```

## GitHub vs GitLab

- ✅ **GitHub:** No LFS timeout issues (handles concurrent transfers well)
- ⚠️ **Red Hat GitLab:** MUST use `lfs.concurrenttransfers=1`

## Automation

This configuration is set automatically in:
- Local `.git/config` (manual setup)
- GitHub Actions workflows (no LFS issues)
- GitLab CI/CD (add to `.gitlab-ci.yml` if needed)

## Reference

- GitLab Issue: LFS upload timeouts with large binaries
- Solution: https://github.com/git-lfs/git-lfs/issues/2133
- Red Hat Internal: Known limitation with GitLab LFS proxy

---

**REMEMBER:** One file at a time, or LFS uploads will timeout!

