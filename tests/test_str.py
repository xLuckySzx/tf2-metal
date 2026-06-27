import pytest
from tf2_metal.currency import TF2Currency



def test_str_full_components():
    curr = TF2Currency(keys=2, metal=12.5, key_price_ref=18.0)
    s = str(curr)
    assert "2 keys" in s
    assert "12 ref" in s
    assert "1 reclaimed" in s
    assert "1 scrap" in s
    assert "1 weapon" in s

def test_str_partial():
    curr = TF2Currency(metal=1.0 + 2/18)
    assert str(curr) == "1 ref, 1 scrap"

def test_str_singular_key():
    curr = TF2Currency(keys=1, key_price_ref=18.0)
    s = str(curr)
    assert "1 key" in s
    assert "1 keys" not in s

def test_str_singular_weapon():
    curr = TF2Currency(metal=1.0 + 1/18)
    s = str(curr)
    assert "1 weapon" in s
    assert "1 weapons" not in s

def test_str_singular_ref():
    curr = TF2Currency(metal=1.0)
    assert str(curr) == "1 ref"

def test_str_singular_scrap():
    curr = TF2Currency(metal=1.0 + 2/18)
    s = str(curr)
    assert "1 scrap" in s
    assert "1 scraps" not in s

def test_str_singular_reclaimed():
    curr = TF2Currency(metal=1.0 + 6/18)
    s = str(curr)
    assert "1 reclaimed" in s

def test_str_sub_ref():
    curr = TF2Currency(metal=0.33)
    assert str(curr) in ("1 reclaimed")

def test_str_negative():
    curr = TF2Currency(metal=-1.0)
    assert "-1 ref" in str(curr)

def test_str_zero():
    curr = TF2Currency()
    assert str(curr) == "0 ref"
