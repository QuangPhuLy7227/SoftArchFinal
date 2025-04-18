import sys
import os
import csv
import understand as und
from dotenv import load_dotenv

class VersionComparator:
    def __init__(self):
        load_dotenv()
        self.und_path = os.getenv("UNDERSTAND_PATH")
        self.version_32_path = os.getenv("VERSION_32")
        self.version_33_path = os.getenv("VERSION_33")

        if self.und_path:
            sys.path.append(self.und_path)

    def extract_metrics(self, project_path):
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
        m32 = self.extract_metrics(self.version_32_path)
        m33 = self.extract_metrics(self.version_33_path)

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

        print("✅ Comparison complete. Output saved to compare_3.2_vs_3.3.csv")

# Run the comparison
if __name__ == "__main__":
    comparator = VersionComparator()
    comparator.compare_metrics()