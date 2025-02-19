import os
import zipfile
import shutil
import time

def zip_directory(directory, zip_name, compress_level=9):
    # 使用临时文件
    temp_zip = "temp_archive.zip"
    with zipfile.ZipFile(temp_zip, "w", compresslevel=compress_level) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # 将文件添加到 ZIP 中，并保留相对路径
                zipf.write(file_path, os.path.relpath(file_path, directory))
    # 将临时文件移动到目标位置
    shutil.move(temp_zip, zip_name)


if __name__ == '__main__':
    # Get the current version from the VERSION file
    with open('VERSION', 'r') as f:
        version = f.read().strip()
    # Create a new directory for the release
    os.makedirs(f'releases/{version}', exist_ok=True)

    shutil.rmtree("dist")

    exit_code = os.system("pyinstaller main.spec")
    exit_code = 0
    if exit_code == 0:
        # Copy the compiled executable to the release directory
        os.system("copy dist\\main.exe releases\\{}\\main.exe".format(version))
        os.makedirs('releases/{}/resources'.format(version), exist_ok=True)
        os.system("xcopy resources\\ releases\\{}\\resources\\".format(version))
        version_str = version.replace(".", "_")
        print("开始压缩")
        zip_directory('releases\\{}'.format(version), 'releases/{}/archives/screen_searcher_v_{}_portable.zip'.format(version,version_str))
        # Copy the README.md file to the release directory
        os.system("copy README.md releases\\{}\\README.md".format(version))
        print("Release {} created successfully.".format(version))