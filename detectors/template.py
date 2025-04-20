import understand

def find(db):
    """
    Enhanced Template Method detector:
    1) Primitive operations: methods declared abstract (or starting with get if abstract info unavailable).
    2) Template methods: concrete methods that either start with 'test' or call a primitive op.
    No class-level abstract restriction (applies to any class with abstract/primitives).
    Returns:
      { 'template': [ {template_class, primitive_operations, template_methods} ] }
    """
    results = []
    for cls in db.ents("Class"):
        methods = cls.ents("Define", "Method")
        if not methods:
            continue
        # 1) primitive operations: abstract methods
        primitive_ops = []
        for m in methods:
            if hasattr(m, 'isAbstract') and m.isAbstract():
                primitive_ops.append(m)
        # fallback: if no abstract methods, use get* naming
        if not primitive_ops:
            primitive_ops = [m for m in methods if m.name().startswith("get")]
        if not primitive_ops:
            continue
        # build set of primitive longnames
        prim_names = set(p.longname() for p in primitive_ops)

        # 2) template methods: concrete methods that start with test or call primitives
        template_methods = []
        for m in methods:
            # skip abstract
            if hasattr(m, 'isAbstract') and m.isAbstract():
                continue
            name = m.name()
            # name-based detection
            if name.lower().startswith("test"):
                template_methods.append(m)
                continue
            # call-based detection
            for ref in m.refs("Call") + m.refs("Callin"):
                ent = ref.ent()
                if ent and ent.longname() in prim_names:
                    template_methods.append(m)
                    break
        if not template_methods:
            continue
        results.append({
            'template_class': cls.longname(),
            'primitive_operations': [p.longname() for p in primitive_ops],
            'template_methods': [t.longname() for t in template_methods]
        })
    return {"template": results}