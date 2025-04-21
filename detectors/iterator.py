import understand

def is_iterator_class(cls):
    """Check if the class appears to implement Iterator pattern behavior."""
    method_names = set(m.name().lower() for m in cls.ents("Define", "Function"))

    has_core_methods = (
        "hasnext" in method_names and
        "next" in method_names and
        "remove" in method_names  # optional in Java 8+, but still a good hint
    )

    if has_core_methods:
        return True

    # Fallback: check if class extends/implements known iterator-related names
    for ref in cls.refs("Extend", "Class, Interface"):
        if ref.ent() and "iterator" in ref.ent().name().lower():
            return True

    return False

def find(db):
    results = []

    for cls in db.ents("Class"):
        class_name = cls.name().lower()

        # Heuristic 1: name contains "iterator"
        # Heuristic 2: structure matches typical Java iterator (hasNext, next, remove)
        if "iterator" in class_name or is_iterator_class(cls):
            method_names = sorted([m.name() for m in cls.ents("Define", "Function")])
            results.append({
                "iterator_class": cls.longname(),
                "methods": method_names
            })

    return {"iterator": results}
