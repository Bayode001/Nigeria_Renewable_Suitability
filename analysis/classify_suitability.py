
from pathlib import Path
import numpy as np
from osgeo import gdal

gdal.UseExceptions()

# --------------------------------------------------
# CONFIG (reused for solar / wind / hydro)
# --------------------------------------------------
NODATA = 0  # valid for uint8

CLASSES = [
    (0.00, 0.20, 1),  # Very Low
    (0.20, 0.40, 2),  # Low
    (0.40, 0.60, 3),  # Medium
    (0.60, 0.80, 4),  # High
    (0.80, 1.00, 5),  # Very High
]

LABELS = {
    1: "Very Low",
    2: "Low",
    3: "Medium",
    4: "High",
    5: "Very High",
}


def classify_raster(src_path, dst_path):
    src = gdal.Open(str(src_path))
    if src is None:
        raise RuntimeError(f"Cannot open raster: {src_path}")

    band = src.GetRasterBand(1)
    arr = band.ReadAsArray().astype(np.float32)
    src_nodata = band.GetNoDataValue()

    classified = np.zeros(arr.shape, dtype=np.uint8)

    # Apply classes
    for lo, hi, cls in CLASSES:
        classified[(arr >= lo) & (arr < hi)] = cls

    # Preserve NoData
    if src_nodata is not None:
        classified[arr == src_nodata] = NODATA

    driver = gdal.GetDriverByName("GTiff")
    dst = driver.Create(
        str(dst_path),
        src.RasterXSize,
        src.RasterYSize,
        1,
        gdal.GDT_Byte,
        options=["COMPRESS=LZW", "TILED=YES"],
    )

    dst.SetGeoTransform(src.GetGeoTransform())
    dst.SetProjection(src.GetProjection())

    out_band = dst.GetRasterBand(1)
    out_band.WriteArray(classified)
    out_band.SetNoDataValue(NODATA)
    out_band.FlushCache()

    print("✅ Classification complete")
    print("📁", dst_path)


if __name__ == "__main__":
    INPUT = Path("outputs/solar_suitability_continuous.tif")
    OUTPUT = Path("outputs/solar_suitability_classified.tif")

    classify_raster(INPUT, OUTPUT)
