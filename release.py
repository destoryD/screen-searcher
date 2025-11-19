import os
import zipfile
import shutil
import time
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_build_version():
    """
    获取构建版本号
    优先级:
    1. 环境变量 BUILD_VERSION (由 GitHub Actions 传入)
    2. 本地 VERSION 文件 (本地开发回退)
    """
    # 1. 尝试读取环境变量
    env_version = os.getenv('BUILD_VERSION')
    if env_version:
        logging.info(f"从环境变量检测到版本号: {env_version}")
        return env_version

    # 2. 回退读取本地文件
    if os.path.exists('VERSION'):
        with open('VERSION', 'r') as f:
            file_version = f.read().strip()
        logging.info(f"从 VERSION 文件读取版本号: {file_version}")
        return file_version
        
    raise ValueError("无法确定版本号: 既没有 BUILD_VERSION 环境变量，也没有 VERSION 文件")

def setup_release_dirs(version):
    """创建发布相关目录"""
    release_dir = Path(f'releases/{version}')
    archive_dir = release_dir / 'archives'
    resource_dir = release_dir / 'resources'
    
    # 如果目录已存在，先清空它们
    if release_dir.exists():
        logging.info(f"清空已存在的发布目录: {release_dir}")
        shutil.rmtree(release_dir)
    
    for dir_path in [release_dir, archive_dir, resource_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return release_dir, archive_dir, resource_dir

def zip_directory(directory, zip_name, compress_level=9):
    """压缩目录为zip文件"""
    try:
        temp_zip = "temp_archive.zip"
        with zipfile.ZipFile(temp_zip, "w", compresslevel=compress_level) as zipf:
            directory_path = Path(directory)
            for file_path in directory_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(directory_path)
                    zipf.write(file_path, arcname)
        shutil.move(temp_zip, zip_name)
        logging.info(f"成功创建压缩包: {zip_name}")
    except Exception as e:
        logging.error(f"压缩过程出错: {str(e)}")
        raise

def clean_build_artifacts():
    """清理构建产物"""
    dirs_to_clean = ['dist', 'build']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            logging.info(f"清理目录: {dir_name}")

def check_required_files():
    """检查必需文件是否存在"""
    # 注意：这里移除了 'VERSION'，因为如果用环境变量构建，本地不一定非要有 VERSION 文件
    required_files = ['main.spec', 'README.md']
    for file in required_files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"缺少必需文件: {file}")

def create_release():
    try:
        # 检查必需文件 (main.spec, README.md)
        check_required_files()
        
        # 获取版本号 (优先 Env，其次 File)
        version = get_build_version()
        
        # 清理旧的构建文件
        clean_build_artifacts()
        
        # 创建目录结构
        release_dir, archive_dir, resource_dir = setup_release_dirs(version)
        
        # 构建可执行文件
        logging.info(f"开始构建版本 {version} 的可执行文件...")
        # 如果需要将版本号传入 PyInstaller，可以在这里修改命令，例如:
        # os.system(f"pyinstaller main.spec --name screen-searcher-v{version}")
        exit_code = os.system("pyinstaller main.spec")
        
        if exit_code != 0:
            raise RuntimeError("PyInstaller 构建失败")
        
        # 检查生成的文件是否存在
        exe_path = Path('dist/screen-searcher.exe')
        if not exe_path.exists():
             # 尝试找找看有没有带 .exe 后缀的文件 (防止 spec 文件里改了名字)
             exes = list(Path('dist').glob('*.exe'))
             if exes:
                 exe_path = exes[0]
                 logging.warning(f"未找到 screen-searcher.exe，但找到了 {exe_path.name}，将使用它。")
             else:
                 raise FileNotFoundError("dist 目录下未找到 .exe 文件")

        # 复制文件
        shutil.copy2(exe_path, release_dir / 'screen-searcher.exe')
        
        if os.path.exists('resources'):
            shutil.copytree('resources', resource_dir, dirs_exist_ok=True)
        else:
            logging.warning("未找到 resources 目录，跳过资源复制")
            
        if os.path.exists('README.md'):
            shutil.copy2('README.md', release_dir / 'README.md')
        
        # 创建便携版压缩包
        version_str = version.replace(".", "_")
        zip_path = archive_dir / f'screen_searcher_v_{version_str}_portable.zip'
        logging.info("开始创建便携版压缩包...")
        zip_directory(release_dir, zip_path)
        
        logging.info(f"Release {version} 创建成功!")
        logging.info(f"文件位置: {zip_path}")
        
    except Exception as e:
        logging.error(f"发布过程失败: {str(e)}")
        # 抛出异常以确保 GitHub Action 能够捕获到失败状态
        raise

if __name__ == '__main__':
    create_release()