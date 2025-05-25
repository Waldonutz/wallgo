# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

# Get the current directory
current_dir = os.path.dirname(os.path.abspath('__file__'))
parent_dir = os.path.dirname(current_dir)

a = Analysis(
    [os.path.join(parent_dir, 'wallgo.py')],
    pathex=[parent_dir],
    binaries=[],
    datas=[
        (os.path.join(parent_dir, 'game_logic.py'), '.'),
        (os.path.join(parent_dir, 'renderer.py'), '.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WallGo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WallGo',
)

app = BUNDLE(
    coll,
    name='WallGo.app',
    icon=None,
    bundle_identifier='com.wallgo.game',
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': 'True'
    },
)
