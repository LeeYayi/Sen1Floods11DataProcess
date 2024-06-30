import os
import rasterio
from rasterio.enums import Resampling

# 创建目标文件夹，如果不存在的话
output_vv_dir = 'Sen1Floods/VV'
output_vh_dir = 'Sen1Floods/VH'
os.makedirs(output_vv_dir, exist_ok=True)
os.makedirs(output_vh_dir, exist_ok=True)

# 定义源文件夹路径
source_dir = 'Sen1Floods11/S1'

# 遍历源文件夹中的所有tif文件
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.endswith('.tif'):
            file_path = os.path.join(root, file)
            # 读取tif文件
            with rasterio.open(file_path) as src:
                # 提取第一个波段(VV)并另存为
                vv = src.read(1)
                vv_path = os.path.join(output_vv_dir, file)
                with rasterio.open(vv_path, 'w', driver='GTiff', height=vv.shape[0],
                                   width=vv.shape[1], count=1, dtype=vv.dtype,
                                   crs=src.crs, transform=src.transform) as vv_dst:
                    vv_dst.write(vv, 1)

                # 提取第二个波段(VH)并另存为
                vh = src.read(2)
                vh_path = os.path.join(output_vh_dir, file)
                with rasterio.open(vh_path, 'w', driver='GTiff', height=vh.shape[0],
                                   width=vh.shape[1], count=1, dtype=vh.dtype,
                                   crs=src.crs, transform=src.transform) as vh_dst:
                    vh_dst.write(vh, 1)