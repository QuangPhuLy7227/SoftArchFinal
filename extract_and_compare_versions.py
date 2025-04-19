import os
import sys
import csv
from pathlib import Path

sys.path.append("/Applications/Understand.app/Contents/MacOS")
import understand as und

def load_dotenv(filepath=".env"):
    try:
        with open(filepath) as f:
            for line in f:
                if line.strip() and not line.startswith("#") and "=" in line:
                    k, v = line.strip().split("=", 1)
                    os.environ[k.strip()] = v.strip()
        print("✅ .env loaded")
    except FileNotFoundError:
        print("⚠️ .env file not found")

def get_version_path(label):
    key = f"VERSION_{label.replace('v', '').replace('.', '')}"
    path = os.getenv(key)
    if not path:
        print(f"❌ {key} not found in .env")
        exit(1)
    return path

METRICS = [
    "CountClassDerived", "CountClassCoupled", "CountDeclClassVariable",
    "SumCyclomatic", "CountDeclClass", "CountDeclInstanceVariablePublic",
    "CountDeclClassMethod", "AvgCyclomatic"
]

class MetricExporter:
    def __init__(self, path): self.db_path = path
    def extract(self):
        db = und.open(self.db_path)
        result = {}
        for ent in db.ents("Class"):
            if ent.library() == "Standard": continue
            metrics = {m: ent.metric(m) or 0 for m in METRICS}
            result[ent.longname()] = metrics
        return result

def export_metrics_csv(data, version_label):
    os.makedirs("version_metrics", exist_ok=True)
    path = f"version_metrics/metrics_{version_label}.csv"
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Class"] + METRICS)
        for cls, m in data.items():
            writer.writerow([cls] + [m[k] for k in METRICS])

def summarize_and_export(v1, v2, d1, d2):
    os.makedirs("compared_version_result", exist_ok=True)
    summary_path = f"compared_version_result/summary_{v1}_vs_{v2}.csv"

    added = set(d2) - set(d1)
    deleted = set(d1) - set(d2)

    with open(summary_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Ver1", "Ver2"])
        writer.writerow(["Classes Added", len(added), ""])
        writer.writerow(["Classes Deleted", len(deleted), ""])
        for metric in METRICS:
            t1 = sum(cls[metric] for cls in d1.values())
            t2 = sum(cls[metric] for cls in d2.values())
            writer.writerow([f"Changes in {metric}", t1, t2])
    return summary_path

if __name__ == "__main__":
    load_dotenv()

    if len(sys.argv) >= 3:
        v1 = sys.argv[1]
        v2 = sys.argv[2]
    else:
        v1 = input("Enter first version (e.g. v3.2): ").strip()
        v2 = input("Enter second version (e.g. v3.3): ").strip()

    path1 = get_version_path(v1)
    path2 = get_version_path(v2)

    d1 = MetricExporter(path1).extract()
    d2 = MetricExporter(path2).extract()

    export_metrics_csv(d1, v1)
    export_metrics_csv(d2, v2)
    summary_file = summarize_and_export(v1, v2, d1, d2)

    print(f"\n✅ Metrics and summary exported:")
    print(f" - version_metrics/metrics_{v1}.csv")
    print(f" - version_metrics/metrics_{v2}.csv")
    print(f" - {summary_file}")
