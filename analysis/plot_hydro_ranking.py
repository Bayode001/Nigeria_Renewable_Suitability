#plot_hydro_ranking.py
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV = PROJECT_ROOT / "outputs" / "hydro_zonal_statistics.csv"
OUT_PNG = PROJECT_ROOT / "outputs" / "state_hydro_ranking.png"

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("🟢 Plotting Hydro State Ranking")

    df = pd.read_csv(CSV)

    # Take top 15 states
    top = df.sort_values("hydro_index", ascending=False).head(15)

    plt.figure(figsize=(10, 6))
    plt.barh(top["state"], top["hydro_index"])
    plt.gca().invert_yaxis()

    plt.xlabel("Hydro Suitability Index")
    plt.ylabel("State")
    plt.title("Top 15 Nigerian States by Hydropower Suitability")

    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=300)
    plt.close()

    print("✅ Plot saved")
    print("📁", OUT_PNG)


if __name__ == "__main__":
    main()
