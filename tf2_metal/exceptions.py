class TF2MetalError(Exception):
    """Base class for all tf2-metal exceptions."""
    pass

class TF2ValidationError(TF2MetalError):
    """Raised when validation of input parameters fails."""
    pass
