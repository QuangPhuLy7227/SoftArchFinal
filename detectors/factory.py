# detectors/factory.py

from typing import Tuple
from dependency_type import DependencyType
from dsm_types import CNode, Entity, tuple_list_as_entities
from dsm import DSMDataStructure

def _in_groups(sub: Entity, sup: Entity) -> Tuple[Entity, Entity]:
    # port of Scala _EntityTuple.inGroups
    grouped = {}
    for n in sup.nodes:
        grouped.setdefault(n.class_id, []).append(n)
    e1, e2 = [], []
    for sup_id, sup_nodes in grouped.items():
        pocket = sup_nodes[0].pocket
        sup_pockets = [n.pocket for n in sup_nodes]
        # all sub-nodes whose pocket is in sup_pockets
        other = [n for n in sub.nodes if n.pocket in sup_pockets]
        # remap them to the same pocket
        remapped = [CNode(n.class_id, 0, pocket) for n in other]
        e2.extend(remapped)
        e1.append(CNode(sup_id, 0, pocket))
    return Entity(e2), Entity(e1)

def find_abstract_factory(dsm: DSMDataStructure) -> dict:
    # SPECIALIZE = EXTEND ++ IMPLEMENT
    spec_pairs = dsm.EXTEND() + dsm.IMPLEMENT()
    sub, sup = tuple_list_as_entities(spec_pairs)
    sub, sup = _in_groups(sub, sup)

    cf = sub.that(DependencyType.TYPED, sup, dsm)\
            .that(DependencyType.CREATE, sub, dsm)
    af = cf.superClasses(sup)
    ap = sup.thatIs(DependencyType.TYPED, af, dsm)
    cp = ap.subClasses(sub)

    return {
      "Abstract Factory": [dsm.files[n.class_id] for n in af.nodes],
      "Concrete Factory": [dsm.files[n.class_id] for n in cf.nodes],
      "Abstract Product": [dsm.files[n.class_id] for n in ap.nodes],
      "Concrete Product": [dsm.files[n.class_id] for n in cp.nodes],
    }

def find_factory_method(dsm: DSMDataStructure) -> dict:
    spec_pairs = dsm.EXTEND() + dsm.IMPLEMENT()
    sub, sup = tuple_list_as_entities(spec_pairs)
    sub, sup = _in_groups(sub, sup)

    cc = sub.that(DependencyType.TYPED, sup, dsm)\
            .that(DependencyType.CREATE, sub, dsm)
    creator = cc.superClasses(sup)
    ap = sup.thatIs(DependencyType.TYPED, creator, dsm)
    cp = ap.subClasses(sub)

    return {
      "Creator":            [dsm.files[n.class_id] for n in creator.nodes],
      "Concrete Creator":   [dsm.files[n.class_id] for n in cc.nodes],
      "Product":            [dsm.files[n.class_id] for n in ap.nodes],
      "Concrete Product":   [dsm.files[n.class_id] for n in cp.nodes],
    }