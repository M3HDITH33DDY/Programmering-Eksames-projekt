# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=['.venv/Lib/site-packages/PySide6'],
    binaries=[],
    datas=[
        ('IMV/screens/enthalpy_data.json', 'IMV/screens'),           # JSON file for EnthalpyScreen
        ('IMV/images/*.png', 'IMV/images'),                         # Image files for HomeScreen
        ('IMV/screens/PDF-Filer/*', 'IMV/screens/PDF-Filer'),       # PDF files and directory for PDFViewerScreen
        ('.venv/Lib/site-packages/PySide6/plugins', 'PySide6/plugins'),  # PySide6 plugins
    ],
    hiddenimports=['PySide6.QtGui', 'PySide6.QtWidgets', 'PySide6.QtCore', 'PySide6.QtWebEngineWidgets', 'PySide6.QtWebEngineCore'],
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
    name='IMV',
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
)