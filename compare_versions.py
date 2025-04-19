import os
import sys
import understand as und
from dotenv import load_dotenv

UNDERSTAND_PATH = "C:/Program Files/SciTools/bin/pc-win64/Python"
VERSION_32_PATH = "C:/Users/Owner/Downloads/commons-net-3.2-src/commons-net-3.2-src/commons-net-3.2-src.und"
VERSION_33_PATH = "C:/Users/Owner/Downloads/commons-net-3.3-src/commons-net-3.3-src/commons-net-3.3-src.und"

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ dotenv module loaded and .env file processed")
except Exception as e:
    print("❌ dotenv NOT working:", e)
    
print("🔍 VERSION_32 =", os.getenv("VERSION_32"))
print("🔍 VERSION_33 =", os.getenv("VERSION_33"))

class FileComparator:
    def __init__(self):
        self.version_32_path = VERSION_32_PATH
        self.version_33_path = VERSION_33_PATH

    def get_project_files(self, project_path):
        db = und.open(project_path)
        files = set()

        for ent in db.ents("File"):
            path = ent.name()
            if path.endswith(".java"):
                filename = os.path.basename(path)
                files.add(filename)

        return files

    def compare_files(self):
        files_32 = self.get_project_files(self.version_32_path)
        files_33 = self.get_project_files(self.version_33_path)

        # ✅ Print total counts
        print(f"📦 Total project-defined .java files in version 3.2: {len(files_32)}")
        print(f"📦 Total project-defined .java files in version 3.3: {len(files_33)}")

        # ✅ Compare differences
        only_in_32 = sorted(files_32 - files_33)
        only_in_33 = sorted(files_33 - files_32)

        if only_in_32:
            print("\n📁 Files only in version 3.2:")
            for file in only_in_32:
                print(f" - {file}")

        if only_in_33:
            print("\n📁 Files only in version 3.3:")
            for file in only_in_33:
                print(f" - {file}")

        if not only_in_32 and not only_in_33:
            print("\n✅ No file differences — all .java files match between versions.")

# Run it
if __name__ == "__main__":
    comparator = FileComparator()
    comparator.compare_files()
