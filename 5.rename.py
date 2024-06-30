import os

def rename_files_in_directory(directory):
    """
    更灵活地重命名目录中的文件，移除文件名分割后的第三部分。
    """
    for filename in os.listdir(directory):
        # 分割文件名
        parts = filename.split('_')
        # 移除第三部分
        if len(parts) > 3:  # 确保文件名有足够的部分可以移除
            new_parts = parts[:2] + parts[3:]  # 移除第三部分
            new_filename = '_'.join(new_parts)
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)
            
            # 重命名文件
            os.rename(old_file_path, new_file_path)
            print(f"重命名文件：{filename} -> {new_filename}")

# 定义需要处理的文件夹路径
directories = [
    "Sen1Floods_256/Labels",
    "Sen1Floods_256/VH",
    # "Sen1Floods_256/VV",
]

# 对每个目录应用重命名函数
for directory in directories:
    rename_files_in_directory(directory)
    print(f"完成重命名在目录：{directory}")