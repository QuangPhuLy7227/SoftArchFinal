import os
import sys
import understand as und
from dotenv import load_dotenv

# Load .env if available
try:
    load_dotenv()
    print("✅ dotenv module loaded and .env file processed")
except Exception as e:
    print("❌ dotenv NOT working:", e)

# Set paths
VERSION_32_PATH = os.getenv("VERSION_32", "C:/Users/Owner/Downloads/commons-net-3.2-src/commons-net-3.2-src/commons-net-3.2-src.und")
VERSION_33_PATH = os.getenv("VERSION_33", "C:/Users/Owner/Downloads/commons-net-3.3-src/commons-net-3.3-src/commons-net-3.3-src.und")

# Define metrics
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

class FileComparator:
    def __init__(self):
        self.version_32_path = VERSION_32_PATH
        self.version_33_path = VERSION_33_PATH

    def get_class_metrics(self, project_path):
        db = und.open(project_path)
        class_metrics = {}
        for ent in db.ents("Class"):
            class_name = ent.longname()
            metrics = {metric: ent.metric(metric) or 0 for metric in METRICS}
            class_metrics[class_name] = metrics
        return class_metrics

    def compare_metrics(self):
        print("\n📊 Comparing metrics for classes between versions...")
        data_32 = self.get_class_metrics(self.version_32_path)
        data_33 = self.get_class_metrics(self.version_33_path)

        classes_32 = set(data_32.keys())
        classes_33 = set(data_33.keys())

        added_classes = sorted(classes_33 - classes_32)
        deleted_classes = sorted(classes_32 - classes_33)

        print("\n➕ Classes Added:")
        for c in added_classes:
            print(" +", c)

        print("\n➖ Classes Deleted:")
        for c in deleted_classes:
            print(" -", c)

        print("\n🔁 Metric Differences in Common Classes:")
        common_classes = classes_32 & classes_33
        for cls in sorted(common_classes):
            diffs = []
            for metric in METRICS:
                val_32 = data_32[cls][metric]
                val_33 = data_33[cls][metric]
                if val_32 != val_33:
                    diffs.append(f"{metric}: {val_32} → {val_33}")
            if diffs:
                print(f"📍 {cls}")
                for diff in diffs:
                    print("   -", diff)

        # General metric comparison (plain Python output)
        print("\n📈 General Metric Comparison Across Versions:")
        print(f"{'Metric':40} {'Version 3.2':>12} {'Version 3.3':>12}")
        print("-" * 70)
        for metric in METRICS:
            total_32 = sum(cls_metrics[metric] for cls_metrics in data_32.values())
            total_33 = sum(cls_metrics[metric] for cls_metrics in data_33.values())
            print(f"{metric:40} {total_32:12} {total_33:12}")

# Run it
if __name__ == "__main__":
    comparator = FileComparator()
    comparator.compare_metrics()