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
        if self.keys != 0 and self.key_price_ref == 0.0:
            raise TF2ValidationError("Cannot specify keys when key_price_ref is not set.")
        if self.key_price_ref < 0 or math.isnan(self.key_price_ref) or math.isinf(self.key_price_ref):
            raise TF2ValidationError("key_price_ref must be a finite non-negative number.")
        if self.key_price_usd is not None and (self.key_price_usd < 0 or math.isnan(self.key_price_usd) or math.isinf(self.key_price_usd)):
            raise TF2ValidationError("key_price_usd must be a finite non-negative number.")
            
        key_price_in_weapons = 0
        if self.keys != 0:
            key_price_in_weapons = int(self.metal_to_weapons(self.key_price_ref, self.rounding_mode))
            
        _weapons = self.keys * key_price_in_weapons + self.metal_to_weapons(self.metal, self.rounding_mode)
        object.__setattr__(self, "_weapons", _weapons)

    def breakdown(self) -> dict[str, int]:
        from tf2_metal.constants import WEAPONS_PER_REF, WEAPONS_PER_RECLAIMED, WEAPONS_PER_SCRAP
        
        is_neg = self._weapons < 0
        rem = abs(self._weapons)
        
        result = {}
        
        if self.key_price_ref > 0:
            key_price_in_weapons = int(self.metal_to_weapons(self.key_price_ref, self.rounding_mode))
            if key_price_in_weapons > 0:
                result["keys"] = rem // key_price_in_weapons
                rem = rem % key_price_in_weapons

        result["refined"] = rem // WEAPONS_PER_REF
        rem = rem % WEAPONS_PER_REF
        
        result["reclaimed"] = rem // WEAPONS_PER_RECLAIMED
        rem = rem % WEAPONS_PER_RECLAIMED
        
        result["scrap"] = rem // WEAPONS_PER_SCRAP
        rem = rem % WEAPONS_PER_SCRAP
        
        result["weapons"] = rem
        
        if is_neg:
            for k in ["keys", "refined", "reclaimed", "scrap", "weapons"]:
                if k in result and result[k] != 0:
                    result[k] = -result[k]
                    break
                    
        return result
    def __str__(self) -> str:
        from tf2_metal.constants import WEAPONS_PER_REF
        
        if self._weapons == 0:
            return "0 ref"

        abs_w = abs(self._weapons)
        
        if self.key_price_ref == 0.0 and abs_w < WEAPONS_PER_REF:
            float_val = round(abs_w / WEAPONS_PER_REF, 2)
            prefix = "-" if self._weapons < 0 else ""
            return f"{prefix}{float_val} ref"

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
                
        return ", ".join(components)

    @classmethod
    def _from_weapons(cls, weapons: int, rounding_mode: RoundingMode, key_price_ref: float = 0.0, key_price_usd: float | None = None) -> "TF2Currency":
        from tf2_metal.constants import WEAPONS_PER_REF
        inst = cls.__new__(cls)
        object.__setattr__(inst, "keys", 0)
        object.__setattr__(inst, "metal", weapons / WEAPONS_PER_REF)
        object.__setattr__(inst, "rounding_mode", rounding_mode)
        object.__setattr__(inst, "key_price_ref", key_price_ref)
        object.__setattr__(inst, "key_price_usd", key_price_usd)
        object.__setattr__(inst, "_weapons", weapons)
        return inst

    def _check_prices(self, other: "TF2Currency") -> tuple[float, float]:
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
        new_weapons = self._weapons + other._weapons
        return self._from_weapons(new_weapons, self.rounding_mode, res_ref, res_usd)

    def __sub__(self, other: "TF2Currency") -> "TF2Currency":
        if not isinstance(other, TF2Currency):
            return NotImplemented
        res_ref, res_usd = self._check_prices(other)
        new_weapons = self._weapons - other._weapons
        return self._from_weapons(new_weapons, self.rounding_mode, res_ref, res_usd)

    def __mul__(self, scalar: int | float) -> "TF2Currency":
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        if isinstance(scalar, float) and (math.isnan(scalar) or math.isinf(scalar)):
            raise TF2ValidationError("Scalar cannot be NaN or infinity.")
        
        raw = self._weapons * scalar
        
        from tf2_metal.constants import RoundingMode
        if self.rounding_mode == RoundingMode.ROUND:
            new_weapons = round(raw)
        elif self.rounding_mode == RoundingMode.FLOOR:
            new_weapons = math.floor(raw)
        elif self.rounding_mode == RoundingMode.CEIL:
            new_weapons = math.ceil(raw)
        else:
            raise ValueError(f"Unsupported rounding mode: {self.rounding_mode}")
            
        return self._from_weapons(new_weapons, self.rounding_mode, self.key_price_ref, self.key_price_usd)

    def __rmul__(self, scalar: int | float) -> "TF2Currency":
        return self.__mul__(scalar)

    def __truediv__(self, scalar: int | float) -> "TF2Currency":
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        if scalar == 0 or scalar == 0.0:
            raise TF2ValidationError("Division by zero.")
        if isinstance(scalar, float) and (math.isnan(scalar) or math.isinf(scalar)):
            raise TF2ValidationError("Scalar cannot be NaN or infinity.")
            
        raw = self._weapons / scalar
        
        from tf2_metal.constants import RoundingMode
        if self.rounding_mode == RoundingMode.ROUND:
            new_weapons = round(raw)
        elif self.rounding_mode == RoundingMode.FLOOR:
            new_weapons = math.floor(raw)
        elif self.rounding_mode == RoundingMode.CEIL:
            new_weapons = math.ceil(raw)
        else:
            raise ValueError(f"Unsupported rounding mode: {self.rounding_mode}")
            
        return self._from_weapons(new_weapons, self.rounding_mode, self.key_price_ref, self.key_price_usd)

    def __lt__(self, other: "TF2Currency") -> bool:
        if not isinstance(other, TF2Currency):
            return NotImplemented
        return self._weapons < other._weapons

    def __le__(self, other: "TF2Currency") -> bool:
        if not isinstance(other, TF2Currency):
            return NotImplemented
        return self._weapons <= other._weapons

    def __gt__(self, other: "TF2Currency") -> bool:
        if not isinstance(other, TF2Currency):
            return NotImplemented
        return self._weapons > other._weapons

    def __ge__(self, other: "TF2Currency") -> bool:
        if not isinstance(other, TF2Currency):
            return NotImplemented
        return self._weapons >= other._weapons

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
        
        if keys_val != 0 and key_price_ref == 0.0:
            raise TF2ValidationError("Cannot specify keys in string when key_price_ref is not set.")
            
        int_keys = int(keys_val)
        frac_keys = keys_val - int_keys
        
        final_metal = metal_val + (frac_keys * key_price_ref)
        
        return TF2Currency(keys=int_keys, metal=final_metal, rounding_mode=rounding_mode, key_price_ref=key_price_ref, key_price_usd=key_price_usd)

    def to_dict(self) -> dict[str, int | float]:
        from tf2_metal.constants import WEAPONS_PER_REF
        
        if self.key_price_ref > 0:
            key_price_in_weapons = int(self.metal_to_weapons(self.key_price_ref, self.rounding_mode))
            
            if key_price_in_weapons > 0:
                bd = self.breakdown()
                keys = bd.get("keys", 0)
                rem_weapons = self._weapons - (keys * key_price_in_weapons)
                metal = round(rem_weapons / WEAPONS_PER_REF, 2)
                return {"keys": keys, "metal": metal}
        
        keys = 0
        metal = round(self._weapons / WEAPONS_PER_REF, 2)
        return {"keys": keys, "metal": metal}

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
            
        if keys_val != 0 and key_price_ref == 0.0:
            raise TF2ValidationError("Cannot specify keys when key_price_ref is not set.")
            
        int_keys = int(keys_val)
        frac_keys = keys_val - int_keys
        
        final_metal = metal_val + (frac_keys * key_price_ref)
        
        return cls(keys=int_keys, metal=final_metal, rounding_mode=rounding_mode, key_price_ref=key_price_ref, key_price_usd=key_price_usd)
