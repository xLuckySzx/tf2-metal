import pytest
import tf2_metal

def test_imports():
    try:
        from tf2_metal import TF2Currency
        from tf2_metal import RoundingMode
        from tf2_metal import TF2MetalError
        from tf2_metal import TF2ValidationError
        from tf2_metal import TF2Market
    except ImportError as e:
        pytest.fail(f"ImportError raised unexpectedly: {e}")

def test_all_contains_exact_symbols():
    expected = ["TF2Currency", "RoundingMode", "TF2MetalError", "TF2ValidationError", "TF2Market"]
    assert sorted(tf2_metal.__all__) == sorted(expected)

def test_no_private_symbols_in_all():
    for sym in tf2_metal.__all__:
        assert not sym.startswith("_")

def test_star_import():
    namespace = {}
    exec("from tf2_metal import *", namespace)
    expected = ["TF2Currency", "RoundingMode", "TF2MetalError", "TF2ValidationError", "TF2Market"]
    for sym in expected:
        assert sym in namespace
    
    leaked = [k for k in namespace.keys() if k not in expected and k != "__builtins__"]
    assert len(leaked) == 0
