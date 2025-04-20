import understand

def find(db):
    """
    Detect Strategy pattern via createSocket strategy injection:
    - Finds classes with a field of type SocketFactory
    - Looks for calls to createSocket() in any method
    Returns { 'strategy': [ {context, strategy_interface, field, usage_methods} ] }
    """
    results = []
    for cls in db.ents("Class"):
        # find factory fields
        fields = [(f.name(), f.type(), f.longname())
                  for f in cls.ents("Define", "Member") if f.type() and "SocketFactory" in f.type()]
        if not fields:
            continue
        # find methods using createSocket
        usage_methods = []
        for m in cls.ents("Define", "Method"):
            for ref in m.refs("Call"):
                ent = ref.ent()
                if ent and ent.name() == "createSocket":
                    usage_methods.append(m.longname())
                    break
        if usage_methods:
            # pick first field
            name, iface, fullname = fields[0]
            results.append({
                'context': cls.longname(),
                'strategy_interface': iface,
                'field': fullname,
                'usage_methods': usage_methods
            })
    return {"strategy": results}
