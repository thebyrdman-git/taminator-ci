# Enable GitLab CI/CD for TAMINATOR

**Quick guide to enable CI/CD pipelines**

---

## Issue

GitLab CI/CD shows: "Pipeline cannot be run. Missing CI config file"

**Cause:** CI/CD is not enabled for the project.

---

## Solution

### Step 1: Enable CI/CD in Project Settings

1. Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/settings/ci_cd
2. Expand "General pipelines"
3. Check if CI/CD is disabled
4. If disabled, enable it

### Step 2: Enable Shared Runners

1. In same page, expand "Runners"
2. Enable "Shared runners"
3. Look for available Red Hat runners

### Step 3: Verify Configuration

1. Check `.gitlab-ci.yml` exists at project root:
   ```bash
   ls -la /home/jbyrd/TAMINATOR/.gitlab-ci.yml
   ```

2. Validate YAML syntax:
   ```bash
   cd /home/jbyrd/TAMINATOR
   python3 -c "import yaml; print('Valid!' if yaml.safe_load(open('.gitlab-ci.yml')) else 'Invalid')"
   ```

### Step 4: Test Pipeline

1. Make a small change and push:
   ```bash
   cd /home/jbyrd/TAMINATOR
   git commit --allow-empty -m "test: Trigger CI/CD pipeline"
   git push origin main
   ```

2. Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/pipelines
3. Should see pipeline running

---

## Current .gitlab-ci.yml

The file is configured for:
- **Documentation deployment** to GitHub Pages
- **Python 3.11** image
- **MkDocs Material** for docs

```yaml
stages:
  - test
  - deploy

test_docs:
  stage: test
  script:
    - mkdocs build
  except:
    - main

deploy_github_pages:
  stage: deploy
  script:
    - mkdocs build
    - git config --global user.email "ci@taminator.dev"
    - git config --global user.name "Taminator CI"
    - git remote add github-deploy https://${GITHUB_TOKEN}@github.com/thebyrdman-git/taminator.git
    - mkdocs gh-deploy --force --remote-name github-deploy --remote-branch gh-pages
  only:
    - main
```

**Note:** Requires `GITHUB_TOKEN` variable in GitLab CI/CD settings.

---

## Alternative: Manual Deployment

If CI/CD continues to have issues, deploy manually:

```bash
cd /home/jbyrd/TAMINATOR
mkdocs gh-deploy --force --remote-name github --remote-branch gh-pages
```

---

## Resources

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Red Hat GitLab Support](https://red.ht/gitlab-support)

---

**Last Updated:** November 11, 2025

