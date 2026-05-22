import pytest
from tf2_metal.currency import TF2Currency
from tf2_metal.exceptions import TF2ValidationError

@pytest.fixture(autouse=True)
def reset_class_vars():
    yield
    TF2Currency.key_price_ref = 0.0
    TF2Currency.key_price_usd = 0.0

def test_set_key_price_metal_success():
    TF2Currency.set_key_price_metal(66.33)
    assert TF2Currency.key_price_ref == 66.33
    
    inst = TF2Currency()
    assert inst.key_price_ref == 66.33

def test_set_key_price_metal_zero():
    with pytest.raises(TF2ValidationError):
        TF2Currency.set_key_price_metal(0)

def test_set_key_price_metal_negative():
    with pytest.raises(TF2ValidationError):
        TF2Currency.set_key_price_metal(-1.0)

def test_set_key_price_metal_inf():
    with pytest.raises(TF2ValidationError):
        TF2Currency.set_key_price_metal(float('inf'))

def test_set_key_price_metal_nan():
    with pytest.raises(TF2ValidationError):
        TF2Currency.set_key_price_metal(float('nan'))


def test_set_key_price_usd_success():
    TF2Currency.set_key_price_usd(2.49)
    assert TF2Currency.key_price_usd == 2.49

def test_set_key_price_usd_zero():
    with pytest.raises(TF2ValidationError):
        TF2Currency.set_key_price_usd(0)

def test_set_key_price_usd_negative():
    with pytest.raises(TF2ValidationError):
        TF2Currency.set_key_price_usd(-1.0)

def test_set_key_price_usd_inf():
    with pytest.raises(TF2ValidationError):
        TF2Currency.set_key_price_usd(float('inf'))

def test_set_key_price_usd_nan():
    with pytest.raises(TF2ValidationError):
        TF2Currency.set_key_price_usd(float('nan'))
