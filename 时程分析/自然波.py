import os
import shutil


def copy_and_rename_txt_files(source_dir, destination_dir):
    # 检查目标文件夹是否存在，不存在则创建
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # 遍历source_dir中的所有文件
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # 检查文件扩展名是否为 .txt
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                new_file_name = rename_with_prefix(file, os.path.basename(os.path.dirname(file_path)))  # 调用重命名函数
                destination_path = os.path.join(destination_dir, new_file_name)
                new_file_name = os.path.splitext(destination_path)[0] + '.dat'
                shutil.copy(file_path, new_file_name)
                print(f"Copied and renamed: {file_path} to {destination_path}")


# 定义重命名规则函数，示例：在文件名前添加前缀
def rename_with_prefix(file_name, prefix):
    # prefix = "new_"  # 自定义前缀
    return prefix + file_name


# 你也可以自定义其他重命名逻辑，如添加后缀或更改文件名
def rename_with_suffix(file_name):
    suffix = "_backup"  # 自定义后缀
    name, ext = os.path.splitext(file_name)
    return name + suffix + ext


if __name__ == '__main__':
    # 指定源文件夹和目标文件夹
    source_directory = './NP22.080.019 Ground Motion Data R0 2023.03.16/02 Time-Histories/01 Davao and Offshore/03 1,000-Year'
    destination_directory = './out/Dav_1000'

    copy_and_rename_txt_files(source_directory, destination_directory)  # 使用前缀重命名
    # 或者使用
