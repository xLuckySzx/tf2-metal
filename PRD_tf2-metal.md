# Product Requirement Document (PRD)

## Titolo del Progetto: tf2-metal

**Stato**: Approvato / Specifiche Congelate  
**Ambito**: Economia e Conversione di Valute di Team Fortress 2  
**Destinazione**: Uso privato — nessuna pubblicazione su PyPI richiesta

---

## 1. Introduzione e Obiettivi

`tf2-metal` è una libreria Python pura per il parsing, la manipolazione e la conversione delle valute di Team Fortress 2 (TF2).

**Obiettivi:**
- Eliminare gli errori di precisione della virgola mobile tramite rappresentazione intera interna.
- Fornire un oggetto matematico immutabile, type-safe e componibile.
- Esporre un'API minima: zero dipendenze esterne, zero I/O, zero caching.

Tutta la logica di alto livello (scraping, retry, caching) è delegata all'applicazione esterna.

---

## 2. Fattori di Conversione (constants.py)

Tutte le grandezze sono ricondotte all'unità minima: **weapon**.

| Unità      | Valore in weapons |
|------------|-------------------|
| 1 Weapon   | 1                 |
| 1 Scrap    | 2                 |
| 1 Reclaimed| 6                 |
| 1 Refined  | 18                |

Questi valori sono costanti intere immutabili definite in `constants.py`.

---

## 3. Requisiti Funzionali Core

### 3.1 Rappresentazione Interna

- Tutta la logica interna opera su un singolo intero `_weapons: int`.
- `_weapons` è calcolato in `__post_init__` come:
  `_weapons = keys * key_price_in_weapons + metal_to_weapons(metal, rounding_mode)`
- `metal_to_weapons(metal: float, rounding_mode: RoundingMode) -> int`:
  moltiplica `metal` per `WEAPONS_PER_REF` (18) e applica la politica di arrotondamento.

### 3.2 Immutabilità (Frozen Dataclass)

- `TF2Currency` è definita con `@dataclass(frozen=True)`.
- Ogni operazione matematica restituisce una nuova istanza distinta.
- `__hash__` e `__eq__` sono generati automaticamente da Python.

### 3.3 Costruttore

```python
@dataclass(frozen=True)
class TF2Currency:
    keys: int = 0
    metal: float = 0.0
    rounding_mode: RoundingMode = RoundingMode.ROUND
```

- `__post_init__` calcola `_weapons` tramite `object.__setattr__`.
- Solleva `TF2ValidationError` nei seguenti casi:
  - `keys > 0` e `TF2Currency.key_price_ref == 0.0` (prezzo chiavi non impostato).
  - `metal` è `float('inf')`, `float('-inf')` o `float('nan')`.
- Se `metal < 0` e `keys > 0` contemporaneamente, il segno del saldo complessivo è determinato dal totale in weapons.

### 3.4 Configurazione Globale del Prezzo delle Chiavi

`key_price_ref` e `key_price_usd` sono **variabili di classe** (`ClassVar`). Una modifica si propaga istantaneamente a tutte le istanze e a tutti i costrutti futuri.

```python
class TF2Currency:
    key_price_ref: ClassVar[float] = 0.0   # sentinella: non impostato
    key_price_usd: ClassVar[float] = 0.0   # sentinella: non impostato

    @classmethod
    def set_key_price_metal(cls, ref: float) -> None:
        """Imposta il prezzo delle chiavi in Refined Metal."""
        # Solleva TF2ValidationError se ref <= 0 oppure ref è inf o nan
        cls.key_price_ref = ref

    @classmethod
    def set_key_price_usd(cls, usd: float) -> None:
        """Imposta il prezzo delle chiavi in dollari USD."""
        # Solleva TF2ValidationError se usd <= 0 oppure usd è inf o nan
        cls.key_price_usd = usd
```

### 3.5 Modalità di Arrotondamento (RoundingMode)

Enum definita in `constants.py`:

```python
class RoundingMode(Enum):
    ROUND = "round"   # default — arrotonda all'intero più vicino
    FLOOR = "floor"   # arrotonda per difetto
    CEIL  = "ceil"    # arrotonda per eccesso
```

### 3.6 Scomposizione Fisica (breakdown)

Metodo `breakdown() -> dict[str, int]` che scompone `_weapons` in ordine decrescente:

1. `keys`: intero, solo se `key_price_ref > 0` (divisione intera su `_weapons`).
2. `refined`: divisione intera del resto per 18.
3. `reclaimed`: divisione intera del resto per 6.
4. `scrap`: divisione intera del resto per 2.
5. `weapons`: residuo finale (0 o 1).

Se `key_price_ref == 0.0`, `keys` è omesso e il calcolo parte da `refined`.

### 3.7 Valori Negativi

- La libreria supporta nativamente istanze con valore negativo (delta di prezzo, bilanci).
- `_weapons` può essere negativo.
- `breakdown()` e `__str__` riflettono il segno negativo sul componente di testa non nullo (es: `-2 keys, 3 ref`).

---

## 4. Requisiti Funzionali Avanzati

### 4.1 Operatori Algebrici

| Operatore | Operandi                        | Comportamento |
|-----------|---------------------------------|---------------|
| `+`, `-`  | `TF2Currency` + `TF2Currency`   | Somma/differenza di `_weapons`. Restituisce nuova istanza con `rounding_mode` dell'operando sinistro. |
| `*`, `/`  | `TF2Currency` × `int \| float`  | Moltiplica/divide `_weapons`. Applica `rounding_mode` dell'istanza. Restituisce nuova istanza. |
| `==`, `<`, `>`, `<=`, `>=` | `TF2Currency` vs `TF2Currency` | Confronto diretto su `_weapons`. |

- La divisione per zero solleva `TF2ValidationError`.
- Gli operatori `*` e `/` con uno scalare non richiedono `key_price_ref`.
- Scalare `inf` o `nan`: l'operatore intercetta l'`OverflowError` di Python e solleva `TF2ValidationError`.
- Operandi di tipo non supportato: l'operatore restituisce `NotImplemented`; Python solleva `TypeError` nativo.

### 4.2 Parser Regex (from_string)

```python
@staticmethod
def from_string(
    s: str,
    rounding_mode: RoundingMode = RoundingMode.ROUND
) -> "TF2Currency":
```

- Accetta stringhe non strutturate: `"1.5 keys"`, `"13.33 ref"`, `"2k, 5 ref"`, `"2 keys 1.33 metal"`.
- Regex identifica separatamente il gruppo keys e il gruppo ref/metal.
- Se la stringa contiene keys e `key_price_ref` non è impostato → `TF2ValidationError`.
- Stringa vuota o composta solo da whitespace → `TF2ValidationError`.
- Se la stringa non è riconoscibile → `TF2ValidationError`.

### 4.3 Formattazione Canonica (__str__)

Chiama `breakdown()` e formatta solo i componenti con valore non nullo:

```
"2 keys, 12 ref, 1 reclaimed, 1 scrap, 1 weapon"
"1 key, 3 ref, 2 scrap"
"-2 keys, 1 ref"
"0.33 ref"   # solo scrap e weapon → formato compatto in ref
```

Regola: se il valore è puramente in metallo inferiore a 1 ref, mostra il float ref equivalente.

### 4.4 Serializzazione dict

```python
def to_dict(self) -> dict[str, int | float]:
    """Restituisce {"keys": int, "metal": float}.
    metal è espresso in Refined Metal arrotondato a 2 decimali.
    keys è 0 se key_price_ref non è impostato."""

@classmethod
def from_dict(
    cls,
    data: dict[str, int | float],
    rounding_mode: RoundingMode = RoundingMode.ROUND
) -> "TF2Currency":
    """Costruisce da {"keys": int, "metal": float}.
    Solleva TF2ValidationError se:
    - mancano i campi "keys" o "metal";
    - i valori hanno tipo non numerico;
    - data["keys"] > 0 e key_price_ref non è impostato."""
```

---

## 5. Gestione degli Errori ed Eccezioni Custom (exceptions.py)

```
TF2MetalError          ← classe base; non istanziare direttamente
└── TF2ValidationError ← tutti i casi di input non valido:
                         key_price_ref/usd <= 0, inf o nan nei setter;
                         keys > 0 con key_price_ref non impostato;
                         metal = inf o nan nel costruttore;
                         scalare inf o nan in __mul__ / __truediv__;
                         stringa vuota o non riconoscibile in from_string;
                         dict malformato in from_dict;
                         divisione per zero
```

Operatori con tipo non supportato: restituiscono `NotImplemented` — Python solleva `TypeError` nativo (pattern stdlib standard).

Ogni eccezione trasporta un messaggio descrittivo. Nessun wrapping di eccezioni esterne.

---

## 6. Architettura dei Moduli e Struttura File

```
tf2-metal/
├── tf2_metal/
│   ├── py.typed              # Marcatore PEP 484 per linter e IDE
│   ├── __init__.py           # Espone: TF2Currency, RoundingMode,
│   │                         #         TF2MetalError, TF2ValidationError
│   ├── constants.py          # RoundingMode (Enum), WEAPONS_PER_REF,
│   │                         # WEAPONS_PER_RECLAIMED, WEAPONS_PER_SCRAP
│   ├── exceptions.py         # TF2MetalError, TF2ValidationError
│   └── currency.py           # TF2Currency (dataclass, tutta la logica)
│
├── tests/                    # Test unitari; mock non necessari (no I/O)
├── README.md
└── pyproject.toml            # Nessuna dipendenza esterna
```

**Dipendenze**: nessuna. La libreria usa esclusivamente la stdlib Python (≥ 3.11).

---

## 7. Interfaccia Pubblica (__init__.py)

```python
from tf2_metal.currency import TF2Currency
from tf2_metal.constants import RoundingMode
from tf2_metal.exceptions import TF2MetalError, TF2ValidationError

__all__ = [
    "TF2Currency",
    "RoundingMode",
    "TF2MetalError",
    "TF2ValidationError",
]
```

---

## 8. Esempio d'Uso Canonico

```python
from tf2_metal import TF2Currency, RoundingMode

# 1. Impostare il prezzo delle chiavi (da scraper esterno)
TF2Currency.set_key_price_metal(66.33) # in Refined Metal
TF2Currency.set_key_price_usd(2.49)    # in USD

# 2. Costruzione
a = TF2Currency(keys=2, metal=13.33)
b = TF2Currency(metal=1.33)

# 3. Aritmetica
total = a + b                          # nuova istanza
delta = a - b
scaled = a * 2

# 4. Confronto
assert a > b

# 5. Parsing
c = TF2Currency.from_string("1.5 keys, 5 ref")

# 6. Serializzazione
d = TF2Currency.from_dict({"keys": 1, "metal": 13.33})
print(d.to_dict())                     # {"keys": 1, "metal": 13.33}

# 7. Formattazione
print(a)                               # "2 keys, 13 ref, 1 scrap, 1 weapon"

# 8. Scomposizione
print(a.breakdown())
# {"keys": 2, "refined": 13, "reclaimed": 0, "scrap": 1, "weapons": 1}
```

---

## 9. Vincoli e Decisioni Esplicite

| Tema | Decisione |
|------|-----------|
| Dipendenze esterne | Zero — stdlib only |
| I/O di rete | Escluso — delegato all'applicazione esterna |
| Asincronia | Esclusa — libreria sincrona pura |
| Caching / retry | Esclusi |
| Pubblicazione PyPI | Non richiesta |
| Versione Python minima | 3.11 |
| Stile | PEP 484 rigoroso, `@dataclass(frozen=True)` |
