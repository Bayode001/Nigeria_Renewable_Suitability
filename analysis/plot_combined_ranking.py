import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV = PROJECT_ROOT / "outputs_reports" / "combined_renewable_index.csv"
OUT = PROJECT_ROOT / "outputs_reports" / "combined_state_ranking.png"

df = pd.read_csv(CSV)

top = df.head(15)

plt.figure(figsize=(10, 6))
plt.barh(top["state"], top["combined_index"])
plt.gca().invert_yaxis()

plt.xlabel("Combined Renewable Suitability Index")
plt.title("Top 15 Nigerian States – Combined Renewable Suitability")

plt.tight_layout()
plt.savefig(OUT, dpi=200)
plt.close()

print("✅ Combined ranking chart saved:", OUT)
