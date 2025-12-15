"""
Solar Suitability Analysis – Nigeria
Main orchestration script
"""

from analysis.utils_raster import log_step, ensure_exists, ensure_folder
from pathlib import Path


BASE = Path("C:/GIS_Renewable_Nigeria/Nigeria_Renewable_Suitability")
DATA = BASE / "data"
PROCESSED = DATA / "processed"
OUTPUTS = BASE / "outputs"


def main():
    log_step("Starting solar suitability analysis")

    ensure_folder(OUTPUTS)

    ghi = ensure_exists(PROCESSED / "resampled_ghi_aligned_4326.tif")
    slope = ensure_exists(PROCESSED / "resampled_slope_aligned_4326.tif")
    landmask = ensure_exists(PROCESSED / "resampled_landmask_binary.tif")

    log_step("All input rasters verified")
    log_step("Ready for weighted overlay / classification")


if __name__ == "__main__":
    main()
