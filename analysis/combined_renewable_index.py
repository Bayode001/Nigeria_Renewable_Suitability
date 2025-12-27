import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "outputs_reports"

SOLAR = OUT_DIR / "solar_zonal_statistics.csv"
WIND = OUT_DIR / "wind_zonal_statistics.csv"
HYDRO = OUT_DIR / "hydro_zonal_statistics.csv"

OUT_CSV = OUT_DIR / "combined_renewable_index.csv"

# ----------------------------
# WEIGHTS (v1 – adjustable)
# ----------------------------
W_SOLAR = 0.40
W_WIND = 0.35
W_HYDRO = 0.25

print("🟢 Building Combined Renewable Suitability Index")

# Load
solar = pd.read_csv(SOLAR)[["state", "solar_index"]]
wind = pd.read_csv(WIND)[["state", "wind_index"]]
hydro = pd.read_csv(HYDRO)[["state", "hydro_index"]]

# Merge
df = solar.merge(wind, on="state").merge(hydro, on="state")

# Normalize each index (0–1)
for col in ["solar_index", "wind_index", "hydro_index"]:
    df[col + "_norm"] = df[col] / df[col].max()

# Combined index
df["combined_index"] = (
    W_SOLAR * df["solar_index_norm"]
    + W_WIND * df["wind_index_norm"]
    + W_HYDRO * df["hydro_index_norm"]
)

# Ranking
df = df.sort_values("combined_index", ascending=False).reset_index(drop=True)
df["rank"] = df.index + 1

# Save
df.to_csv(OUT_CSV, index=False)

print("✅ Combined index created")
print("📁 Output:", OUT_CSV)
