import understand

def find(db):
    """
    Detect Adapter pattern instances in the Understand database.
    Returns dict { 'adapter': [ {adapter, target, adaptee}... ] }
    """
    results = []
    # For every class, find interfaces it implements and member fields
    for cls in db.ents("Class"):
        # interfaces implemented
        impl_ifaces = [r.ent() for r in cls.refs("Inheritance") if r.kindname()=="Implements"]
        for iface in impl_ifaces:
            # fields in class
            for var in cls.ents("Define","Member"):
                var_type = var.type() or ""
                # lookup classes matching the field type
                adaptees = db.lookup(var_type, "Class")
                for adaptee in adaptees:
                    # skip if adaptee also implements the interface
                    if any(r.kindname()=="Implements" and r.ent()==iface for r in adaptee.refs("Inheritance")):
                        continue
                    results.append({
                        "adapter": cls.longname(),
                        "target": iface.longname(),
                        "adaptee": adaptee.longname()
                    })
    return {"adapter": results}