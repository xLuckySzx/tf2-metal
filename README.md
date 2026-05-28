<div align="center">
  
# 🎒 tf2-metal
**A Pure Python Library for Team Fortress 2 Economy & Currency Mathematics**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![Types: Mypy](https://img.shields.io/badge/types-Mypy-informational.svg?style=for-the-badge)](https://github.com/python/mypy)

*Eliminate floating-point inaccuracies when calculating keys, refined, reclaimed, and scrap metal.*

</div>

---

## 🎯 The Problem

Calculating Team Fortress 2 currency with standard floating-point arithmetic leads to precision errors. For example, `1.33 ref + 0.11 ref` often yields `1.4400000000000002` instead of the expected `1.44`.

`tf2-metal` solves this by converting all currency values down to their lowest common integer denominator (the "weapon"). By performing all internal math using integers, **precision errors are mathematically impossible**.

## ✨ Features

- 🛡️ **Absolute Precision**: 100% integer-based internal math. No float anomalies.
- 🧊 **Thread-Safe & Immutable**: Built on frozen dataclasses without global state. Perfect for async trading bots.
- 🧮 **Rich Arithmetic**: Native support for `+`, `-`, `*`, `/`, and logical operators (`<`, `>`, `==`).
- 📝 **Flexible Parsing**: Instantly parse user input strings like `"2k, 5.33 ref"`, `"-1.5 keys"`, or `"0.05 ref"`.
- 🔄 **Serialization**: Convert to and from Python dictionaries for easy JSON storage.
- 📏 **Rounding Modes**: Customizable strategies (`ROUND`, `FLOOR`, `CEIL`) for fractional calculations.
- 📦 **Zero Dependencies**: Relies solely on the Python standard library.

## 🚀 Quickstart

### 1. Installation

This library is intended for private/internal use. Add it to your project via git clone:

```bash
git clone https://github.com/your-username/tf2-metal.git
pip install -e tf2-metal/
```

### 2. Basic Usage (The Factory Pattern)

To avoid passing key prices manually every time you instantiate a currency, `tf2-metal` provides the `TF2Market` class. This is the recommended pattern for trading bots.

```python
from tf2_metal import TF2Market

# 1. Initialize the market once with the current prices
market = TF2Market(key_price_ref=65.0, key_price_usd=1.85)

# 2. Create and parse currencies effortlessly
wallet = market.create(keys=10, metal=5.11)
item_price = market.parse("1k, 13.33 ref")

# 3. Arithmetic Operations (Returns a new immutable TF2Currency instance)
remaining = wallet - item_price
print(remaining) 
# Output: "8 keys, 56 ref, 2 reclaimed, 1 scrap" (aka 56.77 ref)

# 4. Multiplication & Division
print(item_price * 2)
# Output: "3 keys, 13 ref"

# 5. Serialization to JSON/Dict
data = remaining.to_dict()
print(data) 
# Output: {'keys': 8, 'metal': 56.77}

# 6. Update prices later when the market changes
market.update_prices(new_ref=65.11, new_usd=1.84)
```

## 🔐 Type Safety & Consistency

To prevent arithmetic errors across fluctuating markets, `tf2-metal` enforces strict consistency checks. You cannot accidentally add or subtract two currencies evaluated at different key rates:

```python
c1 = TF2Currency(keys=1, key_price_ref=65.0)
c2 = TF2Currency(keys=1, key_price_ref=70.0)

# Raises TF2ValidationError: "Cannot perform operations on currencies with different key prices."
total = c1 + c2 
```

## 📚 Documentation

For a comprehensive machine-readable API guide tailored for Large Language Models (LLMs) or automated agents, please refer to [docs/llm_guide.md](docs/llm_guide.md).
