import os
import understand as und

def detect_singletons(project_path):
    db = und.open(project_path)
    results = []

    for cls in db.ents("Class"):
        fields = [ref.ent().name() for ref in cls.refs("Define", "Variable")]
        methods = [ref.ent().name() for ref in cls.refs("Define", "Method")]

        has_static_instance = any("instance" in f.lower() for f in fields)
        has_getInstance = any("getinstance" in m.lower() for m in methods)

        if has_static_instance and has_getInstance:
            results.append(cls.longname())

    print("🔍 Possible Singleton Classes:")
    for r in results:
        print(" -", r)

# Example usage
if __name__ == "__main__":
    path = input("Enter path to .und file: ").strip()
    detect_singletons(path)