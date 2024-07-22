# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['GUI.py'],
    pathex=[],
    binaries=[('preprocessor.pkl', '.')],
    datas=[('accident_prediction_model.keras', '.'), ('tf_model.py', '.'), ('GUI.ui', '.')],
    hiddenimports=['sklearn.compose', 'PyQt5.QtWebEngineWidgets.QwebEngineView'],
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
    [],
    exclude_binaries=True,
    name='Marine Accident Predictions',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GUI',
)
