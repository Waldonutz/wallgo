# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

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
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add game_logic.py and renderer.py to the data files
a.datas += [('game_logic.py', 'game_logic.py', 'DATA')]
a.datas += [('renderer.py', 'renderer.py', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Mac executable
exe_mac = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
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
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Mac app bundle
app = BUNDLE(
    exe_mac,
    name='WallGo.app',
    icon=None,
    bundle_identifier=None,
)

# Windows executable
exe_win = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
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
    target_arch=None,
)
