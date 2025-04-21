import understand

# List of common command method names
COMMAND_METHOD_NAMES = {"execute", "run", "perform", "doAction"}

def is_command_interface(cls):
    """Detect a potential Command interface or abstract class."""
    if not (cls.kind().check("Interface") or cls.kind().check("Abstract")):
        return False

    for m in cls.ents("Define", "Function"):
        if m.name().lower() in COMMAND_METHOD_NAMES:
            return True
    return False

def find(db):
    results = []

    for cls in db.ents("Class, Interface"):
        if not is_command_interface(cls):
            continue

        command_interface = cls
        command_interface_name = command_interface.longname()

        concrete_commands = []
        invokers = set()

        for candidate in db.ents("Class"):
            # Check if candidate implements the command interface
            if not any(
                ref.ent() and ref.ent().longname() == command_interface_name
                for ref in candidate.refs("Extend", "Class, Interface")
            ):
                continue

            # Check if candidate defines a valid command method
            defines_command_method = any(
                m.name().lower() in COMMAND_METHOD_NAMES
                for m in candidate.ents("Define", "Function")
            )

            if defines_command_method:
                concrete_commands.append(candidate.longname())

                # Find classes that call its command method
                for method in candidate.ents("Define", "Function"):
                    if method.name().lower() not in COMMAND_METHOD_NAMES:
                        continue
                    call_refs = method.refs("Callby", "Function", True)
                    for ref in call_refs:
                        caller_cls = ref.ent().parent()
                        if caller_cls and caller_cls.kind().check("Class"):
                            invokers.add(caller_cls.longname())

        if concrete_commands:
            results.append({
                "command_interface": command_interface_name,
                "concrete_commands": sorted(set(concrete_commands)),
                "invokers": sorted(invokers),
            })

    return {"command": results}
