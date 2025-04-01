# -*- mode: python -*-

import os
import platform
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

try:
    this_dir = os.path.abspath(os.path.dirname(__file__))
except NameError:
    this_dir = os.getcwd()

datas = [
    (os.path.join(this_dir, '..', 'frontend', 'build'), os.path.join('frontend', 'build')),
    (os.path.join(this_dir, 'recipes'), 'recipes'),
    (os.path.join(this_dir, 'instance'), 'instance')
]

hiddenimports = []
hiddenimports += collect_submodules('flask')
hiddenimports += collect_submodules('routes')
hiddenimports += collect_submodules('models')

a = Analysis(
    ['app.py'],
    pathex=[this_dir],
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

if platform.system() == "Darwin":
    exe_name = 'hypixel_dwarven_forge-v1.1.2-macos'
elif platform.system() == "Linux":
    exe_name = 'hypixel_dwarven_forge-v1.1.2-linux'
else:
    exe_name = 'hypixel_dwarven_forge-v1.1.2-win'

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
)

if platform.system() == "Darwin":
    app = BUNDLE(
        exe,
        name='hypixel_dwarven_forge-v1.1.2.app',
        icon=None,
        bundle_identifier=None,
    )