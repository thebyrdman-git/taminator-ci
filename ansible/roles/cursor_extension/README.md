# Cursor Extension Role

**Builds Taminator Intelligence Cursor IDE extension from Ansible templates**

## Purpose

Generate, build, and package the Cursor IDE extension entirely from Ansible.
No manual code creation - everything is templated and version-controlled.

## Structure

```
cursor_extension/
├── defaults/main.yml       # Extension configuration
├── tasks/main.yml          # Build pipeline
├── templates/              # All source code templates
│   ├── package.json.j2
│   ├── tsconfig.json.j2
│   ├── extension.ts.j2
│   ├── api/
│   ├── commands/
│   └── sidebar/
├── files/                  # Static assets
│   └── icon.png
└── meta/main.yml          # Role metadata
```

## Usage

```bash
# Build extension
ansible-playbook ansible/playbooks/build-cursor-extension.yml

# Build and package
ansible-playbook ansible/playbooks/build-cursor-extension.yml -e package_extension=true

# Build with tests
ansible-playbook ansible/playbooks/build-cursor-extension.yml -e run_tests=true

# Force reinstall dependencies
ansible-playbook ansible/playbooks/build-cursor-extension.yml -e force_install=true
```

## Variables

See `defaults/main.yml` for all configurable options.

Key variables:
- `extension_version`: Version number
- `extension_name`: Package name
- `compile_on_build`: Compile TypeScript (default: true)
- `package_extension`: Create VSIX (default: true)
- `run_tests`: Run test suite (default: false)

## Output

- Source: `cursor-extension/src/`
- Compiled: `cursor-extension/out/`
- Package: `cursor-extension/*.vsix`
- Release: `release/v{{ extension_version }}/cursor-extension/`

## Pipeline

1. Create directory structure
2. Template all source files from Jinja2
3. Install npm dependencies
4. Compile TypeScript
5. Run tests (optional)
6. Package VSIX
7. Copy to release directory
8. Generate checksums

## Benefits

✅ Version controlled configuration
✅ Repeatable builds
✅ No manual file editing
✅ Consistent with other Taminator features
✅ Easy to update (change variables, re-run)
✅ Auditable (all changes in git)

