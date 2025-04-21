import understand

def find(db):
    results = []

    for cls in db.ents("Class"):
        if cls.name() != "SocketClient":
            continue

        print(f"🔍 Analyzing class: {cls.longname()}")

        fields = cls.ents("Define", "Variable Member")
        delegates = set()
        forwarded_methods = set()
        field_type_map = {}

        for field in fields:
            try:
                field_type = field.type()
                field_longname = field_type.longname() if hasattr(field_type, "longname") else field_type

                print(f"  🧩 Field: {field.name()} → Type: {field_longname}")

                if not field_longname or field_longname == cls.longname():
                    continue

                field_type_ents = db.lookup(field_longname, "Class Interface")
                if not field_type_ents:
                    print(f"    ❌ No matching type found in lookup for {field_longname}")
                    continue

                field_type_ent = field_type_ents[0]
                delegates.add(field_type_ent.longname())
                field_type_map[field.name()] = field_type_ent.longname()
            except Exception as e:
                print(f"    ⚠️ Field error: {e}")
                continue

        for method in cls.ents("Define", "Function"):
            for call in method.refs("Call", "Function"):
                try:
                    callee = call.ent()
                    if not callee:
                        continue

                    parent = callee.parent()
                    if parent and parent.kind().check("class interface"):
                        parent_name = parent.longname()
                        if parent_name in delegates:
                            print(f"    🔁 Forwarded call: {callee.name()} → {parent_name}")
                            forwarded_methods.add(callee.name())
                except Exception as e:
                    print(f"    ⚠️ Call error: {e}")
                    continue

            for ref in method.refs("Use"):
                ent = ref.ent()
                if ent and ent.kind().check("Variable Member"):
                    field_name = ent.name()
                    if field_name in field_type_map:
                        delegated_class = field_type_map[field_name]
                        delegates.add(delegated_class)

        if delegates:
            print(f"✅ Proxy detected: {cls.longname()} delegates to {delegates}")
            results.append({
                "proxy_class": cls.longname(),
                "delegates_to": list(delegates),
                "forwarded_methods": list(forwarded_methods)
            })

    return {"proxy": results}
