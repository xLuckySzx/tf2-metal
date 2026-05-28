import pytest
from tf2_metal.market import TF2Market
from tf2_metal.currency import TF2Currency
from tf2_metal.exceptions import TF2ValidationError

def test_market_initialization():
    market = TF2Market(key_price_ref=65.0, key_price_usd=1.85)
    assert market.key_price_ref == 65.0
    assert market.key_price_usd == 1.85

def test_market_initialization_invalid():
    with pytest.raises(TF2ValidationError):
        TF2Market(key_price_ref=-1.0)
    with pytest.raises(TF2ValidationError):
        TF2Market(key_price_ref=65.0, key_price_usd=float('inf'))
    with pytest.raises(TF2ValidationError):
        TF2Market(key_price_ref=float('nan'))

def test_market_update_prices():
    market = TF2Market(key_price_ref=65.0)
    assert market.key_price_ref == 65.0
    
    market.update_prices(70.11, 1.90)
    assert market.key_price_ref == 70.11
    assert market.key_price_usd == 1.90
    
    market.update_prices(new_ref=65.0)
    assert market.key_price_ref == 65.0
    assert market.key_price_usd == 1.90
    
    market.update_prices(new_usd=2.0)
    assert market.key_price_ref == 65.0
    assert market.key_price_usd == 2.0

def test_market_update_prices_invalid():
    market = TF2Market(key_price_ref=65.0)
    with pytest.raises(TF2ValidationError):
        market.update_prices(-5.0, 1.85)
    with pytest.raises(TF2ValidationError):
        market.update_prices(70.11, -1.90)

def test_market_create():
    market = TF2Market(key_price_ref=60.0)
    curr = market.create(keys=2, metal=1.33)
    assert isinstance(curr, TF2Currency)
    assert curr.keys == 2
    assert curr.metal == 1.33
    assert curr.key_price_ref == 60.0

def test_market_parse():
    market = TF2Market(key_price_ref=60.0)
    curr = market.parse("2 keys, 13.33 ref")
    assert isinstance(curr, TF2Currency)
    assert curr.keys == 2
    assert curr.metal == 13.33
    assert curr.key_price_ref == 60.0

def test_market_from_dict():
    market = TF2Market(key_price_ref=60.0)
    curr = market.from_dict({"keys": 1, "metal": 10.0})
    assert isinstance(curr, TF2Currency)
    assert curr.keys == 1
    assert curr.metal == 10.0
    assert curr.key_price_ref == 60.0

def test_market_from_weapons():
    market = TF2Market(key_price_ref=60.0, key_price_usd=2.0)
    curr = market.from_weapons(1080)
    assert isinstance(curr, TF2Currency)
    assert curr.keys == 0
    assert curr.metal == 60.0
    assert curr.key_price_ref == 60.0
    assert curr.key_price_usd == 2.0
    assert curr._weapons == 1080

def test_market_from_weapons_edge_cases():
    market = TF2Market(key_price_ref=60.0, key_price_usd=2.0)
    
    # 0 weapons
    curr = market.from_weapons(0)
    assert curr.keys == 0
    assert curr.metal == 0.0
    assert curr.key_price_ref == 60.0
    assert curr._weapons == 0
    
    # Negative weapons
    curr2 = market.from_weapons(-1080)
    assert curr2.keys == 0
    assert curr2.metal == -60.0
    assert curr2._weapons == -1080
    
    # Very large number of weapons
    curr3 = market.from_weapons(108000000)
    assert curr3.metal == 6000000.0
    assert curr3._weapons == 108000000
