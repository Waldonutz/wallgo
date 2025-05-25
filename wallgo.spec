# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['wallgo.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

# Add game_logic.py and renderer.py to the data files
a.datas += [('game_logic.py', 'game_logic.py', 'DATA')]
a.datas += [('renderer.py', 'renderer.py', 'DATA')]

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='WallGo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='NONE',
)

app = BUNDLE(
    exe,
    name='WallGo.app',
    icon=None,
    bundle_identifier=None,
)
