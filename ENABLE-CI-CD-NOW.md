# Enable GitLab CI/CD for TAMINATOR

**Issue:** Pipeline didn't start automatically after push  
**Cause:** CI/CD not enabled in project settings

---

## 🔧 Fix: Enable CI/CD

### Step 1: Enable CI/CD Feature

1. **Go to project settings:**
   ```
   https://gitlab.cee.redhat.com/jbyrd/taminator/-/settings/general
   ```

2. **Expand:** "Visibility, project features, permissions"

3. **Find:** "CI/CD" toggle (should be near Repository, Issues, etc.)

4. **Enable:** Toggle it ON

5. **Save changes:** Click the green "Save changes" button at bottom

### Step 2: Enable Shared Runners

1. **Go to CI/CD settings:**
   ```
   https://gitlab.cee.redhat.com/jbyrd/taminator/-/settings/ci_cd
   ```

2. **Expand:** "Runners" section

3. **Enable:** "Enable shared runners for this project"

4. **Optional:** You might see "miraclemax" or other Red Hat runners listed

### Step 3: Verify .gitlab-ci.yml

1. **Check the file is in the repo:**
   ```
   https://gitlab.cee.redhat.com/jbyrd/taminator/-/blob/main/.gitlab-ci.yml
   ```

2. **Validate syntax:**
   - GitLab should show a green checkmark if syntax is valid
   - Or use: https://gitlab.cee.redhat.com/jbyrd/taminator/-/ci/lint

### Step 4: Trigger a Pipeline

**Option A: Push again**
```bash
cd /home/jbyrd/TAMINATOR
git commit --allow-empty -m "chore: Trigger CI/CD pipeline"
git push origin main
```

**Option B: Manual trigger**
1. Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines/new
2. Select branch: `main`
3. Click "Run pipeline"

**Option C: Use the tag**
```bash
cd /home/jbyrd/TAMINATOR
git push origin v2.1.2
```

---

## ✅ Verification

After enabling CI/CD, you should see:

1. **Pipelines page accessible:**
   ```
   https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines
   ```

2. **CI/CD menu in left sidebar:**
   - Pipelines
   - Jobs
   - Schedules
   - etc.

3. **Pipeline badge on README** (optional)

4. **Automatic pipeline on next push**

---

## 🐛 If Still Not Working

### Check 1: .gitlab-ci.yml Location
```bash
cd /home/jbyrd/TAMINATOR
ls -la .gitlab-ci.yml
# Should exist in root directory
```

### Check 2: Validate YAML Syntax
```bash
cd /home/jbyrd/TAMINATOR

# Check if it's valid YAML
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml'))"
# Should print nothing if valid
```

### Check 3: GitLab CI Lint
Visit:
```
https://gitlab.cee.redhat.com/jbyrd/taminator/-/ci/lint
```
Paste the contents of `.gitlab-ci.yml` and click "Validate"

### Check 4: Project Permissions
Make sure you have:
- Maintainer or Owner role on the project
- Permissions to enable CI/CD
- Access to shared runners

---

## 📊 Common Issues

### Issue: "No runners available"
**Solution:** Enable shared runners in project settings

### Issue: ".gitlab-ci.yml not found"
**Solution:** Make sure it's in the root directory and pushed to GitLab

### Issue: "Pipeline is disabled"
**Solution:** Enable CI/CD in project features

### Issue: "YAML syntax error"
**Solution:** Validate at https://gitlab.cee.redhat.com/jbyrd/taminator/-/ci/lint

---

## 🚀 Once Enabled

Pipeline will automatically run on:
- Every push to `main` branch (lint, test, docs)
- Every tag push (lint, test, build, release)
- Manual triggers

**Expected first run:** 5-7 minutes for lint/test stages

---

**Created:** November 14, 2025  
**Status:** Waiting for CI/CD to be enabled  
**Next:** Follow steps above, then push or manually trigger

