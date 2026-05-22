# tf2-metal

A pure Python library for Team Fortress 2 currency parsing, manipulation, and conversion.

## Usage

```python
from tf2_metal import TF2Currency

# Set global key price
TF2Currency.set_key_price_metal(66.33)

# Build instances
a = TF2Currency(keys=2, metal=13.33)
b = TF2Currency(metal=1.33)

# Math operations
total = a + b

# String representation
print(total)
```
