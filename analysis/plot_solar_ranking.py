from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_CSV = PROJECT_ROOT / "outputs_reports" / "solar_zonal_statistics.csv"
OUTPUT_PNG = PROJECT_ROOT / "outputs_reports" / "state_solar_ranking.png"

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("🟢 Generating Solar Suitability Ranking Chart")

    df = pd.read_csv(INPUT_CSV)

    # Sort by solar index
    df = df.sort_values("solar_index", ascending=True)

    plt.figure(figsize=(10, 12))
    plt.barh(df["state"], df["solar_index"])

    plt.xlabel("Solar Suitability Index")
    plt.ylabel("State")
    plt.title("Solar Suitability Ranking by State (Nigeria)")

    plt.tight_layout()
    OUTPUT_PNG.parent.mkdir(exist_ok=True)
    plt.savefig(OUTPUT_PNG, dpi=300)
    plt.close()

    print("✅ Solar ranking chart saved")
    print("📁 Output:", OUTPUT_PNG)


if __name__ == "__main__":
    main()
