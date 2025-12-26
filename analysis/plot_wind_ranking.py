from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV = PROJECT_ROOT / "outputs_reports" / "wind_zonal_statistics.csv"
OUT_PNG = PROJECT_ROOT / "outputs_reports" / "state_wind_ranking.png"

def main():
    df = pd.read_csv(CSV)

    df = df.sort_values("wind_index", ascending=True)

    plt.figure(figsize=(8, 12))
    plt.barh(df["state"], df["wind_index"])
    plt.xlabel("Wind Suitability Index")
    plt.title("State-Level Wind Energy Suitability (Nigeria)")

    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=200)
    plt.close()

    print("✅ Wind ranking chart saved")
    print("📁", OUT_PNG)

if __name__ == "__main__":
    main()
