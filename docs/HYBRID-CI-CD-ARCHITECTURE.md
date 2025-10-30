# Hybrid CI/CD Architecture

**Taminator uses a hybrid CI/CD approach to optimize costs and leverage the right infrastructure for each platform.**

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    TAMINATOR RELEASE PIPELINE                    │
└─────────────────────────────────────────────────────────────────┘

                              ┌──────────┐
                              │  Source  │
                              │  GitLab  │
                              │ (Private)│
                              └────┬─────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
            ┌───────▼────────┐          ┌────────▼────────┐
            │  GitHub CI     │          │  MiracleMax     │
            │  (Public)      │          │  Self-Hosted    │
            │                │          │                 │
            │ taminator-ci   │          │  GitLab Runner  │
            └───────┬────────┘          └────────┬────────┘
                    │                             │
        ┌───────────┴───────────┐     ┌──────────┴─────────┐
        │                       │     │                    │
   ┌────▼─────┐          ┌─────▼───┐ │  ┌──────────────┐  │
   │  macOS   │          │ Windows │ │  │  Linux x64   │  │
   │   DMG    │          │   EXE   │ │  │  AppImage    │  │
   │          │          │         │ │  └──────────────┘  │
   │ Intel +  │          │   x64   │ │  ┌──────────────┐  │
   │  Apple   │          │         │ │  │  Linux ARM64 │  │
   │ Silicon  │          │         │ │  │  AppImage    │  │
   └──────────┘          └─────────┘ │  └──────────────┘  │
                                     │  ┌──────────────┐  │
                                     │  │  Container   │  │
                                     │  │    Image     │  │
                                     │  └──────────────┘  │
                                     └────────────────────┘
```

## Why Hybrid?

### GitHub Actions (Public Repo)
**Repository:** `github.com/thebyrdman-git/taminator-ci` (PUBLIC)

**Builds:**
- macOS DMG (Intel + Apple Silicon)
- Windows EXE (x64)

**Why GitHub?**
- ✅ **Free unlimited minutes** for public repos
- ✅ **Native Mac runners** (no Mac Mini needed)
- ✅ **Native Windows runners** (no Windows VM needed)
- ✅ **Apple/Microsoft maintain runners** (auto-updates)
- ✅ **Fast builds** (cloud infrastructure)

**Cost:** $0/month

### MiracleMax Self-Hosted (Private GitLab)
**Repository:** `gitlab.cee.redhat.com/jbyrd/taminator` (PRIVATE)

**Builds:**
- Linux x86_64 AppImage (native)
- Linux ARM64 AppImage (QEMU emulation)
- Container Image (Podman)

**Why Self-Hosted?**
- ✅ **Red Hat internal network** (compliance)
- ✅ **Full control** over build environment
- ✅ **No cloud costs** (already have hardware)
- ✅ **Most TAMs use Linux** (primary platform)
- ✅ **Container-first deployment** (Red Hat standard)

**Cost:** $0/month (hardware already owned)

## Release Workflow

### 1. Local Development
```bash
cd /home/jbyrd/TAMINATOR
# Make changes, test locally
git commit -m "Feature: XYZ"
```

### 2. Automated Release (Ansible)
```bash
ansible-playbook ansible/playbooks/release-v2.0.yml
```

**This playbook:**
1. ✅ Pre-release audit (customer data check)
2. ✅ Build Cursor IDE extension (VSIX)
3. ✅ Build local artifacts (AppImage, DEB, Container)
4. ✅ Push to GitHub staging (test)
5. ✅ **Mirror to GitHub CI** (public repo) → triggers Mac/Windows builds
6. ✅ Push to GitLab production → triggers Linux builds

### 3. GitHub Actions (Mac/Windows)
**Triggered by:** Tag push to `taminator-ci`

**Builds:**
- macOS DMG (Universal)
- Windows EXE (x64)
- Generates checksums
- Creates GitHub release

**Monitor:** https://github.com/thebyrdman-git/taminator-ci/actions

**Time:** ~10-15 minutes

### 4. MiracleMax CI/CD (Linux)
**Triggered by:** Tag push to GitLab

**Builds:**
- Linux x86_64 AppImage (native)
- Linux ARM64 AppImage (QEMU)
- Container Image (Podman)
- Creates GitLab release

**Monitor:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines

**Time:** ~15-20 minutes

## Security & Compliance

### Public GitHub CI Repo
- ✅ **Sanitized code only** (no customer data)
- ✅ **Pre-push audit** (Ansible playbook checks)
- ✅ **No secrets** (builds don't need credentials)
- ✅ **Read-only for TAMs** (source is on GitLab)

### Private GitLab Repo
- ✅ **Red Hat internal network**
- ✅ **Full source code** (including internal docs)
- ✅ **Customer data allowed** (in gitignored files)
- ✅ **Self-hosted runner** (MiracleMax)

## Cost Comparison

### Before (All Cloud)
- GitHub Actions (private): $10/month (hit limit)
- Total: $10/month + manual Mac builds

### After (Hybrid)
- GitHub Actions (public): $0/month (unlimited)
- MiracleMax self-hosted: $0/month (hardware owned)
- Total: $0/month + fully automated

## Benefits

1. **Cost Savings:** $0/month vs $10+/month
2. **Full Automation:** Mac/Windows/Linux all automated
3. **Red Hat Compliance:** Linux builds on internal network
4. **Best of Both Worlds:** Cloud for Mac/Windows, self-hosted for Linux
5. **Scalability:** Unlimited GitHub Actions minutes
6. **Reliability:** Multiple build systems (redundancy)

## Maintenance

### GitHub CI (Public Repo)
- **Update frequency:** When GitHub Actions runners update (automatic)
- **Maintenance:** Minimal (GitHub maintains runners)
- **Monitoring:** GitHub Actions UI

### MiracleMax (Self-Hosted)
- **Update frequency:** Monthly (Ansible playbooks)
- **Maintenance:** Moderate (OS updates, GitLab runner updates)
- **Monitoring:** GitLab UI + Prometheus/Alertmanager

## Future Enhancements

1. **ARM64 Mac builds:** GitHub Actions supports Apple Silicon natively
2. **Cross-compilation:** Build Linux ARM64 on GitHub (faster than QEMU)
3. **Artifact caching:** Speed up builds with dependency caching
4. **Parallel builds:** Run all platforms simultaneously
5. **Release automation:** Auto-publish to both GitHub and GitLab releases

---

**This hybrid approach gives us the best of both worlds: free cloud builds for Mac/Windows and Red Hat-compliant self-hosted builds for Linux.**

