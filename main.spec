# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=['.venv/Lib/site-packages/PySide6'],
    binaries=[],
    datas=[
        ('IMV/screens/enthalpy_data.json', 'IMV/screens'),
        ('IMV/images/*.png', 'IMV/images'),
        ('.venv/Lib/site-packages/PySide6/plugins', 'PySide6/plugins'),
    ],
    hiddenimports=['PySide6.QtGui', 'PySide6.QtWidgets', 'PySide6.QtCore'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Change to False for final build
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)