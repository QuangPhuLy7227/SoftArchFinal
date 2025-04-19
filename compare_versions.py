import sys
import os
import csv


# Load from environment or fallback to hardcoded paths
UNDERSTAND_PATH = os.getenv("UNDERSTAND_PATH", "C:/Program Files/SciTools/bin/pc-win64/Python")
VERSION_32_PATH = os.getenv("VERSION_32", "C:/Users/Owner/Downloads/commons-net-3.2-src/commons-net-3.2-src/commons-net-3.2-src.und")
VERSION_33_PATH = os.getenv("VERSION_33", "C:/Users/Owner/Downloads/commons-net-3.3-src/commons-net-3.3-src/commons-net-3.3-src.und")

# Add Understand API to sys.path
sys.path.append(UNDERSTAND_PATH)

# Try importing Understand
try:
    import understand as und
    print("✅ Understand module loaded successfully")
except Exception as e:
    print("❌ Error loading Understand module:", e)
    und = None  # Handle missing import safely

class VersionComparator:
    def __init__(self, v1_path, v2_path):
        self.v1_path = v1_path
        self.v2_path = v2_path

    def extract_metrics(self, project_path):
        if not und:
            raise RuntimeError("Understand module not loaded.")

        if not os.path.exists(project_path):
            raise FileNotFoundError(f"Understand project not found: {project_path}")

        db = und.open(project_path)
        metrics = {}

        for cls in db.ents("Class"):
            metrics[cls.name()] = {
                "Coupled": cls.metric("CountClassCoupled"),
                "Derived": cls.metric("CountClassDerived"),
                "Public Methods": cls.metric("CountDeclClassMethod"),
                "Cyclomatic": cls.metric("SumCyclomatic"),
                "Cohesion": cls.metric("PercentLackOfCohesion")
            }

        return metrics

    def compare_metrics(self):
        print(f"🔍 Comparing versions:\n- v3.2: {self.v1_path}\n- v3.3: {self.v2_path}")
        m32 = self.extract_metrics(self.v1_path)
        m33 = self.extract_metrics(self.v2_path)

        all_classes = sorted(set(m32.keys()) | set(m33.keys()))

        with open("compare_3.2_vs_3.3.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Class", "Metric", "3.2", "3.3", "Delta"])

            for cls in all_classes:
                for metric in ["Coupled", "Derived", "Public Methods", "Cyclomatic", "Cohesion"]:
                    v32 = m32.get(cls, {}).get(metric, "N/A")
                    v33 = m33.get(cls, {}).get(metric, "N/A")
                    delta = (v33 - v32) if isinstance(v32, (int, float)) and isinstance(v33, (int, float)) else "N/A"
                    writer.writerow([cls, metric, v32, v33, delta])

        print("✅ Comparison complete. Results saved to: compare_3.2_vs_3.3.csv")

# Run comparison
if __name__ == "__main__":
    if und:
        comparator = VersionComparator(VERSION_32_PATH, VERSION_33_PATH)
        try:
            comparator.compare_metrics()
        except Exception as err:
            print("❌ Error while comparing metrics:", err)
    else:
        print("⚠️ Skipping comparison: Understand API is not available.")
