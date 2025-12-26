from pathlib import Path
import numpy as np
from osgeo import gdal

gdal.UseExceptions()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
# --------------------------------------------------
# CONFIG (shared for solar / wind / hydro)
# --------------------------------------------------
NODATA_OUT = 0  # uint8 nodata

CLASSES = [
    (0.00, 0.20, 1),  # Very Low
    (0.20, 0.40, 2),  # Low
    (0.40, 0.60, 3),  # Medium
    (0.60, 0.80, 4),  # High
    (0.80, 1.01, 5),  # Very High (include 1.0)
]

LABELS = {
    1: "Very Low",
    2: "Low",
    3: "Medium",
    4: "High",
    5: "Very High",
}


def classify_raster(src_path: Path, dst_path: Path):
    print(f"🟢 Classifying: {src_path.name}")

    src = gdal.Open(str(src_path))
    band = src.GetRasterBand(1)

    arr = band.ReadAsArray().astype(np.float32)
    src_nodata = band.GetNoDataValue()

    classified = np.zeros(arr.shape, dtype=np.uint8)

    # Apply class thresholds
    for low, high, cls in CLASSES:
        classified[(arr >= low) & (arr < high)] = cls

    # Preserve nodata
    if src_nodata is not None:
        classified[arr == src_nodata] = NODATA_OUT

    # Write output
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
    out_band.SetNoDataValue(NODATA_OUT)
    out_band.FlushCache()

    print("✅ Classification complete")
    print("📁", dst_path)


# --------------------------------------------------
# CLI USAGE
# --------------------------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage:")
        print("  python -m analysis.classify_suitability <input.tif> <output.tif>")
        sys.exit(1)

    INPUT = Path(sys.argv[1])
    OUTPUT = Path(sys.argv[2])

    classify_raster(INPUT, OUTPUT)