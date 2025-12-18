from osgeo import gdal
from pathlib import Path

# -------------------------
# PATHS (VERIFY THESE)
# -------------------------

REF = Path(
    r"C:/GIS_Renewable_Nigeria/data/processed/aligned/coregisteration_ghi/resampled_ghi_aligned_4326.tif"
)

MASK_SRC = Path(
    r"C:/GIS_Renewable_Nigeria/data/processed/aligned/coregisteration_ghi/resampled_landmask_binary.tif"
)

MASK_OUT = Path(
    r"C:/GIS_Renewable_Nigeria/data/processed/aligned/resampled_landmask_binary_aligned.tif"
)

MASK_OUT.parent.mkdir(parents=True, exist_ok=True)

print("🟢 Opening reference raster")
ref_ds = gdal.Open(str(REF))
if ref_ds is None:
    raise RuntimeError(f"Cannot open reference raster: {REF}")

# -------------------------
# EXTRACT GRID
# -------------------------

gt = ref_ds.GetGeoTransform()
xmin = gt[0]
ymax = gt[3]
xres = gt[1]
yres = abs(gt[5])

xmax = xmin + xres * ref_ds.RasterXSize
ymin = ymax - yres * ref_ds.RasterYSize

print("🟢 Preparing warp options")

warp_opts = gdal.WarpOptions(
    format="GTiff",
    outputBounds=(xmin, ymin, xmax, ymax),
    xRes=xres,
    yRes=yres,
    targetAlignedPixels=True,
    resampleAlg=gdal.GRA_NearestNeighbour,
    dstNodata=0,
    creationOptions=["COMPRESS=LZW"],
)

print("🟢 Warping land mask to reference grid")

gdal.Warp(
    destNameOrDestDS=str(MASK_OUT),
    srcDSOrSrcDSTab=str(MASK_SRC),
    options=warp_opts,
)

print("✅ Mask aligned successfully")
print("📁", MASK_OUT)
