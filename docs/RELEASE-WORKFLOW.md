# Taminator Release Workflow

**Self-Hosted CI/CD on MiracleMax Infrastructure**

## Overview

Taminator uses a **two-stage release process** with self-hosted infrastructure:

1. **GitHub Staging** - Manual testing ground
2. **GitLab Production** - Automated builds via MiracleMax self-hosted runner

## Architecture

```
Local Development
    ↓
GitHub Staging (manual release)
    ↓
Test & Validate
    ↓
GitLab Production (push tag)
    ↓
MiracleMax Self-Hosted Runner
    ↓
Automated Builds (x86_64 + ARM64)
    ↓
GitLab Release (automatic)
```

## MiracleMax Self-Hosted Runner

**Infrastructure:** `miraclemax.local` (home server)

**Capabilities:**
- Native Linux x86_64 builds
- ARM64 builds via QEMU emulation
- Automatic GitLab release creation
- Artifact management

**Configuration:** `.gitlab-ci.yml`
- Runner tags: `miraclemax`, `taminator`, `docker`
- Builds triggered on tag push
- Artifacts expire after 7 days

## Release Process

### Phase 1: GitHub Staging

**Purpose:** Test release before production

**Steps:**
```bash
# 1. Run pre-release audit
ansible-playbook ansible/00-pre-release-audit.yml

# 2. Build locally
ansible-playbook ansible/01-build-appimage.yml
ansible-playbook ansible/02-build-deb.yml

# 3. Push to GitHub staging
ansible-playbook ansible/10-release-github.yml
```

**Manual Actions:**
1. Go to https://github.com/thebyrdman-git/taminator-staging/releases/new
2. Select tag `v2.0.0`
3. Upload artifacts from `gui/dist/`
4. Publish release
5. Test the release (download, install, verify)

### Phase 2: GitLab Production

**Purpose:** Official release via self-hosted CI/CD

**Steps:**
```bash
# Push to GitLab (triggers MiracleMax runner)
ansible-playbook ansible/11-release-gitlab.yml
```

**What Happens Automatically:**
1. Tag `v2.0.0` pushed to GitLab
2. MiracleMax runner detects tag
3. Runner builds:
   - Linux x86_64 AppImage (native)
   - Linux ARM64 AppImage (QEMU)
4. GitLab creates release automatically
5. Artifacts attached to release

**Monitor Pipeline:**
https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines

**View Release:**
https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v2.0.0

## CI/CD Pipeline Details

### Build Jobs

**`build:linux:x64`**
- Native x86_64 build on MiracleMax
- Fast (10-15 minutes)
- Produces: `Taminator-2.0.0-x86_64.AppImage`

**`build:linux:arm64`**
- QEMU emulation on MiracleMax
- Slower (30-60 minutes due to emulation)
- Produces: `Taminator-2.0.0-arm64.AppImage`

**`release:gitlab`**
- Triggered only on tags
- Creates GitLab release
- Attaches build artifacts
- Generates release notes

### Pipeline Triggers

**Automatic:**
- Push to `main` branch → Build only (no release)
- Push tag (e.g., `v2.0.0`) → Build + Release

**Manual:**
- Can trigger via GitLab UI
- Can re-run failed jobs

## Troubleshooting

### Pipeline Fails

**Check runner status:**
```bash
ssh miraclemax.local
sudo systemctl status gitlab-runner
```

**View runner logs:**
```bash
ssh miraclemax.local
sudo journalctl -u gitlab-runner -f
```

**Restart runner:**
```bash
ssh miraclemax.local
sudo systemctl restart gitlab-runner
```

### ARM64 Build Timeout

ARM64 builds via QEMU can take 1-2 hours. If timeout occurs:

1. Check `.gitlab-ci.yml` timeout setting (currently 2h)
2. Consider increasing timeout
3. Or disable ARM64 build temporarily

### Artifacts Not Attached

If GitLab release created but artifacts missing:

1. Check pipeline job status
2. Verify artifacts uploaded in job logs
3. Check artifact expiration (7 days)
4. Re-run failed build jobs

## Benefits of Self-Hosted CI/CD

✅ **No Cloud Costs** - Runs on existing infrastructure
✅ **Full Control** - Complete access to runner and logs
✅ **Red Hat Compliance** - Stays within internal network
✅ **Multi-Architecture** - x86_64 + ARM64 support
✅ **Automatic Releases** - No manual artifact upload
✅ **Audit Trail** - Full pipeline logs and history

## Comparison: Manual vs Automated

### Old Workflow (Manual)
1. Build locally
2. Upload to GitLab manually
3. Create release manually
4. Attach artifacts manually
5. Write release notes manually

**Time:** 30-45 minutes per release

### New Workflow (Self-Hosted CI/CD)
1. Push tag to GitLab
2. MiracleMax builds automatically
3. Release created automatically
4. Artifacts attached automatically

**Time:** 5 minutes (human), 30-60 minutes (automated)

## Future Enhancements

**Potential Additions:**
- Windows builds (requires Windows runner)
- macOS builds (requires macOS runner)
- Automated testing before release
- Slack notifications on build completion
- Email alerts on pipeline failures
- Container image builds (Podman)

**Current Limitations:**
- No Windows/macOS builds (Linux only)
- No automated testing (manual testing required)
- No multi-runner parallelization

---

**Documentation:** `RELEASE-WORKFLOW.md`
**Last Updated:** 2025-10-29
**Version:** 2.0.0


