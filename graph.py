# import understand

# # === CONFIG SECTION ===
# UND_FILE = r"C:\Users\Owner\Downloads\commons-net-3.2-src\commons-net-3.2-src\commons-net-3.2-src.und"
# # SELECTED_CLASSES = ["EventListener", "CopyStreamListener", "CopyStreamAdapter"]  # Add your target classes
# SELECTED_CLASSES = ["DefaultFTPFileEntryParserFactoryTest", "DefaultFTPFileEntryParserFactory"]
# OUTPUT_FILE = "class_diagram.puml"
# # =======================

# db = understand.open(UND_FILE)
# output = ["@startuml"]

# selected_set = set(SELECTED_CLASSES)

# for cls in db.ents("class"):
#     cls_name = cls.name()
#     if cls_name not in selected_set:
#         continue

#     output.append(f"class {cls_name} {{")

#     # Add attributes (fields)
#     for ref in cls.refs("Define", "Variable"):
#         if ref.ent().kind().check("Variable"):
#             output.append(f"    +{ref.ent().name()}")

#     # Add methods
#     for ref in cls.refs("Define", "Function"):
#         if ref.ent().kind().check("Function"):
#             output.append(f"    +{ref.ent().name()}()")

#     output.append("}")

#     # Inheritance
#     for parent in cls.refs("Extendby"):
#         parent_name = parent.ent().name()
#         if parent_name in selected_set:
#             output.append(f"{cls_name} --|> {parent_name}")

#     # Associations: has-a (e.g., member variable type)
#     for ref in cls.refs("Useby"):
#         target = ref.ent()
#         if target.kind().check("class") and target.name() in selected_set:
#             output.append(f"{cls_name} --> {target.name()} : uses")

#     # Method calls to other selected classes (e.g., A.method() calls B.method())
#     for ref in cls.refs("Call"):
#         callee_cls = ref.ent().parent()
#         if callee_cls and callee_cls.name() in selected_set and callee_cls.name() != cls_name:
#             output.append(f"{cls_name} ..> {callee_cls.name()} : calls")

# output.append("@enduml")

# with open(OUTPUT_FILE, "w") as f:
#     f.write("\n".join(output))

# print(f"✅ PlantUML diagram saved to {OUTPUT_FILE}")

import understand
import os

# === CONFIG ===
UND_FILE = r"C:\Users\Owner\Downloads\commons-net-3.2-src\commons-net-3.2-src\commons-net-3.2-src.und"
SELECTED_CLASSES = [
    "SocketClient",
    "FTP",
    "SMTP",
    "POP3",
    "IMAP",
    "FTPClient",
    "SMTPClient",
    "POP3Client",
    "IMAPClient",
]
# SELECTED_CLASSES = ["CopyStreamAdapter", "CopyStreamListener"]
OUTPUT_FILE = "class_diagram_with_relationships.puml"
# ===============

db = understand.open(UND_FILE)
output = ["@startuml"]
selected_set = set(SELECTED_CLASSES)
processed_entities = set()
entity_map = {}

print("\U0001F4C4 Absolute paths of selected entities:")
for ent in db.ents():
    if ent.name() in selected_set:
        for ref in ent.refs("Define", "File"):
            file_ent = ref.file()
            if file_ent:
                abs_path = os.path.abspath(file_ent.name())
                print(f" - {ent.name()}: {abs_path}")
                break
print("")

# === First pass: create classes for any kind of entity ===
for ent in db.ents():
    name = ent.name()
    if name not in selected_set or name in processed_entities:
        continue

    processed_entities.add(name)
    entity_map[name] = ent

    output.append(f"class {name} {{")

    for var in ent.ents("Define", "Variable"):
        visibility = "+"
        if "private" in var.kind().name().lower() or var.simplename().startswith("_"):
            visibility = "-"
        elif "protected" in var.kind().name().lower():
            visibility = "#"
        output.append(f"    {visibility} {var.simplename()} : {var.type()}")

    for method in ent.ents("Define", "Method"):
        visibility = "+"
        kind = method.kind().name().lower()
        if "private" in kind:
            visibility = "-"
        elif "protected" in kind:
            visibility = "#"

        params = [f"{p.simplename()}: {p.type()}" for p in method.ents("Define", "Parameter")]
        output.append(f"    {visibility} {method.simplename()}({', '.join(params)}) : {method.type()}")

    output.append("}")

# === Second pass: all relationships with specific arrows ===
added_relationships = set()
for from_name, from_ent in entity_map.items():
    for to_name, to_ent in entity_map.items():
        if from_name == to_name:
            continue

        for kind in ["Call", "Use", "Set", "Define", "Couple", "Extendby", "Implementby"]:
            for ref in from_ent.refs(kind):
                target_ent = ref.ent()
                match = (
                    target_ent.longname() == to_ent.longname() or
                    (target_ent.parent() and target_ent.parent().longname() == to_ent.longname())
                )
                if match:
                    if kind == "Extendby":
                        relation = f"{from_name} --|> {to_name} : inherits"
                    elif kind == "Implementby":
                        relation = f"{from_name} ..|> {to_name} : implements"
                    elif kind == "Call":
                        relation = f"{from_name} --> {to_name} : calls"
                    elif kind == "Use":
                        relation = f"{from_name} ..> {to_name} : uses"
                    elif kind == "Set":
                        relation = f"{from_name} --> {to_name} : sets"
                    elif kind == "Define":
                        relation = f"{from_name} ..> {to_name} : defines"
                    elif kind == "Couple":
                        relation = f"{from_name} --> {to_name} : couples"
                    else:
                        continue

                    if relation not in added_relationships:
                        output.append(relation)
                        added_relationships.add(relation)

output.append("@enduml")

with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(output))

print(f"✅ UML class diagram saved to {os.path.abspath(OUTPUT_FILE)}")