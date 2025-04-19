import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Prompt user for version labels ---
v1 = input("Enter first version label (e.g. 32 will be for v3.2): ").strip()
v2 = input("Enter second version label (e.g. 33 will be for v3.3): ").strip()

folder = f"{v1} vs {v2}"
summary_file = f"summary_{v1}_vs_{v2}.csv"
csv_path = os.path.join(folder, summary_file)

# --- Validate file exists ---
if not os.path.exists(csv_path):
    print(f"❌ Summary CSV not found: {csv_path}")
    exit(1)

# --- Load the summary CSV ---
df = pd.read_csv(csv_path)

# --- Filter for actual metric rows ---
metrics_only = df[df["Metric"].str.startswith("Changes in ")].copy()
metrics_only["Metric"] = metrics_only["Metric"].str.replace("Changes in ", "")

# --- Parse numeric values ---
metrics_only["Ver1"] = pd.to_numeric(metrics_only["Ver1"], errors="coerce")
metrics_only["Ver2"] = pd.to_numeric(metrics_only["Ver2"], errors="coerce")

# --- Plot ---
plt.figure(figsize=(10, 6))
bar_width = 0.35
x = range(len(metrics_only))

bars1 = plt.bar(x, metrics_only["Ver1"], width=bar_width, label=v1)
bars2 = plt.bar([i + bar_width for i in x], metrics_only["Ver2"], width=bar_width, label=v2)

plt.xticks([i + bar_width / 2 for i in x], metrics_only["Metric"], rotation=45)
plt.title(f"Metric Comparison: {v1} vs {v2}")
plt.ylabel("Total Metric Value")
plt.legend()
plt.tight_layout()

# --- Annotate bars with values ---
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        plt.annotate(
            f'{int(height)}',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha='center', va='bottom', fontsize=8
        )

add_labels(bars1)
add_labels(bars2)

plt.show()
