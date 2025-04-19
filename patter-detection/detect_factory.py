import os
import understand as und

def detect_factories(project_path):
    db = und.open(project_path)
    results = []

    for func in db.ents("Function"):
        name = func.name().lower()
        if name.startswith("create") or name.startswith("build") or name.startswith("get"):
            if func.kindname().startswith("Method") and "return" in func.parameters():
                results.append(func.parent().longname())

    print("🏭 Possible Factory Method Classes:")
    for r in sorted(set(results)):
        print(" -", r)

# Example usage
if __name__ == "__main__":
    path = input("Enter path to .und file: ").strip()
    detect_factories(path)
