# import understand

# def find(db):
#     """
#     Detect Observer pattern instances generically in the Understand database.
#     Returns { 'observer': [ {subject, listener_interface, add_methods, remove_methods, fields} ] }
#     """
#     results = []
#     # Iterate all classes
#     for cls in db.ents("Class"):
#         # 1) find addXListener methods
#         add_methods = [m for m in cls.ents("Define","Method")
#                        if m.name().startswith("add") and "Listener" in m.name()]
#         # 2) find removeXListener methods
#         remove_methods = [m for m in cls.ents("Define","Method")
#                           if m.name().startswith("remove") and "Listener" in m.name()]
#         if not add_methods or not remove_methods:
#             continue

#         # 3) infer listener interface type from first add method's signature
#         params = add_methods[0].parameters() or []
#         listener_interface = None
#         for p in params:
#             parts = p.split()
#             for part in parts:
#                 if part.endswith("Listener"):
#                     listener_interface = part
#                     break
#             if listener_interface:
#                 break
#         if not listener_interface:
#             listener_interface = "<unknown>"

#         # 4) find fields that hold listeners
#         fields = [f for f in cls.ents("Define","Member")
#                   if (f.type() and (listener_interface in f.type() or "ListenerList" in f.type()))]
#         if not fields:
#             continue

#         results.append({
#             "subject": cls.longname(),
#             "listener_interface": listener_interface,
#             "add_methods": [m.longname() for m in add_methods],
#             "remove_methods": [m.longname() for m in remove_methods],
#             "fields": [f.longname() for f in fields]
#         })
#     return {"observer": results}

# detectors/observer.py

# # detectors/observer.py
# from dsm_types import CNode, Entity
# from dependency_type import DependencyType

# def find(dsm):
#     """
#     A very naive Observer‐like detector:
#       - we look for a “Subject” class that ‘calls’/depends on an interface
#       - then a “Concrete Observer” that depends on that interface
#       (here we collapse all dependency‐kinds into the same buckets)
#     """
#     # build a simple pocket for each file
#     nodes = [CNode(i, 0, i) for i in range(dsm.size)]
#     all_ent = Entity(nodes)

#     # pretend the “interface” is any class with >0 dependents
#     iface = Entity([n for n in nodes if dsm.dependents(n.class_id)])
#     # concrete observer: those who depend on the interface
#     con_obs = Entity([n for n in nodes
#                       if set(dsm.dependencies(n.class_id)).intersection(iface.ids())])
#     # subject: those that depend (call/use) the interface
#     subj = con_obs  # in this stub, we just reuse con_obs

#     return {
#         "Observer Interface":   [dsm.files[n.class_id] for n in iface.nodes],
#         "Concrete Observer":    [dsm.files[n.class_id] for n in con_obs.nodes],
#         "Subject":              [dsm.files[n.class_id] for n in subj.nodes],
#     }

from dependency_type       import DependencyType
from dsm_types             import tuple_list_as_entities, in_groups

def find(dsm):
    # SPECIALIZE := EXTEND ∪ IMPLEMENT
    ext  = dsm.dependency_pair(DependencyType.EXTEND)
    impl = dsm.dependency_pair(DependencyType.IMPLEMENT)
    spec = list({*ext, *impl})

    sub0, sup0 = tuple_list_as_entities(spec)
    sub, sup   = in_groups(sub0, sup0)

    # Observer Interface: those sup nodes typed or used by someone
    obsI = sup.thatIs([DependencyType.TYPED, DependencyType.USE], dsm)

    # Concrete Observer: subclasses of obsI within sub
    conO = obsI.subClasses(sub)

    # Subject: those that *use* or *type* obsI
    from dsm import load_dsm  # noqa
    pairs = dsm.classes_that([DependencyType.TYPED, DependencyType.USE], obsI)
    subj, _ = tuple_list_as_entities(pairs)

    return {
      "Observer Interface": [dsm.files[n.class_id] for n in obsI.nodes],
      "Concrete Observer":  [dsm.files[n.class_id] for n in conO.nodes],
      "Subject":            [dsm.files[n.class_id] for n in subj.nodes],
    }