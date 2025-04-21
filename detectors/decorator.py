# detectors/decorator.py

from dependency_type import DependencyType
from dsm_types import CNode, Entity, tuple_list_as_entities
from dsm import DSMDataStructure
from detectors.factory import _in_groups

def find_decorator(dsm: DSMDataStructure) -> dict:
    """
    Port of Praso‑DPD's _decorator:
      val (sub, sup) = dsm.SPECIALIZE.asEntities.inGroups
      val decorator       = sup andIn sub
      val concDecorator   = decorator subClasses sub
      val component       = decorator superClasses sup
      val concComponent   = component.subClasses(sub).exclude(decorator, concDecorator)
      // + rule: require at least one concrete decorator pocket
    """
    # Build SPECIALIZE = EXTEND ++ IMPLEMENT pairs
    spec_pairs = dsm.EXTEND() + dsm.IMPLEMENT()
    sub, sup = tuple_list_as_entities(spec_pairs)
    sub, sup = _in_groups(sub, sup)

    decorator       = sup.andIn(sub)
    conc_decorator  = decorator.subClasses(sub)
    component       = decorator.superClasses(sup)
    conc_component  = component.subClasses(sub).exclude(decorator, conc_decorator)

    # final check: we only declare a decorator pattern if there's at least one concrete decorator
    if not conc_decorator.nodes:
        return {
            "Component":          [],
            "Decorator":          [],
            "Concrete Component": [],
            "Concrete Decorator": []
        }

    return {
        "Component":          [dsm.files[n.class_id] for n in component.nodes],
        "Decorator":          [dsm.files[n.class_id] for n in decorator.nodes],
        "Concrete Component": [dsm.files[n.class_id] for n in conc_component.nodes],
        "Concrete Decorator": [dsm.files[n.class_id] for n in conc_decorator.nodes],
    }