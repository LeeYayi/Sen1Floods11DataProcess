import numpy as np
import os
import rasterio
from rasterio.transform import Affine

def tile256(raster_path, output_dir):
    """
    Modified to handle 512x512 images, split them into four 256x256 tiles,
    and rename files according to specified pattern.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    with rasterio.open(raster_path) as src:
        width = src.width
        height = src.height
        res = src.transform[0]
        UL_c, UL_r = src.transform * (0, 0)
        band = src.read(1)
        kwargs = src.meta.copy()
        
        base_filename = os.path.splitext(os.path.basename(raster_path))[0]
        
        for col in range(2):  # 512 / 256 = 2
            for row in range(2):  # 512 / 256 = 2
                tf_tile = Affine(res, 0.0, UL_c + (256 * res * col), 0.0, -res, UL_r + (256 * -res * row))
                # File renaming: remove part after second underscore and add tile index
                base_name = os.path.splitext(os.path.basename(raster_path))[0]
                new_base_name = '_'.join(base_name.split('_')[:2])  # Keep only first two parts
                tile_name = f"{new_base_name}_{row}{col}.tif"  # New file name with tile index

                # tile_name = f'{base_filename}_{row}{col}.tif'
                
                np_arr = np.zeros((256, 256), dtype=band.dtype)
                tile_band = band[256 * row : 256 * (row + 1), 256 * col : 256 * (col + 1)]
                np_arr[:tile_band.shape[0], :tile_band.shape[1]] = tile_band
                
                kwargs.update({
                    'transform': tf_tile,
                    'width': 256,
                    'height': 256,
                    'compress': 'lzw',
                    'dtype': band.dtype,
                })
                
                with rasterio.open(os.path.join(output_dir, tile_name), "w", **kwargs) as dst:
                    dst.write(np_arr, 1)

# 定义源目录和目标目录
source_dirs = {
    'VV': 'Sen1Floods/VV',
    'VH': 'Sen1Floods/VH',
    'Labels': 'Sen1Floods/Labels',
}
output_dirs = {
    'VV': 'Sen1Floods_256/VV',
    'VH': 'Sen1Floods_256/VH',
    'Labels': 'Sen1Floods_256/Labels',
}

# 对每个目录应用 tile256 函数
for category, source_dir in source_dirs.items():
    output_dir = output_dirs[category]
    for file in os.listdir(source_dir):
        if file.endswith('.tif'):
            raster_path = os.path.join(source_dir, file)
            tile256(raster_path, output_dir)
