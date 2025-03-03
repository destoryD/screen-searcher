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
    required_files = ['main.spec', 'README.md', 'VERSION']
    for file in required_files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"缺少必需文件: {file}")

def create_release():
    try:
        # 检查必需文件
        check_required_files()
        
        # 读取版本号
        with open('VERSION', 'r') as f:
            version = f.read().strip()
        
        # 清理旧的构建文件
        clean_build_artifacts()
        
        # 创建目录结构
        release_dir, archive_dir, resource_dir = setup_release_dirs(version)
        
        # 构建可执行文件
        logging.info("开始构建可执行文件...")
        exit_code = os.system("pyinstaller main.spec")
        if exit_code != 0:
            raise RuntimeError("PyInstaller 构建失败")
        
        # 复制文件
        shutil.copy2('dist/screen-searcher.exe', release_dir / 'screen-searcher.exe')
        shutil.copytree('resources', resource_dir, dirs_exist_ok=True)
        shutil.copy2('README.md', release_dir / 'README.md')
        
        # 创建便携版压缩包
        version_str = version.replace(".", "_")
        zip_path = archive_dir / f'screen_searcher_v_{version_str}_portable.zip'
        logging.info("开始创建便携版压缩包...")
        zip_directory(release_dir, zip_path)
        
        logging.info(f"Release {version} 创建成功!")
        
    except Exception as e:
        logging.error(f"发布过程失败: {str(e)}")
        raise

if __name__ == '__main__':
    create_release()