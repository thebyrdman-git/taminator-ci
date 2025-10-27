# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Taminator CLI
Bundles tam-rfe with all Python dependencies into a standalone executable
"""

import sys
from pathlib import Path

block_cipher = None

# Get the source directory
src_path = Path('src').absolute()

a = Analysis(
    ['src/taminator/cli.py'],
    pathex=[str(src_path)],
    binaries=[],
    datas=[
        # Include templates if they exist
        ('src/templates', 'templates'),
    ],
    hiddenimports=[
        'rich',
        'rich.console',
        'rich.table',
        'rich.panel',
        'rich.prompt',
        'rich.progress',
        'rich.markdown',
        'requests',
        'jinja2',
        'yaml',
        'cryptography',
        # Include all taminator modules
        'taminator',
        'taminator.cli',
        'taminator.commands',
        'taminator.commands.check',
        'taminator.commands.update',
        'taminator.commands.post',
        'taminator.commands.onboard',
        'taminator.commands.config',
        'taminator.commands.dashboard',
        'taminator.commands.report_issue',
        'taminator.core',
        'taminator.core.auth_box',
        'taminator.core.auth_types',
        'taminator.core.auth_audit',
        'taminator.core.hybrid_auth',
        'taminator.core.vault_client',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pytest',
        'pytest-cov',
        'pytest-mock',
        'black',
        'flake8',
        'mypy',
        'IPython',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='tam-rfe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

