# # dsm.py
# import csv
# from typing import List, Tuple
# from dsm_types import CNode
# from dependency_type import DependencyType

# class DSMDataStructure:
#     def __init__(self,
#                  files: List[str],
#                  adjMatrix: List[List[Tuple[int,int]]]
#                 ):
#         self.files = files
#         self.adjMatrix = adjMatrix
#         self.size = len(files)

#     def dependencies(self, class_id: int, *deps: DependencyType) -> List[int]:
#         # ignore deps‐filter for CSV; just return all targets
#         return [col for (_count,col) in self.adjMatrix[class_id]]

#     def dependents(self, class_id: int, *deps: DependencyType) -> List[int]:
#         rows = []
#         for r, row in enumerate(self.adjMatrix):
#             if any(col == class_id for (_count,col) in row):
#                 rows.append(r)
#         return rows

# def load_dsm(path: str) -> DSMDataStructure:
#     """
#     Loads a CSV of the form Understand -dependencies csv matrix:
#       first row → header: Dependent File, f1.java, f2.java, …
#       each subsequent row: rowfile, count_1, count_2, …
#     any count>0 → we record a dependency (1, col_index).
#     """
#     with open(path, newline='') as f:
#         reader = csv.reader(f)
#         rows = list(reader)

#     # header
#     files = rows[0][1:]
#     matrix = []
#     for row in rows[1:]:
#         counts = row[1:]
#         deps = []
#         for idx, cell in enumerate(counts):
#             try:
#                 if int(cell) > 0:
#                     deps.append((int(cell), idx))
#             except ValueError:
#                 continue
#         matrix.append(deps)

#     return DSMDataStructure(files, matrix)

# dsm.py

import csv
from dependency_type import DependencyType

class DSMDataStructure:
    def __init__(self, files, matrix):
        self.files  = files               # List[str], one per ROW
        self.size   = len(files)
        self.matrix = matrix              # List[List[(bitmask:int, col:int)]]

    @classmethod
    def load_csv(cls, path):
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)  
            targets = header[1:]      # we keep targets for column‐IDs but don’t use them as `files`
            files = []
            matrix = []
            for row in reader:
                src = row[0]
                bits = row[1:]
                files.append(src)
                row_list = []
                for j, cell in enumerate(bits):
                    cell = cell.strip()
                    if cell and cell != '0':
                        b = int(cell)
                        row_list.append((b, j))
                matrix.append(row_list)
        return cls(files, matrix)

    def dependencies(self, class_id, *deps):
        row = self.matrix[class_id]
        if not deps:
            return [col for b, col in row]
        mask = sum(d.value for d in deps)
        return [col for b, col in row if (b & mask) != 0]

    def dependents(self, class_id, *deps):
        mask = sum(d.value for d in deps) if deps else None
        result = []
        for i, row in enumerate(self.matrix):
            for b, col in row:
                if col == class_id and (mask is None or (b & mask) != 0):
                    result.append(i)
        return result

    def dependency_pair(self, *deps):
        mask = sum(d.value for d in deps)
        pairs = []
        for i, row in enumerate(self.matrix):
            for b, col in row:
                if (b & mask) != 0:
                    pairs.append((i, col))
        return pairs

    def classes_that(self, deps, entity):
        mask = sum(d.value for d in deps)
        pairs = []
        for i, row in enumerate(self.matrix):
            for b, col in row:
                if (b & mask) != 0 and col in entity.ids():
                    pairs.append((i, col))
        return pairs
    
    def EXTEND(self):      return self.dependency_pair(DependencyType.EXTEND)
    def IMPLEMENT(self):   return self.dependency_pair(DependencyType.IMPLEMENT)

def load_dsm(path):
    return DSMDataStructure.load_csv(path)