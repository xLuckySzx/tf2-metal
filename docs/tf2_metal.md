# LLM Usage Guide: `tf2-metal`

This document provides a concise, machine-readable overview of the `tf2-metal` library to help Large Language Models (LLMs) and automated agents understand how to consume its API without needing to parse the entire source code.

## 1. Core Concepts
- **Absolute Precision**: `TF2Currency` eliminates floating-point errors by converting all inputs into a single internal integer `_weapons` (1 ref = 18 weapons, 1 scrap = 2 weapons, 1 reclaimed = 6 weapons). 
- **Immutability**: `TF2Currency` is a `@dataclass(frozen=True)`. Do not attempt to mutate instances.
- **Instance-specific Key Price**: Conversions between keys and metal require explicitly passing the current key price `key_price_ref` to the constructor or factory methods. This eliminates global state and ensures thread-safety.

## 2. Public API
Always import symbols from the top-level namespace:
from tf2_metal import TF2Currency, RoundingMode, TF2MetalError, TF2ValidationError, TF2Market
```

## 3. Class: `TF2Market` (Factory Pattern)

`TF2Market` is the recommended way to instantiate `TF2Currency` objects. It holds the current market prices and injects them automatically.
`key_price_ref` is strictly required upon initialization. `key_price_usd` is always optional (defaults to `None`).

### 3.1 Setup & Updates
```python
market = TF2Market(key_price_ref=65.0, key_price_usd=1.85)

# Update prices later (arguments are optional, updates only what you provide)
market.update_prices(new_ref=65.11)
market.update_prices(new_usd=1.84)
```

### 3.2 Factory Methods
- **Create**: `market.create(keys=1, metal=2.0)`
- **Parse**: `market.parse("1k, 5 ref")`
- **From Dict**: `market.from_dict({"keys": 1, "metal": 5.0})`

## 4. Class: `TF2Currency`

### 4.1 Constructor
```python
# Keys and metal default to 0.0
# RoundingMode defaults to RoundingMode.ROUND
currency = TF2Currency(
    keys=2, 
    metal=1.33, 
    rounding_mode=RoundingMode.FLOOR, 
    key_price_ref=65.0, 
    key_price_usd=1.85
)
```
- Raises `TF2ValidationError` if you pass non-zero `keys` without providing `key_price_ref`.

### 4.2 Factory Methods
- **From String**: 
  ```python
  c = TF2Currency.from_string("2 keys, 13.33 ref", rounding_mode=RoundingMode.ROUND, key_price_ref=65.0)
  ```
  Parses strings like `"2k"`, `"1.5 keys"`, `"-5 ref"`, `"2 keys 13.33 metal"`.
- **From Dictionary**:
  ```python
  c = TF2Currency.from_dict(
      {"keys": 1, "metal": 13.33}, 
      key_price_ref=65.0,
      key_price_usd=1.85
  )
  ```

### 4.3 Serialization and Inspection
- **To Dictionary**:
  ```python
  c.to_dict() # Returns {"keys": int, "metal": float}
  ```
- **String Formatting**:
  ```python
  str(c) # Returns canonical TF2 formats e.g., "1 key, 2 ref, 1 scrap" or "0.05 ref"
  ```
- **Breakdown**:
  ```python
  c.breakdown() # Returns physical items dict: {"keys": 1, "refined": 2, "reclaimed": 0, "scrap": 1, "weapons": 0}
  ```

### 4.4 Arithmetic & Comparisons
Instances support native Python operators and always return new, distinct `TF2Currency` instances.
- **Addition / Subtraction**: `c1 + c2`, `c1 - c2`
- **Price Consistency**: Addition and subtraction will raise a `TF2ValidationError` if performed on two instances with differing, non-zero `key_price_ref`.
- **Multiplication / Division** (by scalar integer or float): `c1 * 2`, `c1 / 2.5`
- **Comparisons** (based on absolute value in weapons): `c1 == c2`, `c1 != c2`, `c1 > c2`, `c1 <= c2`

## 5. Enums & Exceptions
- **`RoundingMode`**: `RoundingMode.ROUND`, `RoundingMode.FLOOR`, `RoundingMode.CEIL`. Defines how fractional weapons are handled during conversions and scalar multiplications.
- **`TF2ValidationError`**: Raised for invalid inputs (e.g., negative key prices, division by zero, invalid string parsing). Inherits from `TF2MetalError`.
