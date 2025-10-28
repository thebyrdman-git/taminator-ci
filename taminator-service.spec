# -*- mode: python ; coding: utf-8 -*-
# Taminator Service PyInstaller Spec
# Custom spec to exclude system libraries that cause glibc issues

block_cipher = None

a = Analysis(
    ['src/taminator/cli_service.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'taminator.api.main',
        'taminator.api.routes.health',
        'taminator.api.routes.customers',
        'taminator.api.routes.jira',
        'taminator.api.routes.portal',
        'taminator.api.routes.logs',
        'taminator.api.routes.rhcase',
        'taminator.api.routes.debug',
        'taminator.api.routes.diagnostics',
        'taminator.core.exceptions',
        'taminator.core.logging_config',
        'taminator.services.customer_service',
        'taminator.services.jira_service',
        'taminator.services.portal_service',
        'taminator.services.rhcase_service',
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# CRITICAL: Exclude ONLY system .so libraries that cause glibc issues
# Python packages (.pyc, .py) should still be bundled
# System libraries will be loaded from the system at runtime
exclude_libs = ['libz.so', 'libc.so', 'libpthread.so', 'libm.so', 'libdl.so', 'librt.so', 'libcrypt.so']
a.binaries = [x for x in a.binaries if not any(lib in x[0] for lib in exclude_libs)]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='taminator-service',
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
