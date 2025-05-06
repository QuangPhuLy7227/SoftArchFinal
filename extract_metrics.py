import os
import sys
import csv
from pathlib import Path
import understand as und

# --- Load .env ---
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

def load_total_class_counts(filepath="total_class_count.txt"):
    counts = {}
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    version, count = line.split("=", 1)
                    counts[version.strip()] = int(count.strip())
    except FileNotFoundError:
        print("❌ total_class_count.txt not found. Using fallback counts.")
    return counts

def get_version_path(label):
    try:
        num = label.lower().replace("v", "").replace(".", "")  
        key = f"VERSION_{num}"
        value = os.getenv(key)
        if not value:
            print(f"❌ Version key {key} not found in .env")
            exit(1)
        return key, value
    except Exception as e:
        print(f"❌ Error parsing version label {label}: {e}")
        exit(1)

# --- Metric config ---
METRICS = [
    "CountClassDerived",
    "CountClassCoupled",
    "CountDeclClassVariable",
    "SumCyclomatic",
    "CountDeclClass",
    "CountDeclInstanceVariablePublic",
    "CountDeclClassMethod",
    "AvgCyclomatic"
]

class MetricExporter:
    def __init__(self, db_path):
        self.db_path = db_path

    def extract(self):
        db = und.open(self.db_path)
        classes = {}
        interfaces = {}

        for ent in db.ents("Class ~Interface"):
            if ent.library() == "Standard":
                continue
            name = ent.longname()
            metrics = {metric: ent.metric(metric) or 0 for metric in METRICS}
            classes[name] = metrics

        for ent in db.ents("Interface"):
            if ent.library() == "Standard":
                continue
            name = ent.longname()
            interfaces[name] = {}

        return classes, interfaces

def export_metrics_csv(data, filepath):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Class"] + METRICS)
        for cls, metrics in data.items():
            row = [cls] + [metrics[m] for m in METRICS]
            writer.writerow(row)

def summarize_totals(v1_label, v2_label,
                     data1, data2,
                     interfaces1, interfaces2,
                     added_classes, deleted_classes,
                     added_interfaces, deleted_interfaces,
                     output_path,
                     total_class_counts):
    summary = []

    total_classes_v1 = total_class_counts.get(v1_label, len(data1))
    total_classes_v2 = total_class_counts.get(v2_label, len(data2))
    total_interfaces_v1 = len(interfaces1)
    total_interfaces_v2 = len(interfaces2)

    class_added_count = total_classes_v2 - total_classes_v1 + len(deleted_classes)

    summary.append(["Total Classes", total_classes_v1, total_classes_v2])
    summary.append(["Total Interfaces", total_interfaces_v1, total_interfaces_v2])
    summary.append(["Classes Added", "", class_added_count])
    summary.append(["Classes Deleted", len(deleted_classes), ""])
    summary.append(["Interfaces Added", "", len(added_interfaces)])
    summary.append(["Interfaces Deleted", len(deleted_interfaces), ""])

    for metric in METRICS:
        total1 = sum(cls[metric] for cls in data1.values())
        total2 = sum(cls[metric] for cls in data2.values())
        summary.append([f"Changes in {metric}", total1, total2])

    print("\n📊 Metric Summary Table")
    print(f"{'Metric':35} {v1_label:>10} {v2_label:>10}")
    print("-" * 60)
    for row in summary:
        print(f"{row[0]:35} {str(row[1]):>10} {str(row[2]):>10}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", v1_label, v2_label])
        writer.writerows(summary)

    print("\n🆕 Classes Added:")
    for name in sorted(added_classes):
        print(" +", name)

    print("\n🗑️ Classes Deleted:")
    for name in sorted(deleted_classes):
        print(" -", name)

    print("\n🆕 Interfaces Added:")
    for name in sorted(added_interfaces):
        print(" +", name)

    print("\n🗑️ Interfaces Deleted:")
    for name in sorted(deleted_interfaces):
        print(" -", name)

# --- Main Execution ---
if __name__ == "__main__":
    load_dotenv()
    total_class_counts = load_total_class_counts()

    v1_label = input("Enter first version label (e.g. v3.2): ").strip()
    v2_label = input("Enter second version label (e.g. v3.3): ").strip()

    if not v1_label.startswith("v"):
        v1_label = "v" + v1_label
    if not v2_label.startswith("v"):
        v2_label = "v" + v2_label

    k1, path1 = get_version_path(v1_label)
    k2, path2 = get_version_path(v2_label)

    output_dir = os.path.join("version_metrics")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n📦 Comparing: {v1_label} vs {v2_label}")
    print(f"📂 Exporting to: {output_dir}/")

    data1, interfaces1 = MetricExporter(path1).extract()
    data2, interfaces2 = MetricExporter(path2).extract()

    export_metrics_csv(data1, os.path.join(output_dir, f"metrics_{v1_label}.csv"))
    export_metrics_csv(data2, os.path.join(output_dir, f"metrics_{v2_label}.csv"))

    added_classes = set(data2.keys()) - set(data1.keys())
    deleted_classes = set(data1.keys()) - set(data2.keys())
    added_interfaces = set(interfaces2.keys()) - set(interfaces1.keys())
    deleted_interfaces = set(interfaces1.keys()) - set(interfaces2.keys())

    output_summary_dir = os.path.join("compared_version_result")
    os.makedirs(output_summary_dir, exist_ok=True)
    summary_path = os.path.join(output_summary_dir, f"summary_{v1_label}_vs_{v2_label}.csv")

    summarize_totals(v1_label, v2_label,
                     data1, data2,
                     interfaces1, interfaces2,
                     added_classes, deleted_classes,
                     added_interfaces, deleted_interfaces,
                     summary_path,
                     total_class_counts)