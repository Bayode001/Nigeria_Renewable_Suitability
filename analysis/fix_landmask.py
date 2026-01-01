from pathlib import Path
import rasterio
import numpy as np

# Input landmask (actual source)
src_mask_path = Path(r"C:\GIS_Renewable_Nigeria\data\processed\aligned\coregisteration_ghi\landmask_ghi_coregisteration_clean.tif")

# Output binary masks
out_mask_aligned_path = Path(r"C:\GIS_Renewable_Nigeria\data\processed\aligned\resampled_landmask_binary_aligned.tif")
out_mask_coreg_path = Path(r"C:\GIS_Renewable_Nigeria\data\processed\aligned\coregisteration_ghi\resampled_landmask_binary.tif")

# Open source raster
with rasterio.open(src_mask_path) as src:
    data = src.read(1)
    # Convert to binary: 1 for valid land, 0 for invalid
    mask = np.where(data > 0, 1, 0)
    meta = src.meta.copy()
    meta.update(dtype=rasterio.uint8, count=1)

    # Save both outputs
    for out_path in [out_mask_aligned_path, out_mask_coreg_path]:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(out_path, 'w', **meta) as dst:
            dst.write(mask.astype(rasterio.uint8), 1)
        print(f"Binary mask saved: {out_path}")

