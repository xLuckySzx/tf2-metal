# tf2-metal

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

`tf2-metal` is a pure Python library designed for parsing, manipulating, and converting Team Fortress 2 (TF2) currencies (Keys, Refined, Reclaimed, Scrap, and Weapons) with absolute precision. 

By utilizing an internal integer representation based on the lowest common denominator (the "weapon"), this library completely eliminates floating-point precision errors that commonly plague TF2 economy calculations.

## Features

- **Absolute Precision**: All internal calculations are performed using integers (weapons) to prevent floating-point anomalies.
- **Immutable & Type-Safe**: Built on frozen dataclasses. Every arithmetic operation returns a new instance.
- **Rich Arithmetic Support**: Supports addition, subtraction, multiplication, division, and all comparison operators.
- **Flexible Parsing**: Parse complex currency strings like `"2k, 5.33 ref"`, `"-1.5 keys"`, or `"0.05 ref"`.
- **Serialization**: Built-in support for converting to and from dictionaries for easy JSON serialization.
- **Rounding Modes**: Customizable rounding strategies (`ROUND`, `FLOOR`, `CEIL`) for fractional metal conversions.
- **Zero External Dependencies**: Standard library only.

## Installation

This library is intended for private/internal use and is not published on PyPI. You can add it to your project by cloning the repository or using git submodules:

```bash
git clone https://github.com/your-username/tf2-metal.git
```
Then, ensure the `tf2-metal` directory is in your `PYTHONPATH` or install it via `pip install -e .`.

## Quickstart

```python
from tf2_metal import TF2Currency, RoundingMode

# 1. Set the global key price (required for key-metal conversions)
TF2Currency.set_key_price_metal(66.33)

# 2. Create currency instances
wallet = TF2Currency(keys=10, metal=5.11)
item_price = TF2Currency.from_string("1k, 13.33 ref")

# 3. Arithmetic operations
remaining = wallet - item_price
print(remaining) 
# Output: "8 keys, 58 ref, 1 scrap"

# 4. Multiplication/Division
print(item_price * 2)
# Output: "3 keys, 13 ref"

# 5. Serialization
data = remaining.to_dict()
print(data) 
# Output: {'keys': 8, 'metal': 58.11}
```

## Documentation

For a comprehensive guide specifically tailored for Large Language Models (LLMs) or automated agents to interact with this library, please refer to [docs/llm_guide.md](docs/llm_guide.md).
