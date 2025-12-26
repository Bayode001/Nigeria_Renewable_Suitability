# analysis/zonal_stats_wind.py
from pathlib import Path
import pandas as pd
import geopandas as gpd
from rasterstats import zonal_stats

# --------------------------------------------------
# PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RASTER = PROJECT_ROOT / "outputs" / "wind_suitability_classified.tif"
STATES = PROJECT_ROOT / "data" / "boundaries" / "nga_adm1_32632.shp"

OUTPUT_CSV = PROJECT_ROOT / "outputs_reports" / "wind_zonal_statistics.csv"

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
    print("🟢 Running Wind Zonal Statistics")

    states = gpd.read_file(STATES)

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

        # collect counts
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

        # wind index
        row["wind_index"] = (
            WEIGHTS["very_high"] * row["pct_very_high"]
            + WEIGHTS["high"] * row["pct_high"]
        )

        row["state"] = props.get("ADM1_EN", "UNKNOWN")

        rows.append(row)

    df = pd.DataFrame(rows)

    # ranking
    df = df.sort_values("wind_index", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1

    df.to_csv(OUTPUT_CSV, index=False)

    print("✅ Wind zonal statistics completed")
    print("📁 Output:", OUTPUT_CSV)


if __name__ == "__main__":
    main()
