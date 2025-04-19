import understand

def find(db):
    """
    Detect Observer pattern instances generically in the Understand database.
    Returns { 'observer': [ {subject, listener_interface, add_methods, remove_methods, fields} ] }
    """
    results = []
    # Iterate all classes
    for cls in db.ents("Class"):
        # 1) find addXListener methods
        add_methods = [m for m in cls.ents("Define","Method")
                       if m.name().startswith("add") and "Listener" in m.name()]
        # 2) find removeXListener methods
        remove_methods = [m for m in cls.ents("Define","Method")
                          if m.name().startswith("remove") and "Listener" in m.name()]
        if not add_methods or not remove_methods:
            continue

        # 3) infer listener interface type from first add method's signature
        params = add_methods[0].parameters() or []
        listener_interface = None
        for p in params:
            parts = p.split()
            for part in parts:
                if part.endswith("Listener"):
                    listener_interface = part
                    break
            if listener_interface:
                break
        if not listener_interface:
            listener_interface = "<unknown>"

        # 4) find fields that hold listeners
        fields = [f for f in cls.ents("Define","Member")
                  if (f.type() and (listener_interface in f.type() or "ListenerList" in f.type()))]
        if not fields:
            continue

        results.append({
            "subject": cls.longname(),
            "listener_interface": listener_interface,
            "add_methods": [m.longname() for m in add_methods],
            "remove_methods": [m.longname() for m in remove_methods],
            "fields": [f.longname() for f in fields]
        })
    return {"observer": results}