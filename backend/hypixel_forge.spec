# -*- mode: python -*-

import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

try:
    this_dir = os.path.abspath(os.path.dirname(__file__))
except NameError:
    this_dir = os.getcwd()

datas = [
    (os.path.join(this_dir, '..', 'frontend', 'build'), 'frontend/build'),
    (os.path.join(this_dir, 'recipes'), 'recipes'),
    (os.path.join(this_dir, 'instance'), 'instance')
]

hiddenimports = []
hiddenimports += collect_submodules('flask')
hiddenimports += collect_submodules('routes')
hiddenimports += collect_submodules('models')

a = Analysis(
    ['app.py'],  # Main Flask file
    pathex=[this_dir],  # ensures PyInstaller can locate your current directory
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
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
    name='hypixel_dwarven_forge-v1.1.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX
    console=True,
)