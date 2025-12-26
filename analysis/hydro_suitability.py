from pathlib import Path
import numpy as np
from osgeo import gdal

gdal.UseExceptions()

# --------------------------------------------------
# PATHS
# --------------------------------------------------

DATA = Path(r"C:/GIS_Renewable_Nigeria/hydro")

RAS = {
    "flow": DATA / "flowacc_cell_count.tif",
    "slope": DATA / "slope_from_dem_aligned.tif",   # <-- MUST be slope
}

MASK = DATA / "landmask_binary_hydro_fixed.tif"
OUTPUT = Path("outputs/hydro_suitability_continuous.tif")

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

WEIGHTS = {
    "flow": 0.7,
    "slope": 0.3,
}

NODATA = -9999
BLOCK = 1024

# --------------------------------------------------
# SCORING FUNCTIONS
# --------------------------------------------------

def log_normalize(arr):
    """Log-scale normalize flow accumulation"""
    arr = np.where(arr <= 0, np.nan, arr)
    arr = np.log1p(arr)

    vmin = np.nanpercentile(arr, 5)
    vmax = np.nanpercentile(arr, 95)

    arr = np.clip(arr, vmin, vmax)
    return (arr - vmin) / (vmax - vmin)


def slope_score(slope):
    """
    Lower slope = better for hydro
    """
    score = np.zeros_like(slope, dtype=np.float32)
    score[slope <= 5] = 1.0
    score[(slope > 5) & (slope <= 15)] = 0.6
    score[slope > 15] = 0.2
    return score


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("🟢 Starting Hydro Suitability Analysis")

    ds_flow = gdal.Open(str(RAS["flow"]))
    ds_slope = gdal.Open(str(RAS["slope"]))
    ds_mask = gdal.Open(str(MASK))

    if not all([ds_flow, ds_slope, ds_mask]):
        raise RuntimeError("❌ Failed to open one or more input rasters")

    flow_band = ds_flow.GetRasterBand(1)
    slope_band = ds_slope.GetRasterBand(1)
    mask_band = ds_mask.GetRasterBand(1)

    xsize = ds_flow.RasterXSize
    ysize = ds_flow.RasterYSize

    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(
        str(OUTPUT),
        xsize,
        ysize,
        1,
        gdal.GDT_Float32,
        options=["TILED=YES", "COMPRESS=LZW"],
    )

    out_ds.SetGeoTransform(ds_flow.GetGeoTransform())
    out_ds.SetProjection(ds_flow.GetProjection())

    out_band = out_ds.GetRasterBand(1)
    out_band.SetNoDataValue(NODATA)

    # --------------------------------------------------
    # BLOCK PROCESSING
    # --------------------------------------------------

    for y in range(0, ysize, BLOCK):
        rows = min(BLOCK, ysize - y)

        for x in range(0, xsize, BLOCK):
            cols = min(BLOCK, xsize - x)

            flow = flow_band.ReadAsArray(x, y, cols, rows).astype(np.float32)
            slope = slope_band.ReadAsArray(x, y, cols, rows).astype(np.float32)
            mask = mask_band.ReadAsArray(x, y, cols, rows)

            flow_n = log_normalize(flow)
            slope_n = slope_score(slope)

            suitability = (
                WEIGHTS["flow"] * flow_n
                + WEIGHTS["slope"] * slope_n
            )

            suitability[mask == 0] = NODATA
            out_band.WriteArray(suitability, x, y)

    out_band.FlushCache()
    out_ds = None

    print("✅ Hydro suitability completed")
    print("📁 Output:", OUTPUT)


if __name__ == "__main__":
    main()
