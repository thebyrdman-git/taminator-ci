# 🚀 Getting Started with Taminator v2.0.1

**Welcome!** This guide will help you use the complete Ansai + GitHub CI workflow.

---

## 📋 Quick Start (5 Minutes)

### For Users (Installing Taminator)

```bash
# Download Linux build
wget https://github.com/YOUR-ORG/taminator-ci/releases/download/v2.0.1/Taminator-2.0.1.AppImage

# Make executable and run
chmod +x Taminator-2.0.1.AppImage
./Taminator-2.0.1.AppImage
```

**macOS Users**: Download the DMG, right-click → Open

---

### For Developers (Contributing)

```bash
# Clone repository
git clone https://github.com/YOUR-ORG/taminator-ci.git
cd taminator-ci

# Use tam-dev tools
./bin/tam-dev health     # Check if service is running
./bin/tam-dev debug      # Interactive debugging
./bin/tam-dev logs       # Watch logs

# Make changes, then verify
ansible-playbook ansible/test-taminator-simple.yml
```

---

## 🛠️ Development Workflow

### 1. Setup Your Environment

```bash
cd /home/jbyrd/TAMINATOR

# Backend (Python)
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Frontend (Node.js)
cd gui
npm install
cd ..
```

### 2. Use tam-dev Tools

```bash
# Interactive menu (15 workflows)
./bin/tam-dev

# Or direct commands:
./bin/tam-dev health       # Quick health check
./bin/tam-dev debug        # IPython with Taminator context
./bin/tam-dev logs         # Tail service logs
./bin/tam-dev test         # Run tests
./bin/tam-dev jira         # Test JIRA connection
./bin/tam-dev ai           # Test AI features
```

### 3. Make Changes

```bash
# Edit code
vim gui/public/js/intelligence-client.js

# Check code quality
cd gui
npx eslint public/js/*.js --fix

# Test locally
npm start
```

### 4. Verify Changes

```bash
# Run Ansible verification
ansible-playbook ansible/test-taminator-simple.yml

# Check ESLint
cd gui && npx eslint public/js/*.js

# Manual testing
./bin/tam-dev debug
```

---

## 📦 Release Workflow

### Full Release Process

```bash
cd /home/jbyrd/TAMINATOR

# 1. Run Ansible release playbook
ansible-playbook ansible/playbooks/taminator-release.yml

# This does:
# ✅ Bumps version (2.0.0 → 2.0.1)
# ✅ Runs ESLint
# ✅ Builds Linux AppImage
# ✅ Generates release notes
# ✅ Creates distribution

# 2. Review what was created
cat RELEASE-NOTES-2.0.1.md
ls -lh releases/v2.0.1/

# 3. Test the build
./releases/v2.0.1/Taminator-2.0.1.AppImage

# 4. Commit and tag
git add gui/package.json RELEASE-NOTES-2.0.1.md
git commit -m "Release v2.0.1 - Hotfix"
git tag -a v2.0.1 -m "Release v2.0.1"

# 5. Push to trigger CI (builds macOS automatically)
git push github main
git push github v2.0.1

# 6. Monitor CI build (~15 minutes)
gh run watch --repo YOUR-ORG/taminator-ci

# 7. Download from GitHub Releases
# https://github.com/YOUR-ORG/taminator-ci/releases
```

---

## 🎯 Common Tasks

### Fix a Bug

```bash
# 1. Identify the issue
./bin/tam-dev errors      # Check error logs
./bin/tam-dev debug       # Interactive debugging

# 2. Fix the code
vim gui/public/js/FILE.js

# 3. Verify fix
npx eslint gui/public/js/FILE.js
ansible-playbook ansible/test-taminator-simple.yml

# 4. Commit
git add gui/public/js/FILE.js
git commit -m "Fix: Description of bug fix"
```

### Add a Feature

```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Develop feature
# ... make changes ...

# 3. Test thoroughly
./bin/tam-dev test
ansible-playbook ansible/test-taminator-simple.yml

# 4. Create PR
git push origin feature/new-feature
gh pr create
```

### Update Dependencies

```bash
# Frontend
cd gui
npm outdated
npm update
npm audit fix

# Backend
source venv/bin/activate
pip list --outdated
pip install --upgrade PACKAGE
```

---

## 📊 Monitoring & Debugging

### Check Service Health

```bash
# Quick check
./bin/tam-dev health

# Full status
curl http://127.0.0.1:8765/health/live | jq

# Watch logs live
./bin/tam-dev logs
```

### Debug Issues

```bash
# Interactive Python debugging
./bin/tam-dev debug

# Then in IPython:
>>> import sys
>>> sys.path.insert(0, '/home/jbyrd/TAMINATOR/src')
>>> from taminator.services.ai_client import AIClient
>>> client = AIClient()
>>> # Test your code
```

### Check for Errors

```bash
# Recent errors
./bin/tam-dev errors

# Service logs
tail -100 ~/.local/state/taminator/log/taminator-service.log

# Search for specific error
grep -i "error" ~/.local/state/taminator/log/*.log
```

---

## 🧪 Testing

### Run All Tests

```bash
# Ansible verification (comprehensive)
ansible-playbook ansible/test-taminator-simple.yml

# Python tests (if available)
source venv/bin/activate
pytest tests/ -v

# JavaScript linting
cd gui
npx eslint public/js/*.js
```

### Manual Testing Checklist

- [ ] Service starts without errors
- [ ] GUI loads correctly
- [ ] Can connect to JIRA
- [ ] AI analysis works
- [ ] Customer data loads
- [ ] Settings save correctly
- [ ] No memory leaks (run for 1 hour)
- [ ] Error handling works

---

## 🐛 Troubleshooting

### Service Won't Start

```bash
# Check if port is in use
lsof -i :8765

# Kill existing process
pkill -f taminator-service

# Check logs
tail -50 ~/.local/state/taminator/log/taminator-service.log

# Restart
cd /home/jbyrd/TAMINATOR
./bin/taminator-service &
```

### GUI Won't Load

```bash
# Check Electron
cd gui
npm start

# Check console for errors (F12)
# Check main.js for issues
tail -50 ~/.config/Electron/logs/main.log
```

### Build Fails

```bash
# Check ESLint
cd gui
npx eslint public/js/*.js

# Check Node version
node --version  # Should be 18+

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### CI Build Fails

```bash
# Check GitHub Actions logs
gh run list --repo YOUR-ORG/taminator-ci
gh run view RUN_ID --log

# Re-run failed job
gh run rerun RUN_ID
```

---

## 📚 Documentation Index

### For Users
- `README.md` - Project overview
- `RELEASE-NOTES-X.Y.Z.md` - What's new

### For Developers
- `GETTING-STARTED.md` - This file
- `DEBUGGING-WITH-ANSAI-TOOLS.md` - Debug guide
- `DEVELOPMENT.md` - Development setup (if exists)

### For Contributors
- `FINAL-RECOMMENDATIONS.md` - Best practices
- `TECHNOLOGY-ASSESSMENT.md` - Technology choices
- `JAVASCRIPT-BUGS-TRACKER.md` - Bug database

### For Maintainers
- `GITHUB-CI-SETUP.md` - CI/CD setup
- `RELEASE-BUILD-INSTRUCTIONS.md` - Build instructions
- `ANSAI-GITHUB-CI-INTEGRATION.md` - Complete workflow

---

## 💡 Tips & Tricks

### Speed Up Development

```bash
# Watch mode for auto-restart
cd gui
npm run dev

# Keep tam-dev logs open in separate terminal
./bin/tam-dev logs

# Use aliases
alias td='cd /home/jbyrd/TAMINATOR && ./bin/tam-dev'
alias ttest='ansible-playbook ansible/test-taminator-simple.yml'
```

### Code Quality

```bash
# Auto-fix on save (add to your editor)
# VSCode: settings.json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}

# Pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
cd gui
npx eslint public/js/*.js || exit 1
EOF
chmod +x .git/hooks/pre-commit
```

### Faster Testing

```bash
# Test only changed files
git diff --name-only | grep '\.js$' | xargs npx eslint

# Quick smoke test
./bin/tam-dev health && echo "✅ Service OK"
```

---

## 🎓 Learning Resources

### Ansai Workflows
- Run `./bin/tam-dev` to see all 15 workflows
- Each workflow is documented with `--help`
- See `ANSAI-DEBUG-SESSION.md` for examples

### Electron Development
- Main process: `gui/main.js`
- Renderer process: `gui/public/js/*.js`
- IPC communication: See `intelligence-client.js`

### FastAPI Backend
- API routes: `src/taminator/api/routes/`
- Services: `src/taminator/services/`
- Database: SQLite in `~/.config/taminator/`

---

## 🚀 Next Steps

### After Setup
1. Run `./bin/tam-dev health` to verify installation
2. Make a small change to test workflow
3. Run `ansible-playbook ansible/test-taminator-simple.yml`
4. Review `FINAL-RECOMMENDATIONS.md` for best practices

### For First Release
1. Follow `GITHUB-CI-SETUP.md` to setup CI/CD
2. Test release process with Ansible
3. Push tag to trigger automated builds
4. Verify all artifacts are created

### For Ongoing Development
1. Use tam-dev tools daily
2. Run tests before committing
3. Keep documentation updated
4. Monitor CI builds

---

## 📞 Getting Help

### Check Documentation
```bash
# List all docs
ls -1 /home/jbyrd/TAMINATOR/*.md

# Search docs
grep -r "keyword" /home/jbyrd/TAMINATOR/*.md
```

### Debug Tools
```bash
./bin/tam-dev debug     # Interactive debugging
./bin/tam-dev errors    # Recent errors
./bin/tam-dev logs      # Live logs
```

### Community
- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions
- Internal Wiki: Team documentation

---

## ✅ Checklist for New Developers

### Initial Setup
- [ ] Clone repository
- [ ] Install Python dependencies
- [ ] Install Node.js dependencies
- [ ] Run `./bin/tam-dev health`
- [ ] Test tam-dev tools
- [ ] Read `DEBUGGING-WITH-ANSAI-TOOLS.md`

### First Contribution
- [ ] Find an issue to work on
- [ ] Create feature branch
- [ ] Make changes
- [ ] Run ESLint
- [ ] Run Ansible tests
- [ ] Create PR
- [ ] Respond to review

### First Release (Maintainers)
- [ ] Setup GitHub CI (see `GITHUB-CI-SETUP.md`)
- [ ] Test release playbook
- [ ] Create test tag
- [ ] Verify CI builds
- [ ] Download and test artifacts
- [ ] Document any issues

---

**Welcome to Taminator development!** 🎉

**Status**: ✅ Ready to use  
**Tools**: ✅ All installed  
**Documentation**: ✅ Comprehensive  
**CI/CD**: ✅ Automated  

**Happy coding!** 💻

