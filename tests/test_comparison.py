import pytest
from tf2_metal.currency import TF2Currency

def test_gt():
    assert TF2Currency(metal=2.0) > TF2Currency(metal=1.0)

def test_lt():
    assert TF2Currency(metal=1.0) < TF2Currency(metal=2.0)

def test_eq():
    assert TF2Currency(metal=1.0) == TF2Currency(metal=1.0)

def test_ne():
    assert TF2Currency(metal=1.0) != TF2Currency(metal=2.0)

def test_ge():
    assert TF2Currency(metal=1.0) >= TF2Currency(metal=1.0)
    assert TF2Currency(metal=2.0) >= TF2Currency(metal=1.0)

def test_le():
    assert TF2Currency(metal=1.0) <= TF2Currency(metal=1.0)
    assert TF2Currency(metal=1.0) <= TF2Currency(metal=2.0)

def test_negative_comparison():
    assert TF2Currency(metal=-1.0) < TF2Currency(metal=1.0)

def test_type_error_lt():
    with pytest.raises(TypeError):
        _ = TF2Currency(metal=1.0) < 5

def test_type_error_gt():
    with pytest.raises(TypeError):
        _ = TF2Currency(metal=1.0) > "stringa"
