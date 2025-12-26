from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
from rasterstats import zonal_stats
from osgeo import gdal

gdal.UseExceptions()

# --------------------------------------------------
# PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RASTER = PROJECT_ROOT / "outputs" / "hydro_suitability_classified.tif"

STATES = Path(
    r"C:/GIS_Renewable_Nigeria/github_repo_clean/data/boundaries/nga_adm1_32632.shp"
)

OUTPUT_CSV = PROJECT_ROOT / "outputs" / "hydro_zonal_statistics.csv"

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

CLASS_LABELS = {
    1: "very_low",
    2: "low",
    3: "medium",
    4: "high",
    5: "very_high",
}

WEIGHTS = {
    "high": 0.4,
    "very_high": 0.6,
}

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("🟢 Running Hydro Zonal Statistics")

    # --- Load states ---
    states = gpd.read_file(STATES)

    if states.crs is None:
        raise RuntimeError("❌ States shapefile has no CRS")

    # --- Load raster ---
    raster_ds = gdal.Open(str(RASTER))
    if raster_ds is None:
        raise RuntimeError("❌ Could not open raster")

    raster_crs = raster_ds.GetProjection()

    # --- Reproject states if needed ---
    if states.crs.to_wkt() != raster_crs:
        states = states.to_crs(raster_crs)

    # --- Zonal stats ---
    zs = zonal_stats(
        states,
        RASTER,
        categorical=True,
        nodata=0,
        geojson_out=True,
    )

    rows = []

    for feature in zs:
        props = feature["properties"]
        row = {}

        total_pixels = 0

        # class counts
        for cls, label in CLASS_LABELS.items():
            count = props.get(cls, 0)
            row[f"count_{label}"] = count
            total_pixels += count

        row["total_pixels"] = total_pixels

        # percentages
        for label in CLASS_LABELS.values():
            row[f"pct_{label}"] = (
                row[f"count_{label}"] / total_pixels * 100
                if total_pixels > 0 else 0
            )

        # hydro suitability index
        row["hydro_index"] = (
            WEIGHTS["very_high"] * row["pct_very_high"]
            + WEIGHTS["high"] * row["pct_high"]
        )

        # state name (ADM1)
        row["state"] = props.get("ADM1_EN", "UNKNOWN")

        rows.append(row)

    df = pd.DataFrame(rows)

    # ranking
    df = df.sort_values("hydro_index", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1

    df.to_csv(OUTPUT_CSV, index=False)

    print("✅ Zonal statistics completed")
    print("📁 Output:", OUTPUT_CSV)


if __name__ == "__main__":
    main()
