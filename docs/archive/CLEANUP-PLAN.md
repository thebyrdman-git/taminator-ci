# Taminator Directory Cleanup Plan

## Current Issues
- 80+ markdown files in root directory
- Build scripts scattered in root
- Test scripts in root
- Session summaries cluttering root
- No organized release directory

## Cleanup Strategy

### 1. Archive old session summaries
Move to: docs/archive/sessions/
- *-SUMMARY.md
- *-HANDOFF-*.md
- SESSION-*.md
- TONIGHTS-WORK-SUMMARY.md

### 2. Archive old version docs
Move to: docs/archive/v1.x/
- V1.10.1-*.md
- RELEASE-NOTES-v1.*.md
- DEPLOYMENT-READY-v1.*.md
- README-v1.x-old.md

### 3. Consolidate build scripts
Move to: build/scripts/
- build-*.sh
- build-*.spec
- *.spec files

### 4. Consolidate test scripts
Move to: tests/integration/
- test-*.sh
- test-*.py

### 5. Archive completed feature docs
Move to: docs/archive/features/
- *-COMPLETE.md
- *-INTEGRATION-COMPLETE.md
- FEATURE-*.md

### 6. Keep in root (essential only)
- README.md
- CHANGELOG.md
- LICENSE
- .gitignore
- .gitlab-ci.yml
- Containerfile
- docker-compose.yml
- execution-environment.yml
- requirements.txt
- CONTRIBUTING.md

### 7. Create release/ directory structure
release/
├── v2.0.0/
│   ├── linux/
│   │   ├── x86_64/
│   │   │   ├── Taminator-2.0.0.AppImage
│   │   │   └── taminator-gui_2.0.0_amd64.deb
│   │   └── arm64/
│   ├── windows/
│   └── macos/
├── checksums/
│   └── v2.0.0-checksums.txt
└── README.md

