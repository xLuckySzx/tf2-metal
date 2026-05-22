import pytest
from tf2_metal.exceptions import TF2MetalError, TF2ValidationError

def test_exception_hierarchy():
    assert issubclass(TF2ValidationError, TF2MetalError)
    assert issubclass(TF2MetalError, Exception)

def test_tf2_validation_error_message():
    msg = "messaggio"
    exc = TF2ValidationError(msg)
    
    assert str(exc) == msg
    assert exc.args[0] == msg

def test_tf2_metal_error_message():
    msg = "messaggio"
    exc = TF2MetalError(msg)
    
    assert str(exc) == msg
    assert exc.args[0] == msg
