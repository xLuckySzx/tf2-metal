from tf2_metal.currency import TF2Currency
from tf2_metal.constants import RoundingMode
import math
from tf2_metal.exceptions import TF2ValidationError

class TF2Market:
    """
    A Factory class to manage current market prices and create TF2Currency instances.
    This eliminates the need to pass key prices manually every time you instantiate a currency.
    """

    def __init__(self, key_price_ref: float = 0.0, key_price_usd: float = 0.0):
        self._validate_price(key_price_ref, "key_price_ref")
        self._validate_price(key_price_usd, "key_price_usd")
        self.key_price_ref = key_price_ref
        self.key_price_usd = key_price_usd

    def _validate_price(self, value: float, name: str) -> None:
        if value < 0 or math.isnan(value) or math.isinf(value):
            raise TF2ValidationError(f"{name} must be a finite non-negative number.")

    def update_prices(self, new_ref: float, new_usd: float) -> None:
        """Update the market prices for the factory."""
        self._validate_price(new_ref, "new_ref")
        self._validate_price(new_usd, "new_usd")
        self.key_price_ref = new_ref
        self.key_price_usd = new_usd

    def create(self, keys: int = 0, metal: float = 0.0, rounding_mode: RoundingMode = RoundingMode.ROUND) -> TF2Currency:
        """Create a new TF2Currency instance with the current market prices."""
        return TF2Currency(
            keys=keys,
            metal=metal,
            rounding_mode=rounding_mode,
            key_price_ref=self.key_price_ref,
            key_price_usd=self.key_price_usd
        )

    def parse(self, text: str, rounding_mode: RoundingMode = RoundingMode.ROUND) -> TF2Currency:
        """Parse a string into a TF2Currency instance with the current market prices."""
        return TF2Currency.from_string(
            text,
            rounding_mode=rounding_mode,
            key_price_ref=self.key_price_ref,
            key_price_usd=self.key_price_usd
        )

    def from_dict(self, data: dict[str, int | float], rounding_mode: RoundingMode = RoundingMode.ROUND) -> TF2Currency:
        """Create a TF2Currency from a dictionary with the current market prices."""
        return TF2Currency.from_dict(
            data,
            rounding_mode=rounding_mode,
            key_price_ref=self.key_price_ref,
            key_price_usd=self.key_price_usd
        )
