import math
from dataclasses import FrozenInstanceError
import pytest

from tf2_metal.currency import TF2Currency
from tf2_metal.constants import RoundingMode
from tf2_metal.exceptions import TF2ValidationError



def test_nominal_construction_metal_only():
    curr = TF2Currency(metal=18.0)
    assert curr.to_weapons(66.0) == 324

def test_nominal_construction_with_keys():
    curr = TF2Currency(keys=1, key_price_ref=66.0)
    assert curr.to_weapons(66.0) == 1188

def test_metal_to_weapons_rounding():
    assert TF2Currency.metal_to_weapons(1.5, RoundingMode.ROUND) == 27
    assert TF2Currency.metal_to_weapons(1.4, RoundingMode.ROUND) == 25
    assert TF2Currency.metal_to_weapons(1.4, RoundingMode.FLOOR) == 25
    assert TF2Currency.metal_to_weapons(1.4, RoundingMode.CEIL) == 26
    assert TF2Currency.metal_to_weapons(1.6, RoundingMode.FLOOR) == 28
    assert TF2Currency.metal_to_weapons(1.6, RoundingMode.CEIL) == 29

def test_keys_without_price():
    curr = TF2Currency(keys=1)
    assert curr.keys == 1

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
    assert curr1.to_weapons(66.0) < 0

    curr2 = TF2Currency(keys=-1, metal=0.0, key_price_ref=66.0)
    assert curr2.to_weapons(66.0) < 0

def test_to_weapons():
    curr = TF2Currency(metal=1.0)
    assert curr.to_weapons() == 18
    
    curr2 = TF2Currency(keys=1, metal=1.0, key_price_ref=66.0)
    assert curr2.to_weapons() == 1206

def test_from_weapons():
    curr = TF2Currency.from_weapons(18)
    assert curr.keys == 0
    assert curr.metal == 1.0
    
    curr2 = TF2Currency.from_weapons(1206, key_price_ref=66.0)
    assert curr2.keys == 0
    assert curr2.metal == 67.0
    assert curr2.to_weapons(66.0) == 1206

def test_to_weapons_edge_cases():
    assert TF2Currency(metal=0.0).to_weapons() == 0
    assert TF2Currency(keys=-1, metal=-1.0, key_price_ref=66.0).to_weapons() == -1206
    
    curr = TF2Currency(metal=0.0)
    curr = curr + TF2Currency(metal=0.11)
    assert curr.to_weapons() == 2

def test_from_weapons_edge_cases():
    curr = TF2Currency.from_weapons(0)
    assert curr.keys == 0
    assert curr.metal == 0.0
    assert curr.to_weapons(66.0) == 0
    
    curr2 = TF2Currency.from_weapons(-18)
    assert curr2.keys == 0
    assert curr2.metal == -1.0
    assert curr2.to_weapons(66.0) == -18
    
    curr3 = TF2Currency.from_weapons(1800000)
    assert curr3.metal == 100000.0
    assert curr3.to_weapons(66.0) == 1800000
