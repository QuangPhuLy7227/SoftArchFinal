def find(db):
    results = []
    for cls in db.ents("Class"):
        methods = cls.ents("Define", "Method")
        factory_methods = [m.name() for m in methods if m.name().lower().startswith("create")]
        return_types = [m.type() for m in methods]

        for m, ret in zip(factory_methods, return_types):
            if ret and ret in cls.name():
                results.append({
                    "class": cls.longname(),
                    "factory_method": m,
                    "return_type": ret
                })

    return {"factory": results}
