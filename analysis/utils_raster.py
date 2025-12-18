from osgeo import gdal
import numpy as np


def log_step(msg):
    print(f"🟢 {msg}")


def read_raster(path):
    """
    Read single-band raster into NumPy array.
    """
    ds = gdal.Open(str(path))
    if ds is None:
        raise RuntimeError(f"Cannot open raster: {path}")

    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray().astype(np.float32)
    nodata = band.GetNoDataValue()

    return ds, arr, nodata


def write_raster(
    ref_ds,
    out_path,
    array,
    nodata=-9999,
    dtype=gdal.GDT_Float32,
):
    """
    Write NumPy array to GeoTIFF using reference dataset.
    """
    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(
        str(out_path),
        ref_ds.RasterXSize,
        ref_ds.RasterYSize,
        1,
        dtype,
        options=["COMPRESS=LZW"]
    )

    out_ds.SetGeoTransform(ref_ds.GetGeoTransform())
    out_ds.SetProjection(ref_ds.GetProjection())

    band = out_ds.GetRasterBand(1)
    band.WriteArray(array)
    band.SetNoDataValue(nodata)

    band.FlushCache()
    out_ds.FlushCache()
