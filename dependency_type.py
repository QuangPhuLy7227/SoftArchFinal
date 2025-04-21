from enum import Enum, auto

class DependencyType(Enum):
    TYPED     = 1 << 0
    USE       = 1 << 1
    IMPLEMENT = 1 << 2
    EXTEND    = 1 << 3
    CALL      = 1 << 4
    SET       = 1 << 5
    IMPORT    = 1 << 6
    CREATE    = 1 << 7
    CAST      = 1 << 8
    THROW     = 1 << 9
    MODIFY    = 1 << 10