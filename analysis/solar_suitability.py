from osgeo import gdal
from pathlib import Path
import numpy as np


from analysis.utils_raster import (
    read_raster,
    write_raster,
    log_step,
)
from analysis.weights import SOLAR_WEIGHTS


def main():
    log_step("Starting Solar Suitability Analysis")

    PROJECT_ROOT = Path(
        r"C:/GIS_Renewable_Nigeria/Nigeria_Renewable_Suitability/github_repo"
    )

    #BASE = PROJECT_ROOT / "data/processed/aligned"
    BASE = PROJECT_ROOT /"C:/GIS_Renewable_Nigeria/data/processed/aligned/coregisteration_ghi"


   
    RASTERS = {
        "ghi": BASE / "resampled_ghi_aligned_4326.tif",
        "slope": BASE / "slope_ghi_clean_fixed.tif",
        "landcover": BASE / "landmask_ghi_coregisteration_clean.tif",
        "distance_to_grid": BASE / "grid_proximity_norm.tif",
        #"distance_to_roads": BASE / "distance_to_roads.tif",
    }

    #MASK = BASE / "resampled_landmask_binary.tif"
    MASK = Path(r"C:/GIS_Renewable_Nigeria/data/processed/aligned/resampled_landmask_binary_aligned.tif")

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
    mask = ds_mask.GetRasterBand(1).ReadAsArray().astype(np.uint8)


    # ==========================
    # NORMALIZE (0–1)
    # ==========================

    log_step("Normalizing inputs")

    ghi_n = (ghi - ghi.min()) / (ghi.max() - ghi.min())
    slope_n = 1 - (slope - slope.min()) / (slope.max() - slope.min())
    landcover_n = landcover / landcover.max()
    grid_n = 1 - (dist_grid / dist_grid.max())
    #roads_n = 1 - (dist_roads / dist_roads.max())

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
    suitability = suitability * mask
    suitability[mask == 0] = -9999


    # ==========================
    # WRITE OUTPUT
    # ==========================

    log_step("Writing output raster")
    write_raster(ds_ref, OUT, suitability)

    log_step("Solar suitability completed")
    print(f"📁 {OUT}")


if __name__ == "__main__":
    main()

