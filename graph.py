import understand

# === CONFIG SECTION ===
UND_FILE = r"C:\Users\Owner\Downloads\commons-net-3.2-src\commons-net-3.2-src\commons-net-3.2-src.und"
# SELECTED_CLASSES = ["EventListener", "CopyStreamListener", "CopyStreamAdapter"]  # Add your target classes
SELECTED_CLASSES = ["DefaultFTPFileEntryParserFactoryTest", "DefaultFTPFileEntryParserFactory"]
OUTPUT_FILE = "class_diagram.puml"
# =======================

db = understand.open(UND_FILE)
output = ["@startuml"]

selected_set = set(SELECTED_CLASSES)

for cls in db.ents("class"):
    cls_name = cls.name()
    if cls_name not in selected_set:
        continue

    output.append(f"class {cls_name} {{")

    # Add attributes (fields)
    for ref in cls.refs("Define", "Variable"):
        if ref.ent().kind().check("Variable"):
            output.append(f"    +{ref.ent().name()}")

    # Add methods
    for ref in cls.refs("Define", "Function"):
        if ref.ent().kind().check("Function"):
            output.append(f"    +{ref.ent().name()}()")

    output.append("}")

    # Inheritance
    for parent in cls.refs("Extendby"):
        parent_name = parent.ent().name()
        if parent_name in selected_set:
            output.append(f"{cls_name} --|> {parent_name}")

    # Associations: has-a (e.g., member variable type)
    for ref in cls.refs("Useby"):
        target = ref.ent()
        if target.kind().check("class") and target.name() in selected_set:
            output.append(f"{cls_name} --> {target.name()} : uses")

    # Method calls to other selected classes (e.g., A.method() calls B.method())
    for ref in cls.refs("Call"):
        callee_cls = ref.ent().parent()
        if callee_cls and callee_cls.name() in selected_set and callee_cls.name() != cls_name:
            output.append(f"{cls_name} ..> {callee_cls.name()} : calls")

output.append("@enduml")

with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(output))

print(f"✅ PlantUML diagram saved to {OUTPUT_FILE}")