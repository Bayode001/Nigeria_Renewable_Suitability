from pathlib import Path
import numpy as np
from osgeo import gdal

gdal.UseExceptions()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# --------------------------------------------------
# PATHS (REAL ON-DISK LOCATIONS)
# --------------------------------------------------

WIND = Path(
    r"C:/GIS_Renewable_Nigeria/data/processed/aligned/coregisteration_landcover/"
    r"wind_landcover_coregisteration.tif"
)

LANDCOVER = Path(
    r"C:/GIS_Renewable_Nigeria/data/processed/aligned/coregisteration_landcover/"
    r"resampled_landcover_aligned_32632.tif"
)

MASK = Path(
    r"C:/GIS_Renewable_Nigeria/data/processed/suitability/"
    r"landmask_aligned_to_wind.tif"
)

OUTPUT = Path("outputs/wind_suitability_continuous.tif")

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

WEIGHTS = {
    "wind": 0.7,
    "land": 0.3,
}

NODATA = -9999
BLOCK = 1024  # safe tile size


# --------------------------------------------------
# SCORING
# --------------------------------------------------

def normalize(arr, vmin, vmax):
    arr = np.clip(arr, vmin, vmax)
    return (arr - vmin) / (vmax - vmin)


def landcover_score(lc):
    score = np.zeros_like(lc, dtype=np.float32)
    score[lc == 3] = 0.2   # forest
    score[lc == 4] = 0.6   # cropland
    score[lc == 5] = 1.0   # grassland
    return score


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("🟢 Starting Wind Suitability Analysis")

    ds_wind = gdal.Open(str(WIND))
    ds_land = gdal.Open(str(LANDCOVER))
    ds_mask = gdal.Open(str(MASK))

    if not all([ds_wind, ds_land, ds_mask]):
        raise RuntimeError("❌ Failed to open one or more input rasters")

    wind_band = ds_wind.GetRasterBand(1)
    land_band = ds_land.GetRasterBand(1)
    mask_band = ds_mask.GetRasterBand(1)

    xsize = ds_wind.RasterXSize
    ysize = ds_wind.RasterYSize

    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(
        str(OUTPUT),
        xsize,
        ysize,
        1,
        gdal.GDT_Float32,
        options=["TILED=YES", "COMPRESS=LZW"],
    )

    out_ds.SetGeoTransform(ds_wind.GetGeoTransform())
    out_ds.SetProjection(ds_wind.GetProjection())

    out_band = out_ds.GetRasterBand(1)
    out_band.SetNoDataValue(NODATA)

    # --------------------------------------------------
    # BLOCK PROCESSING (SAFE)
    # --------------------------------------------------

    for y in range(0, ysize, BLOCK):
        rows = min(BLOCK, ysize - y)

        for x in range(0, xsize, BLOCK):
            cols = min(BLOCK, xsize - x)

            wind = wind_band.ReadAsArray(x, y, cols, rows).astype(np.float32)
            land = land_band.ReadAsArray(x, y, cols, rows)
            mask = mask_band.ReadAsArray(x, y, cols, rows)

            wind_norm = normalize(wind, 0, 10)
            land_norm = landcover_score(land)

            suitability = (
                WEIGHTS["wind"] * wind_norm
                + WEIGHTS["land"] * land_norm
            )

            suitability[mask == 0] = NODATA
            out_band.WriteArray(suitability, x, y)

    out_band.FlushCache()
    out_ds = None

    print("✅ Wind suitability completed")
    print("📁 Output:", OUTPUT)


if __name__ == "__main__":
    main()

