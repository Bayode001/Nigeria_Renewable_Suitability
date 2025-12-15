"""
solar_suitability.py
--------------------
Solar energy suitability analysis for Nigeria.

Inputs (processed & aligned):
- GHI raster
- Slope raster
- Grid proximity raster
- Landmask raster

Outputs:
- Solar suitability raster
"""

from pathlib import Path
from analysis.utils_raster import (
    check_file_exists,
    log_step,
    placeholder_raster_alignment,
    placeholder_masking
)

# === Project paths ===
BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PROCESSED = BASE_DIR / "data_processed"
OUTPUTS = BASE_DIR / "outputs"

# === Input rasters ===
GHI = DATA_PROCESSED / "ghi_resampled.tif"
SLOPE = DATA_PROCESSED / "slope_clipped.tif"
GRID = DATA_PROCESSED / "grid_distance.tif"
LANDMASK = DATA_PROCESSED / "landmask_binary.tif"


def main():
    log_step("Starting solar suitability analysis")

    # --- Check inputs ---
    for raster in [GHI, SLOPE, GRID, LANDMASK]:
        check_file_exists(raster)

    # --- Alignment step ---
    placeholder_raster_alignment()

    # --- Masking step ---
    placeholder_masking()

    # --- Weighted overlay (future) ---
    log_step("Weighted overlay placeholder")
    log_step("Solar suitability analysis completed")


if __name__ == "__main__":
    main()
