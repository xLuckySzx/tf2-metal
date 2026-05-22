import math
from dataclasses import FrozenInstanceError
import pytest

from tf2_metal.currency import TF2Currency
from tf2_metal.constants import RoundingMode
from tf2_metal.exceptions import TF2ValidationError

@pytest.fixture(autouse=True)
def reset_class_vars():
    yield
    TF2Currency.key_price_ref = 0.0

def test_nominal_construction_metal_only():
    curr = TF2Currency(metal=18.0)
    assert curr._weapons == 324

def test_nominal_construction_with_keys():
    TF2Currency.set_key_price_metal(66.0)
    curr = TF2Currency(keys=1)
    assert curr._weapons == 1188

def test_metal_to_weapons_rounding():
    assert TF2Currency.metal_to_weapons(1.5, RoundingMode.ROUND) == 27
    assert TF2Currency.metal_to_weapons(1.4, RoundingMode.ROUND) == 25
    assert TF2Currency.metal_to_weapons(1.4, RoundingMode.FLOOR) == 25
    assert TF2Currency.metal_to_weapons(1.4, RoundingMode.CEIL) == 26
    assert TF2Currency.metal_to_weapons(1.6, RoundingMode.FLOOR) == 28
    assert TF2Currency.metal_to_weapons(1.6, RoundingMode.CEIL) == 29

def test_keys_without_price():
    with pytest.raises(TF2ValidationError):
        TF2Currency(keys=1)

def test_invalid_metal_values():
    with pytest.raises(TF2ValidationError):
        TF2Currency(metal=float('inf'))
    with pytest.raises(TF2ValidationError):
        TF2Currency(metal=float('-inf'))
    with pytest.raises(TF2ValidationError):
        TF2Currency(metal=float('nan'))

def test_frozen_instance():
    curr = TF2Currency(metal=1.0)
    with pytest.raises(FrozenInstanceError):
        curr.metal = 5.0

def test_equality():
    assert TF2Currency(metal=1.0) == TF2Currency(metal=1.0)

def test_hashing():
    assert hash(TF2Currency(metal=1.0)) == hash(TF2Currency(metal=1.0))
    assert hash(TF2Currency(metal=1.0)) != hash(TF2Currency(metal=2.0))

def test_negative_values():
    curr1 = TF2Currency(metal=-1.33)
    assert curr1._weapons < 0

    TF2Currency.set_key_price_metal(66.0)
    curr2 = TF2Currency(keys=-1, metal=0.0)
    assert curr2._weapons < 0
