import pytest
from tf2_metal.currency import TF2Currency
from tf2_metal.constants import RoundingMode

def test_add_positive():
    a = TF2Currency(metal=1.0)
    b = TF2Currency(metal=2.0)
    c = a + b
    assert c._weapons == a._weapons + b._weapons

def test_sub_positive():
    a = TF2Currency(metal=3.0)
    b = TF2Currency(metal=1.0)
    c = a - b
    assert c._weapons == 36

def test_sub_negative():
    a = TF2Currency(metal=1.0)
    b = TF2Currency(metal=3.0)
    c = a - b
    assert c._weapons == -36

def test_rounding_mode_preserved():
    a = TF2Currency(metal=1.0, rounding_mode=RoundingMode.FLOOR)
    b = TF2Currency(metal=2.0)
    c = a + b
    assert c.rounding_mode == RoundingMode.FLOOR
    
    d = a - b
    assert d.rounding_mode == RoundingMode.FLOOR

def test_add_not_implemented():
    a = TF2Currency(metal=1.0)
    with pytest.raises(TypeError):
        _ = a + 5

def test_sub_not_implemented():
    a = TF2Currency(metal=1.0)
    with pytest.raises(TypeError):
        _ = a - "ciao"

def test_add_zero():
    a = TF2Currency(metal=1.33)
    b = TF2Currency()
    c = a + b
    assert c._weapons == a._weapons
    assert c is not a

def test_new_instance():
    a = TF2Currency(metal=1.0)
    b = TF2Currency(metal=1.0)
    c = a + b
    assert c is not a
    assert c is not b
