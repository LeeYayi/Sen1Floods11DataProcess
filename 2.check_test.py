import os
import rasterio

# 定义VH文件夹路径
vh_dir = 'Sen1Floods/VH'

# 遍历VH文件夹中的所有文件
for file in os.listdir(vh_dir):
    if file.endswith('.tif'):
        file_path = os.path.join(vh_dir, file)
        # 使用rasterio打开文件
        with rasterio.open(file_path) as src:
            # 获取并打印波段数量
            band_count = src.count
            print(f'文件 {file} 包含的波段数量: {band_count}')
