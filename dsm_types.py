from dataclasses import dataclass
from typing import Iterable, List, Tuple

@dataclass
class CNode:
    class_id: int
    score:    int
    pocket:   int

class Entity:
    def __init__(self, nodes: Iterable[CNode]):
        self.nodes: List[CNode] = list(nodes)

    def ids(self) -> List[int]:
        return [n.class_id for n in self.nodes]

    def pockets(self) -> List[int]:
        return [n.pocket for n in self.nodes]

    def exclude(self, *others: 'Entity') -> 'Entity':
        to_exclude = {cid for ent in others for cid in ent.ids()}
        return Entity(n for n in self.nodes if n.class_id not in to_exclude)

    def that(self, deps, other: 'Entity', dsm: 'DSMDataStructure') -> 'Entity':
        deps_list = deps if isinstance(deps, list) else [deps]
        keep = []
        for n in self.nodes:
            if set(dsm.dependencies(n.class_id, *deps_list)).intersection(other.ids()):
                keep.append(n)
        return Entity(keep)

    def thatIs(self, deps, other_or_dsm, maybe_dsm=None) -> 'Entity':
        # Overloads:
        #  thatIs(deps, dsm)
        #  thatIs(deps, other, dsm)
        deps_list = deps if isinstance(deps, list) else [deps]
        if maybe_dsm is None:
            dsm = other_or_dsm
            keep = [n for n in self.nodes
                    if dsm.dependents(n.class_id, *deps_list)]
        else:
            other, dsm = other_or_dsm, maybe_dsm
            keep = [n for n in self.nodes
                    if set(dsm.dependents(n.class_id, *deps_list)).intersection(other.ids())]
        return Entity(keep)

    def andIn(self, other: 'Entity') -> 'Entity':
        ids = set(other.ids())
        return Entity(n for n in self.nodes if n.class_id in ids)

    def superClasses(self, other: 'Entity') -> 'Entity':
        pockets = set(other.pockets())
        return Entity(n for n in self.nodes if n.pocket in pockets)

    subClasses = superClasses  # alias

    def __repr__(self):
        return f"Entity({self.nodes})"

_next_pocket = 0
def next_pocket() -> int:
    global _next_pocket
    _next_pocket += 1
    return _next_pocket

def tuple_list_as_entities(pairs: List[Tuple[int,int]]) -> Tuple[Entity,Entity]:
    """
    Port of _TupleList.asEntities:
    group by first component, assign each group a new pocket,
    then map to two Entity lists.
    """
    grouped = {}
    for a, b in pairs:
        grouped.setdefault(a, []).append(b)
    sub_nodes, sup_nodes = [], []
    for class_id, cols in grouped.items():
        pocket = next_pocket()
        sub_nodes.append(CNode(class_id, 0, pocket))
        for c in cols:
            sup_nodes.append(CNode(c, 0, pocket))
    return Entity(sub_nodes), Entity(sup_nodes)

def in_groups(sub: Entity, sup: Entity):
    """
    Port of _EntityTuple.inGroups:
    re–group the two lists by matching pocket numbers.
    Returns (new_sub, new_sup).
    """
    # map sup by class_id → list of CNode
    grouped = {}
    for n in sup.nodes:
        grouped.setdefault(n.class_id, []).append(n)
    new_sub, new_sup = [], []
    for class_id, sup_nodes in grouped.items():
        pocket = sup_nodes[0].pocket
        new_sup.append(CNode(class_id, 0, pocket))
        # find all sub with this pocket
        for n in sub.nodes:
            if n.pocket == pocket:
                new_sub.append(CNode(n.class_id, 0, pocket))
    return Entity(new_sub), Entity(new_sup)