# Remaining Tasks Before Alpha

**Current Status**: UX Polish Complete, rhcase Integrated, All Blockers Done  
**Architecture Score**: 92/100  
**Ready to Ship**: Not yet (per user request)

---

## 🎯 Tasks Remaining

### Priority 1: Documentation (2-3 hours)

#### A) Update README for v2.0
**What**: Rewrite README to reflect new architecture  
**Current**: Outdated (references old CLI-spawning design)  
**Needs**:
- v2.0 architecture overview (FastAPI + Electron)
- Installation instructions
- Quick start guide
- Features list (updated)
- Screenshots/GIFs

**Time**: 1 hour  
**Impact**: High (first thing users see)

#### B) Write GETTING-STARTED Guide
**What**: Step-by-step first-use guide  
**Content**:
1. Install Taminator
2. First launch (OOBE wizard)
3. Configure JIRA/Portal tokens
4. Onboard first customer
5. Generate first report
6. Post to Portal

**Time**: 1 hour  
**Impact**: High (reduces support burden)

#### C) Troubleshooting Guide
**What**: Common issues and fixes  
**Content**:
- VPN connection issues
- Token authentication failures
- Service crashes
- rhcase not found
- AI/LiteLLM setup

**Time**: 30 mins  
**Impact**: Medium (self-service fixes)

---

### Priority 2: Testing (2-4 hours)

#### D) Test rhcase Integration
**What**: Verify all rhcase commands work via API  
**Commands to test**:
- `rhcase analyze <case_id>`
- `rhcase list <account>`
- `rhcase kcs search <query>`
- `rhcase kcs fetch <id>`
- `rhcase jira search <query>`
- `rhcase jira fetch <id>`
- `rhcase doctor`

**Time**: 1 hour  
**Impact**: Critical (core functionality)

#### E) Test on Clean Linux VM
**What**: Fresh install, no prior config  
**Tests**:
- AppImage runs on clean system
- OOBE wizard works
- Token configuration works
- First customer onboard works
- No missing dependencies

**Time**: 1 hour  
**Impact**: High (catches packaging issues)

#### F) Test with Real Customer Data
**What**: Use actual TAM workflows  
**Tests**:
- Onboard real customer (non-sensitive)
- Check real JIRA issues
- Update real report
- Post to test Portal group

**Time**: 1 hour  
**Impact**: High (real-world validation)

---

### Priority 3: Missing Features (3-5 hours)

#### G) CLI/GUI Parity
**Status**: Partially implemented  
**Missing**:
- Some GUI features don't have CLI equivalents
- Some CLI features missing from GUI
- Cross-platform command names (tam-rfe.exe vs tam-rfe)

**Time**: 2 hours  
**Impact**: Medium (nice-to-have for v2.0)

#### H) Red Hat Documentation System
**Status**: Deferred (v2.1+)  
**What**:
- `--help` for all commands
- Man pages
- Web-based docs (docs.redhat.com style)
- Search functionality

**Time**: 4-6 hours  
**Impact**: Low (can defer to v2.1)

---

### Priority 4: Pre-Alpha Checklist

#### I) Security Audit
**What**: Final security review  
**Check**:
- No hardcoded secrets
- No customer data in repo
- No debug code
- DevTools disabled in production
- PKCE implemented (✅ done)

**Time**: 30 mins  
**Impact**: Critical (before release)

#### J) Performance Testing
**What**: Ensure smooth performance  
**Tests**:
- Service startup time
- Dashboard load time
- Report generation speed
- API response times
- Memory usage

**Time**: 1 hour  
**Impact**: Medium (UX quality)

---

## 📊 Effort vs Impact Matrix

| Task | Effort | Impact | Priority |
|------|--------|--------|----------|
| **README Update** | 1h | High | ⭐⭐⭐ Do First |
| **GETTING-STARTED** | 1h | High | ⭐⭐⭐ Do First |
| **rhcase Testing** | 1h | Critical | ⭐⭐⭐ Do First |
| **Security Audit** | 30m | Critical | ⭐⭐⭐ Do First |
| Troubleshooting | 30m | Medium | ⭐⭐ Can wait |
| Clean VM Test | 1h | High | ⭐⭐ Pre-alpha |
| Real Data Test | 1h | High | ⭐⭐ Pre-alpha |
| Performance Test | 1h | Medium | ⭐⭐ Nice-to-have |
| CLI/GUI Parity | 2h | Medium | ⭐ v2.1+ |
| Docs System | 6h | Low | ⭐ v2.1+ |

---

## 🎯 Recommended Session Plan

### Session 1: Documentation Blitz (3 hours)
1. **README Update** (1h)
2. **GETTING-STARTED Guide** (1h)
3. **Security Audit** (30m)
4. **Troubleshooting Guide** (30m)

**Result**: Professional docs, security verified

---

### Session 2: Testing Marathon (3 hours)
1. **rhcase Integration Tests** (1h)
2. **Clean VM Testing** (1h)
3. **Real Customer Data Testing** (1h)

**Result**: Validated, ready for alpha

---

### Session 3: Alpha Build & Ship (1 hour)
1. **Bundle rhcase** (20m)
2. **Build AppImage** (20m)
3. **Create GitHub Release** (20m)

**Result**: Alpha distributed to TAMs

---

## 💡 Quick Wins (If Short on Time)

**30-Minute Sessions:**
- ✅ Security Audit (30m)
- ✅ Troubleshooting Guide (30m)
- ✅ rhcase Health Check Test (30m)

**1-Hour Sessions:**
- ✅ README Update (1h)
- ✅ GETTING-STARTED Guide (1h)
- ✅ rhcase Full Testing (1h)

---

## 🚀 What Do You Want to Tackle?

### Option 1: Documentation First
- Get professional docs done
- Makes alpha more polished
- Reduces support questions

### Option 2: Testing First
- Validate everything works
- Find bugs before TAMs do
- Confidence in alpha quality

### Option 3: Security + Quick Wins
- Security audit (critical)
- Troubleshooting guide (helpful)
- rhcase smoke test (validation)

### Option 4: Mix and Match
- Pick specific tasks from the list
- You choose the order

---

**What would you like to work on?**

