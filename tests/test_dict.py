import pytest
from tf2_metal.currency import TF2Currency
from tf2_metal.constants import RoundingMode
from tf2_metal.exceptions import TF2ValidationError



def test_to_dict_with_keys():
    curr = TF2Currency(keys=1, metal=13.33, key_price_ref=66.33)
    assert curr.to_dict() == {"keys": 1, "metal": 13.33}

def test_to_dict_metal_only():
    curr = TF2Currency(metal=1.0)
    assert curr.to_dict() == {"keys": 0, "metal": 1.0}

def test_from_dict_metal_only():
    curr = TF2Currency.from_dict({"keys": 0, "metal": 13.33})
    assert curr.keys == 0
    assert curr.to_weapons(66.0) == 240

def test_from_dict_with_keys():
    curr = TF2Currency.from_dict({"keys": 1, "metal": 13.33}, key_price_ref=66.33)
    assert curr.keys == 1
    assert curr.to_weapons(66.33) == 1434

def test_from_dict_missing_fields():
    with pytest.raises(TF2ValidationError):
        TF2Currency.from_dict({})
    with pytest.raises(TF2ValidationError):
        TF2Currency.from_dict({"keys": 1})
    with pytest.raises(TF2ValidationError):
        TF2Currency.from_dict({"metal": 1.0})

def test_from_dict_invalid_types():
    with pytest.raises(TF2ValidationError):
        TF2Currency.from_dict({"keys": "uno", "metal": 1.0})
    with pytest.raises(TF2ValidationError):
        TF2Currency.from_dict({"keys": 1, "metal": "moltometal"})

def test_from_dict_keys_no_price():
    curr = TF2Currency.from_dict({'keys': 1, 'metal': 0.0})
    assert curr.keys == 1

def test_from_dict_rounding_mode():
    curr = TF2Currency.from_dict({"keys": 0, "metal": 1.4}, rounding_mode=RoundingMode.CEIL)
    assert curr.rounding_mode == RoundingMode.CEIL
