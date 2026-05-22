import pytest
from tf2_metal.currency import TF2Currency
from tf2_metal.constants import RoundingMode
from tf2_metal.exceptions import TF2ValidationError

@pytest.fixture(autouse=True)
def reset_class_vars():
    yield
    TF2Currency.key_price_ref = 0.0

def test_from_string_metal_only():
    curr = TF2Currency.from_string("13.33 ref")
    assert curr.keys == 0
    assert curr.metal == 13.33

def test_from_string_keys_only():
    TF2Currency.set_key_price_metal(66.0)
    curr = TF2Currency.from_string("2 keys")
    assert curr.keys == 2
    assert curr.metal == 0.0

def test_from_string_keys_and_metal():
    TF2Currency.set_key_price_metal(66.0)
    curr = TF2Currency.from_string("2k, 5 ref")
    assert curr.keys == 2
    assert curr.metal == 5.0

def test_from_string_alternative_format():
    TF2Currency.set_key_price_metal(66.0)
    curr = TF2Currency.from_string("2 keys 1.33 metal")
    assert curr.keys == 2
    assert curr.metal == 1.33

def test_from_string_fractional_keys():
    TF2Currency.set_key_price_metal(66.0)
    curr = TF2Currency.from_string("1.5 keys")
    assert curr._weapons == 1782

def test_from_string_empty():
    with pytest.raises(TF2ValidationError):
        TF2Currency.from_string("")

def test_from_string_whitespace():
    with pytest.raises(TF2ValidationError):
        TF2Currency.from_string("   ")

def test_from_string_gibberish():
    with pytest.raises(TF2ValidationError):
        TF2Currency.from_string("gibberish xyz 123abc")

def test_from_string_keys_no_price():
    with pytest.raises(TF2ValidationError):
        TF2Currency.from_string("2 keys")

def test_from_string_rounding_mode():
    curr = TF2Currency.from_string("1.4 ref", rounding_mode=RoundingMode.FLOOR)
    assert curr.rounding_mode == RoundingMode.FLOOR
    assert curr._weapons == 25

def test_from_string_negative_values():
    TF2Currency.set_key_price_metal(66.0)
    curr = TF2Currency.from_string("-2 keys, -1.33 ref")
    assert curr.keys == -2
    assert curr.metal == -1.33
    
    curr2 = TF2Currency.from_string("-1.5 keys")
    assert curr2._weapons == -1782
