import understand

def find(db):
    """
    Detect Adapter pattern instances in the Understand database.
    Returns a dict with key 'adapter' mapping to a list of matches.
    Each match is a dict: {'adapter': ..., 'target': ..., 'adaptee': ...}
    """
    results = []
    # Iterate over all classes in the database
    for cls in db.ents("Class ~ *"):
        # Look for interfaces this class implements
        targets = []
        for ref in cls.refs("Inheritance"):
            if ref.kindname() == "Implements":
                iface = ref.ent()
                if iface.kind() == "interface":
                    targets.append(iface)
        if not targets:
            continue

        # Find member variables declared in this class
        for var_ref in cls.refs("Define", "Variable"):
            var_ent = var_ref.ent()
            var_type = var_ent.type()
            if not var_type:
                continue
            # Lookup class entity for the variable type
            adaptees = db.lookup(var_type, "Class")
            if not adaptees:
                continue

            for adaptee in adaptees:
                # Skip if adaptee also implements the target interface
                if any(r.ent() == targets[0] for r in adaptee.refs("Inheritance")):
                    continue
                # Record a potential adapter match
                results.append({
                    "adapter": cls.longname(),
                    "target": targets[0].longname(),
                    "adaptee": adaptee.longname()
                })
    return {"adapter": results}