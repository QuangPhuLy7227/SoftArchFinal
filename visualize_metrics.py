import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

# --- Prompt user for version labels once ---
v1 = input("Enter first version label (e.g. v3.2): ").strip()
v2 = input("Enter second version label (e.g. v3.3): ").strip()

# --- Define summary file path ---
summary_dir = "compared_version_result"
summary_file = f"summary_{v1}_vs_{v2}.csv"
summary_path = os.path.join(summary_dir, summary_file)

# --- Run extract_and_compare_versions.py if summary not found ---
if not os.path.exists(summary_path):
    print("🔍 Summary not found, running extraction...")
    subprocess.run([
        "/Applications/Understand.app/Contents/MacOS/upython",
        "extract_and_compare_versions.py", v1, v2
    ], check=True)

# --- Recheck file after subprocess ---
if not os.path.exists(summary_path):
    print(f"❌ Could not generate summary: {summary_path}")
    exit(1)

# --- Load the summary CSV ---
df = pd.read_csv(summary_path)

# --- Filter for metrics only ---
metrics_only = df[df["Metric"].str.startswith("Changes in ")].copy()
metrics_only["Metric"] = metrics_only["Metric"].str.replace("Changes in ", "")
metrics_only["Ver1"] = pd.to_numeric(metrics_only["Ver1"], errors="coerce")
metrics_only["Ver2"] = pd.to_numeric(metrics_only["Ver2"], errors="coerce")

# --- Plot setup ---
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

# --- Add value labels on bars ---
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        plt.annotate(
            f'{int(height)}',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha='center', va='bottom', fontsize=8
        )

add_labels(bars1)
add_labels(bars2)

# --- Show plot ---
plt.show()