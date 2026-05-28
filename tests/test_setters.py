import pytest
from tf2_metal.currency import TF2Currency
from tf2_metal.exceptions import TF2ValidationError

def test_set_key_price_metal_success():
    curr = TF2Currency(key_price_ref=66.33)
    assert curr.key_price_ref == 66.33

def test_set_key_price_metal_negative():
    with pytest.raises(TF2ValidationError):
        TF2Currency(key_price_ref=-1.0)

def test_set_key_price_metal_inf():
    with pytest.raises(TF2ValidationError):
        TF2Currency(key_price_ref=float('inf'))

def test_set_key_price_metal_nan():
    with pytest.raises(TF2ValidationError):
        TF2Currency(key_price_ref=float('nan'))


def test_set_key_price_usd_success():
    curr = TF2Currency(key_price_usd=2.49)
    assert curr.key_price_usd == 2.49

def test_set_key_price_usd_negative():
    with pytest.raises(TF2ValidationError):
        TF2Currency(key_price_usd=-1.0)

def test_set_key_price_usd_inf():
    with pytest.raises(TF2ValidationError):
        TF2Currency(key_price_usd=float('inf'))

def test_set_key_price_usd_nan():
    with pytest.raises(TF2ValidationError):
        TF2Currency(key_price_usd=float('nan'))

def test_arithmetic_different_prices():
    c1 = TF2Currency(keys=1, key_price_ref=60.0)
    c2 = TF2Currency(keys=1, key_price_ref=70.0)
    with pytest.raises(TF2ValidationError):
        _ = c1 + c2
    with pytest.raises(TF2ValidationError):
        _ = c1 - c2

def test_arithmetic_one_zero_price():
    c1 = TF2Currency(keys=1, key_price_ref=60.0)
    c2 = TF2Currency(metal=10.0, key_price_ref=0.0)
    c3 = c1 + c2
    assert c3.key_price_ref == 60.0
    assert c3._weapons == c1._weapons + c2._weapons
