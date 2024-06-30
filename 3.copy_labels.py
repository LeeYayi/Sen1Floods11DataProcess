import os
import numpy as np
import rasterio

# 创建目标文件夹，如果不存在的话
output_labels_dir = 'Sen1Floods/Labels'
os.makedirs(output_labels_dir, exist_ok=True)

# 定义源文件夹路径
source_labels_dir = 'Sen1Floods11/Labels'

# 遍历源文件夹中的所有tif文件
for root, dirs, files in os.walk(source_labels_dir):
    for file in files:
        if file.endswith('.tif'):
            file_path = os.path.join(root, file)
            # 读取tif文件
            with rasterio.open(file_path) as src:
                label_band = src.read(1)  # 读取第一个波段
                
                # 移除值为-1的数据，仅保留[0,1]范围的数据
                label_band = np.where(label_band == -1, 0, label_band)  # 将-1替换为0
                
                # 保存处理后的图像到目标文件夹
                output_path = os.path.join(output_labels_dir, file)
                with rasterio.open(output_path, 'w', driver='GTiff', height=label_band.shape[0],
                                   width=label_band.shape[1], count=1, dtype=label_band.dtype,
                                   crs=src.crs, transform=src.transform) as dst:
                    dst.write(label_band, 1)