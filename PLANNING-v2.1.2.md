# TAMINATOR v2.1.2 - Planning Document

**Target Release:** December 2025  
**Type:** Quality & Testing Improvements  
**Status:** Planning Phase

---

## 🎯 Goals

### Primary Goals
1. **Reduce ESLint warnings** from 61 to < 10
2. **Add unit tests** for critical components
3. **Enable GitLab CI/CD** for automated builds
4. **Build new binaries** with all v2.1.1 improvements

### Secondary Goals
5. **Performance optimizations** based on profiling
6. **Integration tests** for key workflows
7. **Documentation updates** for new features

---

## 📊 Current State (v2.1.1)

**Code Quality:**
- ✅ 0 errors
- ⚠️ 61 warnings (target: < 10)
- ✅ ESLint configured
- ✅ Pre-commit hooks active

**Testing:**
- ❌ 0% test coverage (target: 30%+)
- ❌ No unit tests
- ❌ No integration tests

**CI/CD:**
- ⚠️ GitLab CI/CD not enabled
- ⚠️ .gitlab-ci.yml only has docs deployment
- ⚠️ No automated builds

**Binaries:**
- ⚠️ Last build: v2.0.1
- ⚠️ v2.1.1 improvements not in binaries

---

## 📋 Task Breakdown

### Phase 1: Fix ESLint Warnings (Week 1)

**Target:** Reduce from 61 to < 10 warnings

**Current warnings breakdown:**
```bash
cd /home/jbyrd/TAMINATOR/gui
npm run lint 2>&1 | grep "warning" | wc -l
# Result: 61 warnings
```

**Types of warnings:**
1. `require-await` - Async functions without await (~30 warnings)
2. `no-unused-vars` - Unused variables (~15 warnings)
3. Other misc warnings (~16 warnings)

**Action items:**
- [ ] Run lint and categorize all 61 warnings
- [ ] Fix or suppress intentional async functions
- [ ] Remove genuinely unused variables
- [ ] Review and fix remaining warnings
- [ ] Update ESLint rules if needed

**Estimated time:** 4-6 hours

---

### Phase 2: Set Up Testing (Week 1-2)

**Target:** 30% test coverage on critical components

#### Step 1: Install Jest
```bash
cd /home/jbyrd/TAMINATOR/gui
npm install --save-dev jest @types/jest
```

#### Step 2: Configure Jest
Create `gui/jest.config.js`:
```javascript
module.exports = {
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'public/js/**/*.js',
    '!public/js/**/*.test.js',
  ],
  testMatch: [
    '**/__tests__/**/*.js',
    '**/*.test.js',
  ],
};
```

#### Step 3: Write Tests for Critical Components

**Priority 1: Intelligence Client**
- File: `public/js/intelligence-client.js`
- Tests: API calls, error handling, response parsing
- Target: 50% coverage

**Priority 2: Error Handler**
- File: `public/js/error-handler.js`
- Tests: Error display, toast notifications, cleanup
- Target: 60% coverage

**Priority 3: Service Base**
- File: `public/js/service-base.js`
- Tests: API wrapper, error handling, retries
- Target: 40% coverage

**Priority 4: API Client**
- File: `api-client.js`
- Tests: Request formatting, response handling
- Target: 40% coverage

**Estimated time:** 8-12 hours

---

### Phase 3: Enable GitLab CI/CD (Week 2)

#### Step 1: Enable in GitLab Settings
1. Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/settings/ci_cd
2. Expand "General pipelines"
3. Enable CI/CD
4. Enable shared runners or configure MiracleMax

#### Step 2: Update .gitlab-ci.yml

Add build stages:
```yaml
stages:
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "18"

# Keep existing test_docs job

# Add: Run tests
test_unit:
  stage: test
  image: node:${NODE_VERSION}
  script:
    - cd gui
    - npm ci
    - npm run lint
    - npm test
  artifacts:
    reports:
      junit: gui/junit.xml
      coverage_report:
        coverage_format: cobertura
        path: gui/coverage/cobertura-coverage.xml

# Add: Build AppImage
build_appimage_x64:
  stage: build
  tags:
    - miraclemax
  script:
    - cd gui
    - npm ci
    - npm run build:linux
  artifacts:
    paths:
      - gui/dist/*.AppImage
    expire_in: 1 week
  only:
    - tags

# Add: Create release
create_release:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/release-cli:latest
  script:
    - echo "Creating release for ${CI_COMMIT_TAG}"
  release:
    tag_name: ${CI_COMMIT_TAG}
    description: './RELEASE-NOTES-${CI_COMMIT_TAG}.md'
    assets:
      links:
        - name: 'AppImage (x86_64)'
          url: '${CI_PROJECT_URL}/-/jobs/artifacts/${CI_COMMIT_TAG}/raw/gui/dist/TAMINATOR-${CI_COMMIT_TAG}.AppImage?job=build_appimage_x64'
  only:
    - tags
```

#### Step 3: Test Pipeline
```bash
# Trigger test pipeline
git commit --allow-empty -m "test: Trigger CI/CD pipeline"
git push origin main
```

**Estimated time:** 4-6 hours

---

### Phase 4: Build Binaries (Week 3)

#### Update Electron Builder Configuration

**Verify `gui/package.json` build section:**
```json
{
  "build": {
    "appId": "com.redhat.taminator",
    "productName": "TAMINATOR",
    "files": [
      "public/**/*",
      "main.js",
      "service-manager.js",
      "api-client.js",
      "package.json"
    ],
    "linux": {
      "target": ["AppImage"],
      "category": "Development"
    },
    "mac": {
      "target": ["dmg"],
      "category": "public.app-category.developer-tools"
    },
    "win": {
      "target": ["nsis"]
    }
  }
}
```

#### Build Locally for Testing
```bash
cd /home/jbyrd/TAMINATOR/gui

# Linux AppImage
npm run build:linux

# Test the AppImage
chmod +x dist/TAMINATOR-*.AppImage
./dist/TAMINATOR-*.AppImage
```

#### Automate with Ansible
```bash
cd /home/jbyrd/TAMINATOR

# Update version in playbook
sed -i 's/version: "2.1.1"/version: "2.1.2"/' ansible/01-build-appimage.yml

# Build with Ansible
ansible-playbook ansible/01-build-appimage.yml
```

**Estimated time:** 2-4 hours

---

### Phase 5: Release Preparation (Week 3)

#### Update Version Numbers
```bash
# Update package.json
cd /home/jbyrd/TAMINATOR/gui
npm version 2.1.2

# Update README.md
sed -i 's/2.1.1/2.1.2/g' ../README.md
```

#### Update CHANGELOG.md
Add v2.1.2 entry:
```markdown
## [2.1.2] - 2025-12-XX

### 🧪 Testing & Quality Release

### Added
- Jest testing framework
- Unit tests for critical components (30% coverage)
- GitLab CI/CD automated builds
- Integration tests for key workflows

### Fixed
- Reduced ESLint warnings from 61 to < 10
- Fixed async function patterns
- Cleaned up unused variables
- Performance optimizations

### Changed
- Automated build pipeline
- New binaries with all v2.1.1 improvements

### Developer Experience
- Tests run on every commit
- CI/CD builds on every tag
- Test coverage reporting
```

#### Create Release Notes
```bash
# Create RELEASE-NOTES-v2.1.2.md
# Similar structure to v2.1.1
```

#### Tag and Release
```bash
# Create tag
git tag -a v2.1.2 -m "Release v2.1.2 - Testing & CI/CD"

# Push to GitLab
git push origin main
git push origin v2.1.2

# CI/CD will automatically:
# - Run tests
# - Build AppImage
# - Create GitLab release
```

**Estimated time:** 2-3 hours

---

## 📈 Success Metrics

### Code Quality
- ✅ ESLint warnings: 61 → < 10 (85% reduction)
- ✅ ESLint errors: 0 (maintained)
- ✅ All tests passing

### Testing
- ✅ Test coverage: 0% → 30%+
- ✅ Critical components tested
- ✅ CI/CD running tests automatically

### Automation
- ✅ GitLab CI/CD enabled
- ✅ Automated builds on tags
- ✅ Automated releases

### Binaries
- ✅ New AppImage with v2.1.1 + v2.1.2 improvements
- ✅ Available for download on GitLab

---

## ⏰ Timeline

**Week 1:**
- Days 1-2: Fix ESLint warnings
- Days 3-5: Set up Jest and write initial tests

**Week 2:**
- Days 1-2: Continue test writing
- Days 3-4: Enable GitLab CI/CD
- Day 5: Test pipeline

**Week 3:**
- Days 1-2: Build binaries and test
- Days 3-4: Release preparation
- Day 5: Release v2.1.2

**Total:** ~3 weeks of part-time work

---

## 🎯 Priority Order

### Must Have (P0)
1. Reduce ESLint warnings to < 10
2. Set up Jest framework
3. Write tests for intelligence-client.js
4. Enable GitLab CI/CD
5. Build new AppImage

### Should Have (P1)
6. Write tests for error-handler.js
7. Write tests for service-base.js
8. Add integration tests
9. Set up coverage reporting

### Nice to Have (P2)
10. Performance profiling
11. Memory leak testing
12. Load testing
13. Documentation updates

---

## 🚀 Getting Started

### Today (Immediate)
1. Run ESLint and catalog all 61 warnings
2. Categorize warnings by type
3. Create fix plan for each category
4. Start fixing `require-await` warnings

### This Week
1. Fix all ESLint warnings
2. Install Jest
3. Write first test suite

### Next Week
1. Continue testing
2. Enable CI/CD
3. Test pipeline

---

## 📊 Tracking Progress

### Dashboard
Create `PROGRESS-v2.1.2.md` to track:
- [ ] ESLint warnings fixed: 0/61
- [ ] Tests written: 0/X
- [ ] Test coverage: 0%
- [ ] CI/CD enabled: No
- [ ] Binaries built: No

Update daily during development.

---

## 🔗 Resources

**Documentation:**
- Jest: https://jestjs.io/docs/getting-started
- GitLab CI/CD: https://docs.gitlab.com/ee/ci/
- Electron Builder: https://www.electron.build/

**Internal:**
- ESLint config: `gui/.eslintrc.js`
- Current warnings: Run `npm run lint` in gui/
- GitLab settings: https://gitlab.cee.redhat.com/jbyrd/taminator/-/settings/ci_cd

---

## ✅ Definition of Done

**v2.1.2 is complete when:**
- [ ] ESLint warnings < 10
- [ ] Test coverage ≥ 30%
- [ ] GitLab CI/CD passing
- [ ] New AppImage built and tested
- [ ] GitLab release created
- [ ] Documentation updated
- [ ] Binaries available for download

---

**Created:** November 11, 2025  
**Target Release:** December 2025  
**Status:** Ready to Start

🚀 **Let's build v2.1.2!**




