import pytest
from tf2_metal.currency import TF2Currency

@pytest.fixture(autouse=True)
def reset_class_vars():
    yield
    TF2Currency.key_price_ref = 0.0

def test_breakdown_nominal_metal():
    curr = TF2Currency(metal=1.0)
    assert curr.breakdown() == {"refined": 1, "reclaimed": 0, "scrap": 0, "weapons": 0}

def test_breakdown_all_components():
    curr = TF2Currency(metal=1.0 + 6/18 + 2/18 + 1/18)
    assert curr.breakdown() == {"refined": 1, "reclaimed": 1, "scrap": 1, "weapons": 1}

def test_breakdown_with_keys():
    TF2Currency.set_key_price_metal(18.0)
    curr = TF2Currency(keys=1)
    bd = curr.breakdown()
    assert "keys" in bd
    assert bd["keys"] == 1
    assert bd["refined"] == 0
    assert bd["reclaimed"] == 0
    assert bd["scrap"] == 0
    assert bd["weapons"] == 0

def test_breakdown_without_keys_omits_key():
    curr = TF2Currency(metal=1.0)
    bd = curr.breakdown()
    assert "keys" not in bd

def test_breakdown_negative_value():
    curr = TF2Currency(metal=-1.0)
    bd = curr.breakdown()
    assert bd["refined"] == -1
    assert bd["reclaimed"] == 0
    assert bd["scrap"] == 0
    assert bd["weapons"] == 0

def test_breakdown_zero_value():
    curr = TF2Currency(metal=0.0)
    bd = curr.breakdown()
    assert bd == {"refined": 0, "reclaimed": 0, "scrap": 0, "weapons": 0}
    assert "keys" not in bd

def test_breakdown_one_weapon():
    curr = TF2Currency(metal=1/18)
    assert curr.breakdown() == {"refined": 0, "reclaimed": 0, "scrap": 0, "weapons": 1}
