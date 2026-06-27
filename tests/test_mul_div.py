import math
import pytest
from tf2_metal.currency import TF2Currency
from tf2_metal.constants import RoundingMode
from tf2_metal.exceptions import TF2ValidationError

def test_mul_positive_int():
    a = TF2Currency(metal=1.0)
    b = a * 3
    assert b.to_weapons(66.0) == 54

def test_mul_positive_float_rounding():
    a = TF2Currency(metal=1.0, rounding_mode=RoundingMode.ROUND)
    assert (a * 1.5).to_weapons(66.0) == 27
    assert (a * 1.4).to_weapons(66.0) == 25
    
    b = TF2Currency(metal=1.0, rounding_mode=RoundingMode.FLOOR)
    assert (b * 1.4).to_weapons(66.0) == 25
    
    c = TF2Currency(metal=1.0, rounding_mode=RoundingMode.CEIL)
    assert (c * 1.4).to_weapons(66.0) == 26

def test_mul_negative():
    a = TF2Currency(metal=1.0)
    b = a * -1
    assert b.to_weapons(66.0) == -18

def test_mul_zero():
    a = TF2Currency(metal=1.0)
    b = a * 0
    assert b.to_weapons(66.0) == 0

def test_rmul():
    a = TF2Currency(metal=1.0)
    assert (2 * a).to_weapons(66.0) == (a * 2).to_weapons(66.0)

def test_div_positive_int():
    a = TF2Currency(metal=2.0)
    b = a / 2
    assert b.to_weapons(66.0) == 18

def test_div_positive_float_rounding():
    a = TF2Currency(metal=1.0, rounding_mode=RoundingMode.ROUND)
    assert (a / 1.5).to_weapons(66.0) == 12
    assert (a / 1.4).to_weapons(66.0) == 13
    
    b = TF2Currency(metal=1.0, rounding_mode=RoundingMode.FLOOR)
    assert (b / 1.4).to_weapons(66.0) == 12
    
    c = TF2Currency(metal=1.0, rounding_mode=RoundingMode.CEIL)
    assert (c / 1.4).to_weapons(66.0) == 13

def test_div_zero():
    a = TF2Currency(metal=1.0)
    with pytest.raises(TF2ValidationError):
        _ = a / 0
    with pytest.raises(TF2ValidationError):
        _ = a / 0.0

def test_mul_div_invalid_float():
    a = TF2Currency(metal=1.0)
    
    with pytest.raises(TF2ValidationError):
        _ = a * float('inf')
        
    with pytest.raises(TF2ValidationError):
        _ = a * float('nan')
        
    with pytest.raises(TF2ValidationError):
        _ = a / float('inf')
        
    with pytest.raises(TF2ValidationError):
        _ = a / float('nan')

def test_mul_type_error():
    a = TF2Currency(metal=1.0)
    with pytest.raises(TypeError):
        _ = a * "due"

def test_new_instance():
    a = TF2Currency(metal=1.0)
    b = a * 2
    c = a / 2
    assert a is not b
    assert a is not c
