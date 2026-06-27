import math
from dataclasses import dataclass
from tf2_metal.constants import RoundingMode, WEAPONS_PER_REF
from tf2_metal.exceptions import TF2ValidationError


@dataclass(frozen=True)
class TF2Currency:
    keys: int = 0
    metal: float = 0.0
    rounding_mode: RoundingMode = RoundingMode.ROUND

    key_price_ref: float = 0.0
    key_price_usd: float | None = None

    @staticmethod
    def metal_to_weapons(metal: float, rounding_mode: RoundingMode) -> int:
        raw = metal * WEAPONS_PER_REF
        if rounding_mode == RoundingMode.ROUND:
            return round(raw)
        elif rounding_mode == RoundingMode.FLOOR:
            return math.floor(raw)
        elif rounding_mode == RoundingMode.CEIL:
            return math.ceil(raw)
        raise ValueError(f"Unsupported rounding mode: {rounding_mode}")

    def __post_init__(self) -> None:
        if math.isnan(self.metal) or math.isinf(self.metal):
            raise TF2ValidationError("metal must be a finite number.")
        if self.key_price_ref < 0 or math.isnan(self.key_price_ref) or math.isinf(self.key_price_ref):
            raise TF2ValidationError("key_price_ref must be a finite non-negative number.")
        if self.key_price_usd is not None and (self.key_price_usd < 0 or math.isnan(self.key_price_usd) or math.isinf(self.key_price_usd)):
            raise TF2ValidationError("key_price_usd must be a finite non-negative number.")

    def to_weapons(self, key_price_ref: float | None = None) -> int:
        price_ref = key_price_ref if key_price_ref is not None else self.key_price_ref
        if self.keys != 0 and price_ref == 0.0:
            raise TF2ValidationError("Cannot calculate weapons with keys when key_price_ref is not set.")
        key_price_in_weapons = int(self.metal_to_weapons(price_ref, self.rounding_mode)) if self.keys != 0 else 0
        return self.keys * key_price_in_weapons + self.metal_to_weapons(self.metal, self.rounding_mode)

    def breakdown(self) -> dict[str, int]:
        from tf2_metal.constants import WEAPONS_PER_REF, WEAPONS_PER_RECLAIMED, WEAPONS_PER_SCRAP
        
        result = {}
        if self.keys != 0:
            result["keys"] = self.keys
            
        weapons = self.metal_to_weapons(self.metal, self.rounding_mode)
        is_neg = weapons < 0
        rem = abs(weapons)
        
        refined = rem // WEAPONS_PER_REF
        rem = rem % WEAPONS_PER_REF
        reclaimed = rem // WEAPONS_PER_RECLAIMED
        rem = rem % WEAPONS_PER_RECLAIMED
        scrap = rem // WEAPONS_PER_SCRAP
        rem = rem % WEAPONS_PER_SCRAP
        
        if is_neg:
            refined = -refined
            reclaimed = -reclaimed
            scrap = -scrap
            rem = -rem
            
        result["refined"] = refined
        result["reclaimed"] = reclaimed
        result["scrap"] = scrap
        result["weapons"] = rem
            
        return result

    def __str__(self) -> str:
        if self.keys == 0 and self.metal == 0.0:
            return "0 ref"

        bd = self.breakdown()
        
        components = []
        names = {
            "keys": ("key", "keys"),
            "refined": ("ref", "ref"),
            "reclaimed": ("reclaimed", "reclaimed"),
            "scrap": ("scrap", "scrap"),
            "weapons": ("weapon", "weapons")
        }
        
        for k in ["keys", "refined", "reclaimed", "scrap", "weapons"]:
            if k in bd and bd[k] != 0:
                val = bd[k]
                abs_val = abs(val)
                sing, plur = names[k]
                name = sing if abs_val == 1 else plur
                components.append(f"{val} {name}")
                
        if not components:
            return "0 ref"
        return ", ".join(components)

    @classmethod
    def from_weapons(cls, weapons: int, rounding_mode: RoundingMode = RoundingMode.ROUND, key_price_ref: float = 0.0, key_price_usd: float | None = None) -> "TF2Currency":
        from tf2_metal.constants import WEAPONS_PER_REF
        return cls(keys=0, metal=weapons / WEAPONS_PER_REF, rounding_mode=rounding_mode, key_price_ref=key_price_ref, key_price_usd=key_price_usd)

    def _check_prices(self, other: "TF2Currency") -> tuple[float, float | None]:
        if self.key_price_ref != 0.0 and other.key_price_ref != 0.0 and self.key_price_ref != other.key_price_ref:
            raise TF2ValidationError("Cannot perform operations on currencies with different key prices.")
        if self.key_price_usd is not None and other.key_price_usd is not None and self.key_price_usd != other.key_price_usd:
            raise TF2ValidationError("Cannot perform operations on currencies with different USD prices.")
        
        res_ref = self.key_price_ref if self.key_price_ref != 0.0 else other.key_price_ref
        res_usd = self.key_price_usd if self.key_price_usd is not None else other.key_price_usd
        return res_ref, res_usd

    def __add__(self, other: "TF2Currency") -> "TF2Currency":
        if not isinstance(other, TF2Currency):
            return NotImplemented
        res_ref, res_usd = self._check_prices(other)
        return TF2Currency(
            keys=self.keys + other.keys,
            metal=self.metal + other.metal,
            rounding_mode=self.rounding_mode,
            key_price_ref=res_ref,
            key_price_usd=res_usd
        )

    def __sub__(self, other: "TF2Currency") -> "TF2Currency":
        if not isinstance(other, TF2Currency):
            return NotImplemented
        res_ref, res_usd = self._check_prices(other)
        return TF2Currency(
            keys=self.keys - other.keys,
            metal=self.metal - other.metal,
            rounding_mode=self.rounding_mode,
            key_price_ref=res_ref,
            key_price_usd=res_usd
        )

    def __mul__(self, scalar: int | float) -> "TF2Currency":
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        if isinstance(scalar, float) and (math.isnan(scalar) or math.isinf(scalar)):
            raise TF2ValidationError("Scalar cannot be NaN or infinity.")
        
        raw_keys = self.keys * scalar
        int_keys = int(raw_keys)
        frac_keys = raw_keys - int_keys
        
        new_metal = self.metal * scalar
        if frac_keys != 0:
            if self.key_price_ref == 0.0:
                raise TF2ValidationError("Cannot multiply keys to a fractional amount without key_price_ref.")
            new_metal += frac_keys * self.key_price_ref
            
        return TF2Currency(
            keys=int_keys,
            metal=new_metal,
            rounding_mode=self.rounding_mode,
            key_price_ref=self.key_price_ref,
            key_price_usd=self.key_price_usd
        )

    def __rmul__(self, scalar: int | float) -> "TF2Currency":
        return self.__mul__(scalar)

    def __truediv__(self, scalar: int | float) -> "TF2Currency":
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        if scalar == 0 or scalar == 0.0:
            raise TF2ValidationError("Division by zero.")
        if isinstance(scalar, float) and (math.isnan(scalar) or math.isinf(scalar)):
            raise TF2ValidationError("Scalar cannot be NaN or infinity.")
            
        raw_keys = self.keys / scalar
        int_keys = int(raw_keys)
        frac_keys = raw_keys - int_keys
        
        new_metal = self.metal / scalar
        if frac_keys != 0:
            if self.key_price_ref == 0.0:
                raise TF2ValidationError("Cannot divide keys to a fractional amount without key_price_ref.")
            new_metal += frac_keys * self.key_price_ref
            
        return TF2Currency(
            keys=int_keys,
            metal=new_metal,
            rounding_mode=self.rounding_mode,
            key_price_ref=self.key_price_ref,
            key_price_usd=self.key_price_usd
        )

    def __lt__(self, other: "TF2Currency") -> bool:
        if not isinstance(other, TF2Currency):
            return NotImplemented
        if self.keys != other.keys:
            return self.keys < other.keys
        return self.metal < other.metal

    def __le__(self, other: "TF2Currency") -> bool:
        if not isinstance(other, TF2Currency):
            return NotImplemented
        if self.keys != other.keys:
            return self.keys < other.keys
        return self.metal <= other.metal

    def __gt__(self, other: "TF2Currency") -> bool:
        if not isinstance(other, TF2Currency):
            return NotImplemented
        if self.keys != other.keys:
            return self.keys > other.keys
        return self.metal > other.metal

    def __ge__(self, other: "TF2Currency") -> bool:
        if not isinstance(other, TF2Currency):
            return NotImplemented
        if self.keys != other.keys:
            return self.keys > other.keys
        return self.metal >= other.metal

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TF2Currency):
            return NotImplemented
        return self.keys == other.keys and self.metal == other.metal

    @staticmethod
    def from_string(s: str, rounding_mode: RoundingMode = RoundingMode.ROUND, key_price_ref: float = 0.0, key_price_usd: float | None = None) -> "TF2Currency":
        if not s or not s.strip():
            raise TF2ValidationError("String cannot be empty or whitespace only.")
            
        import re
        pattern = re.compile(
            r"^\s*(?:(?P<keys>-?\d+(?:\.\d+)?)\s*(?:k|key|keys))?"
            r"(?:,?\s*)?"
            r"(?:(?P<metal>-?\d+(?:\.\d+)?)\s*(?:ref|metal|refined|refs|refineds))?\s*$",
            re.IGNORECASE
        )
        match = pattern.match(s)
        if not match or (match.group("keys") is None and match.group("metal") is None):
            raise TF2ValidationError(f"Could not parse currency string: {s}")
            
        keys_str = match.group("keys")
        metal_str = match.group("metal")
        
        keys_val = float(keys_str) if keys_str is not None else 0.0
        metal_val = float(metal_str) if metal_str is not None else 0.0
        
        int_keys = int(keys_val)
        frac_keys = keys_val - int_keys
        
        final_metal = metal_val
        if frac_keys != 0:
            if key_price_ref == 0.0:
                raise TF2ValidationError("Cannot specify fractional keys in string when key_price_ref is not set.")
            final_metal += (frac_keys * key_price_ref)
        
        return TF2Currency(keys=int_keys, metal=final_metal, rounding_mode=rounding_mode, key_price_ref=key_price_ref, key_price_usd=key_price_usd)

    def to_dict(self) -> dict[str, int | float]:
        return {"keys": self.keys, "metal": round(self.metal, 2)}

    @classmethod
    def from_dict(cls, data: dict[str, int | float], rounding_mode: RoundingMode = RoundingMode.ROUND, key_price_ref: float = 0.0, key_price_usd: float | None = None) -> "TF2Currency":
        if "keys" not in data:
            raise TF2ValidationError("Missing 'keys' field in dict.")
        if "metal" not in data:
            raise TF2ValidationError("Missing 'metal' field in dict.")
            
        keys_val = data["keys"]
        metal_val = data["metal"]
        
        if not isinstance(keys_val, (int, float)) or isinstance(keys_val, bool):
            raise TF2ValidationError("'keys' must be numeric.")
        if not isinstance(metal_val, (int, float)) or isinstance(metal_val, bool):
            raise TF2ValidationError("'metal' must be numeric.")
            
        int_keys = int(keys_val)
        frac_keys = keys_val - int_keys
        
        final_metal = float(metal_val)
        if frac_keys != 0:
            if key_price_ref == 0.0:
                raise TF2ValidationError("Cannot specify fractional keys when key_price_ref is not set.")
            final_metal += (frac_keys * key_price_ref)
        
        return cls(keys=int_keys, metal=final_metal, rounding_mode=rounding_mode, key_price_ref=key_price_ref, key_price_usd=key_price_usd)
