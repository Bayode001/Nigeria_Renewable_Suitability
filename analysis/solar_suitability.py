from osgeo import gdal
from pathlib import Path
import numpy as np

gdal.UseExceptions()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
# C:\GIS_Renewable_Nigeria\data\processed\aligned\coregisteration_ghi\landmask_ghi_coregisteration_clean.tif


from analysis.utils_raster import (
    read_raster,
    write_raster,
    log_step,
)
from analysis.weights import SOLAR_WEIGHTS

def safe_norm(arr):
    """
    Normalize array to 0–1 safely.
    Returns zeros if array is flat or invalid.
    """
    arr = arr.astype(np.float32)
    valid = np.isfinite(arr)

    if not np.any(valid):
        return np.zeros_like(arr, dtype=np.float32)

    vmin = arr[valid].min()
    vmax = arr[valid].max()

    if vmax == vmin:
        return np.zeros_like(arr, dtype=np.float32)

    out = np.zeros_like(arr, dtype=np.float32)
    out[valid] = (arr[valid] - vmin) / (vmax - vmin)
    return out


def main():
    log_step("Starting Solar Suitability Analysis")

    BASE = Path(
        r"C:/GIS_Renewable_Nigeria/data/processed/aligned/coregisteration_ghi"
    )

    RASTERS = {
        "ghi": BASE / "resampled_ghi_aligned_4326.tif",
        "slope": BASE / "slope_ghi_coregisteration.tif",
        "landcover": BASE / "landmask_ghi_coregisteration.tif",
        "distance_to_grid": BASE / "grid_ghi_coregisteration.tif",
    }

    MASK = Path(
        r"C:/GIS_Renewable_Nigeria/data/processed/aligned/coregisteration_ghi/landmask_ghi_coregisteration.tif"
    )

    OUTPUT_DIR = PROJECT_ROOT / "outputs"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    OUT = OUTPUT_DIR / "solar_suitability_continuous.tif"

    # ==========================
    # READ RASTERS
    # ==========================

    log_step("Reading rasters")

    ds_ref, ghi, _ = read_raster(RASTERS["ghi"])
    _, slope, _ = read_raster(RASTERS["slope"])
    _, landcover, _ = read_raster(RASTERS["landcover"])
    _, dist_grid, _ = read_raster(RASTERS["distance_to_grid"])
    #_, dist_roads, _ = read_raster(RASTERS["distance_to_roads"])
    ds_mask = gdal.Open(str(MASK))
    mask_raw = ds_mask.GetRasterBand(1).ReadAsArray()

    # Treat anything > 0 as valid land
    mask = np.where(np.isfinite(mask_raw) & (mask_raw > 0), 1, 0).astype(np.uint8)


    # ==========================
    # NORMALIZE (0–1)
    # ==========================

    log_step("Normalizing inputs")

    ghi_n        = safe_norm(ghi)
    slope_n      = 1 - safe_norm(slope)
    #landcover_n  = safe_norm(landcover)
    # Example landcover suitability mapping
    # Adjust values to your schema
    landcover_n = np.zeros_like(landcover, dtype=np.float32)

    landcover_n[np.isin(landcover, [1, 2])] = 1.0   # barren / grassland
    landcover_n[np.isin(landcover, [3])] = 0.6      # shrub
    landcover_n[np.isin(landcover, [4])] = 0.2      # forest
    landcover_n[np.isin(landcover, [5])] = 0.0      # water / urban

    grid_n       = 1 - safe_norm(dist_grid)


    print("GHI norm:", ghi_n.min(), ghi_n.max())
    print("Slope norm:", slope_n.min(), slope_n.max())
    print("Landcover norm:", landcover_n.min(), landcover_n.max(), np.unique(landcover_n))
    print("Grid norm:", grid_n.min(), grid_n.max())


    # ==========================
    # WEIGHTED OVERLAY
    # ==========================

    log_step("Applying weights")

    suitability = (
        ghi_n * SOLAR_WEIGHTS["ghi"]
        + slope_n * SOLAR_WEIGHTS["slope"]
        + landcover_n * SOLAR_WEIGHTS["landcover"]
        + grid_n * SOLAR_WEIGHTS["distance_to_grid"]
        #+ roads_n * SOLAR_WEIGHTS["distance_to_roads"]
    )

    # ==========================
    # MASK
    # ==========================

    log_step("Applying land mask")
    suitability = np.clip(suitability, 0, 1)
    suitability[mask == 0] = -9999

    # ==========================
    # FINAL NORMALIZATION
    # ==========================

    log_step("Final normalization")

    valid = suitability != -9999
    #suitability[valid] = safe_norm(suitability[valid])
    tmp = suitability.copy()
    tmp[tmp == -9999] = np.nan
    tmp = safe_norm(tmp)
    suitability[tmp == 0] = -9999
    suitability[tmp != 0] = tmp[tmp != 0]

    suitability[suitability < 1e-6] = 0

    # ==========================
    # WRITE OUTPUT
    # ==========================

    log_step("Writing output raster")
    write_raster(ds_ref, OUT, suitability)

    log_step("Solar suitability completed")
    print(f"📁 {OUT}")


if __name__ == "__main__":
    main()

