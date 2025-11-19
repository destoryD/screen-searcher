# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path

block_cipher = None

# --- 1. 路径优化：使用动态路径 ---
# 获取项目根目录，确保在不同环境下（本地/CI）路径都能正确解析
# 假设 spec 文件在项目根目录下
root_dir = Path(os.getcwd())
src_dir = root_dir / 'src'
res_dir = root_dir / 'resources'
icon_path = res_dir / 'logo.ico'

a = Analysis(
    [str(src_dir / 'main.py')],
    pathex=[str(src_dir)],
    binaries=[],
    datas=[],
    # --- 2. 隐式导入检查 ---
    # 如果你的代码用了 pynput, keyboard, PIL 等库，有时需要手动添加
    hiddenimports=[], 
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # --- 3. 排除不必要的库 (减小体积) ---
    # 保留了你原有的列表，并添加了一些常见的无关标准库
    excludes=[
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6', 
        'torch', 'tensorflow', 
        'cryptography', 
        'pyarrow', 
        'pandas', 'numpy', 'matplotlib', 'scipy',
        'setuptools', 'distutils',
        'jedi',   # 代码补全库，运行不需要
        'pydoc',  # 文档生成
        'unittest', 'pdb', 'difflib', 'doctest', # 测试与调试库
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='screen-searcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True, 
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # GUI 程序不显示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # 确保图标路径存在，否则会报错或使用默认图标
    icon=str(icon_path) if icon_path.exists() else None 
)