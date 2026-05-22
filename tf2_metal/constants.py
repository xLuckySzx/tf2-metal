from enum import Enum

WEAPONS_PER_SCRAP: int = 2
WEAPONS_PER_RECLAIMED: int = 6
WEAPONS_PER_REF: int = 18

class RoundingMode(Enum):
    ROUND = "round"
    FLOOR = "floor"
    CEIL = "ceil"
