import pytest
from tf2_metal.constants import (
    WEAPONS_PER_SCRAP,
    WEAPONS_PER_RECLAIMED,
    WEAPONS_PER_REF,
    RoundingMode
)

def test_constants_values():
    assert WEAPONS_PER_SCRAP == 2
    assert WEAPONS_PER_RECLAIMED == 6
    assert WEAPONS_PER_REF == 18

def test_rounding_mode_enum():
    assert hasattr(RoundingMode, "ROUND")
    assert hasattr(RoundingMode, "FLOOR")
    assert hasattr(RoundingMode, "CEIL")
    
    assert RoundingMode.ROUND.value == "round"
    assert RoundingMode.FLOOR.value == "floor"
    assert RoundingMode.CEIL.value == "ceil"

def test_module_constants_immutability():
    from tf2_metal.constants import WEAPONS_PER_SCRAP
    WEAPONS_PER_SCRAP = 99
    
    import tf2_metal.constants
    assert tf2_metal.constants.WEAPONS_PER_SCRAP == 2
