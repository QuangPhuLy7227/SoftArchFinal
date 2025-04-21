import understand
from itertools import combinations

# === CONFIG SECTION ===
UND_FILE = r"C:\Users\Owner\Downloads\commons-net-3.2-src\commons-net-3.2-src\commons-net-3.2-src.und"
SELECTED_CLASSES = ["DefaultFTPFileEntryParserFactoryTest", "DefaultFTPFileEntryParserFactory"]
# =======================

# Open the Understand database
db = understand.open(UND_FILE)

# Load all entities that are class or interface
all_entities = [ent for ent in db.ents() if ent.kind().check("Class") or ent.kind().check("Interface")]

print("=== Check: Are there ANY class/interface entities? ===")
print(f"Total: {len(all_entities)}")

print("\n=== Debug: Listing all class-like entities with their short names ===")
for ent in all_entities:
    print(f"Full: {ent.name()} → Short: {ent.name().split('.')[-1]}")

# Helper to match short class name
def find_entity_by_short_name(short_name):
    for ent in all_entities:
        if ent.name().endswith(f".{short_name}") or ent.name() == short_name:
            return ent
    return None

# Resolve selected classes
class_entities = {}
for cls in SELECTED_CLASSES:
    ent = find_entity_by_short_name(cls)
    if ent:
        class_entities[cls] = ent
    else:
        print(f"⚠️  Warning: Could not find class: {cls}")

# Debug: List all refs from class A
print(f"\n=== ALL refs from {SELECTED_CLASSES[0]} ===")
classA = class_entities.get(SELECTED_CLASSES[0])
if classA:
    for ref in classA.refs():
        try:
            print(f"[{ref.kind().name()}] {ref.ent().kind().name():<15} → {ref.ent().longname()}")
        except Exception as e:
            print(f"[{ref.kind().name()}] (Invalid entity): {e}")

# Analyze relationships
relationships = []
resolved_classes = list(class_entities.keys())

for classA_name, classB_name in combinations(resolved_classes, 2):
    classA = class_entities[classA_name]
    classB = class_entities[classB_name]

    found = False

    # === Generalization / Inheritance or Implementation ===
    for ref in classA.refs("Extendby"):
        if ref.ent().longname() == classB.longname():
            relationships.append(f"{classA_name} inherits from {classB_name} (Generalization)")
            found = True
    for ref in classA.refs("Implementby"):
        if ref.ent().longname() == classB.longname():
            relationships.append(f"{classA_name} implements {classB_name} (Implementation)")
            found = True

    for ref in classB.refs("Extendby"):
        if ref.ent().longname() == classA.longname():
            relationships.append(f"{classB_name} inherits from {classA_name} (Generalization)")
            found = True
    for ref in classB.refs("Implementby"):
        if ref.ent().longname() == classA.longname():
            relationships.append(f"{classB_name} implements {classA_name} (Implementation)")
            found = True

    # === Association ===
    for ref in classA.refs("Useby"):
        if ref.ent().longname() == classB.longname():
            relationships.append(f"{classA_name} uses {classB_name} (Association)")
            found = True
    for ref in classB.refs("Useby"):
        if ref.ent().longname() == classA.longname():
            relationships.append(f"{classB_name} uses {classA_name} (Association)")
            found = True

    # === Dependency (method call or object use) ===
    for kind in ["Call", "Use", "Set", "Define", "Couple"]:
        for ref in classA.refs(kind):
            target_ent = ref.ent()
            if target_ent.longname() == classB.longname():
                relationships.append(f"{classA_name} depends on {classB_name} (Dependency)")
                found = True
            elif target_ent.parent() and target_ent.parent().longname() == classB.longname():
                relationships.append(f"{classA_name} depends on {classB_name} (Dependency)")
                found = True

    for kind in ["Call", "Use", "Set", "Define", "Couple"]:
        for ref in classB.refs(kind):
            target_ent = ref.ent()
            if target_ent.longname() == classA.longname():
                relationships.append(f"{classB_name} depends on {classA_name} (Dependency)")
                found = True
            elif target_ent.parent() and target_ent.parent().longname() == classA.longname():
                relationships.append(f"{classB_name} depends on {classA_name} (Dependency)")
                found = True

    if not found:
        relationships.append(f"{classA_name} and {classB_name} have no direct relationship")

# Output
print("\n=== Class Relationship Report ===")
for r in relationships:
    print(" -", r)