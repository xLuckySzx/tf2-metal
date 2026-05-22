# CHECKLIST — tf2-metal

## Feature 0 — Scaffolding del Progetto

### Task 0.1 — Struttura directory
- [ ] Creare la directory radice `tf2-metal/`
- [ ] Creare la directory `tf2-metal/tf2_metal/`
- [ ] Creare la directory `tf2-metal/tests/`

### Task 0.2 — pyproject.toml
- [ ] Creare `tf2-metal/pyproject.toml` con `[project]`: `name = "tf2-metal"`, `requires-python = ">=3.11"`, `dependencies = []`
- [ ] Aggiungere i metadata minimi: `version`, `description`, `license`
- [ ] Verificare che nessuna dipendenza esterna sia dichiarata

### Task 0.3 — File py.typed
- [ ] Creare `tf2-metal/tf2_metal/py.typed` vuoto (marcatore PEP 484)

### Task 0.4 — README.md
- [ ] Creare `tf2-metal/README.md` con sezione d'uso minima che mostra almeno: `set_key_price_metal`, costruzione di `TF2Currency`, un'operazione aritmetica, `__str__`

---

## Feature 1 — constants.py

### Task 1.1 — Costanti intere di conversione
- [ ] Creare `tf2-metal/tf2_metal/constants.py`
- [ ] Definire `WEAPONS_PER_SCRAP: int = 2`
- [ ] Definire `WEAPONS_PER_RECLAIMED: int = 6`
- [ ] Definire `WEAPONS_PER_REF: int = 18`

### Task 1.2 — Enum RoundingMode
- [ ] Importare `Enum` da `enum`
- [ ] Definire la classe `RoundingMode(Enum)` con i tre membri: `ROUND = "round"`, `FLOOR = "floor"`, `CEIL = "ceil"`

### Task 1.3 — [TEST] constants.py
- [ ] Creare `tf2-metal/tests/test_constants.py`
- [ ] Verificare che `WEAPONS_PER_SCRAP == 2`
- [ ] Verificare che `WEAPONS_PER_RECLAIMED == 6`
- [ ] Verificare che `WEAPONS_PER_REF == 18`
- [ ] Verificare che `RoundingMode.ROUND`, `RoundingMode.FLOOR`, `RoundingMode.CEIL` esistano come membri dell'Enum
- [ ] Verificare che i valori stringa dei membri siano rispettivamente `"round"`, `"floor"`, `"ceil"`
- [ ] Verificare che il tentativo `WEAPONS_PER_SCRAP = 99` a livello di modulo (dopo import) non alteri il valore del modulo originale (le costanti sono immutabili a runtime come attributi di modulo)

---

## Feature 2 — exceptions.py

### Task 2.1 — TF2MetalError
- [ ] Creare `tf2-metal/tf2_metal/exceptions.py`
- [ ] Definire `TF2MetalError(Exception)` come classe base

### Task 2.2 — TF2ValidationError
- [ ] Definire `TF2ValidationError(TF2MetalError)` come sottoclasse

### Task 2.3 — [TEST] exceptions.py
- [ ] Creare `tf2-metal/tests/test_exceptions.py`
- [ ] Verificare che `TF2ValidationError` sia sottoclasse di `TF2MetalError`
- [ ] Verificare che `TF2MetalError` sia sottoclasse di `Exception`
- [ ] Verificare che `TF2ValidationError("messaggio")` trasporti il messaggio accessibile via `str(exc)` o `exc.args[0]`
- [ ] Verificare che `TF2MetalError("messaggio")` trasporti il messaggio accessibile via `str(exc)` o `exc.args[0]`

---

## Feature 3 — TF2Currency: variabili di classe e setter

### Task 3.1 — Variabili di classe
- [ ] Creare `tf2-metal/tf2_metal/currency.py`
- [ ] Importare `ClassVar` da `typing`, `dataclass` da `dataclasses`, `RoundingMode` da `constants`, `TF2ValidationError` da `exceptions`
- [ ] Dichiarare `key_price_ref: ClassVar[float] = 0.0` sulla classe `TF2Currency`
- [ ] Dichiarare `key_price_usd: ClassVar[float] = 0.0` sulla classe `TF2Currency`

### Task 3.2 — set_key_price_metal
- [ ] Implementare il classmethod `set_key_price_metal(cls, ref: float) -> None`
- [ ] Sollevare `TF2ValidationError` se `ref <= 0`
- [ ] Sollevare `TF2ValidationError` se `ref` è `float('inf')` o `float('-inf')`
- [ ] Sollevare `TF2ValidationError` se `ref` è `float('nan')`
- [ ] Assegnare `cls.key_price_ref = ref` solo se la validazione passa

### Task 3.3 — set_key_price_usd
- [ ] Implementare il classmethod `set_key_price_usd(cls, usd: float) -> None`
- [ ] Sollevare `TF2ValidationError` se `usd <= 0`
- [ ] Sollevare `TF2ValidationError` se `usd` è `float('inf')` o `float('-inf')`
- [ ] Sollevare `TF2ValidationError` se `usd` è `float('nan')`
- [ ] Assegnare `cls.key_price_usd = usd` solo se la validazione passa

### Task 3.4 — [TEST] setter
- [ ] Creare `tf2-metal/tests/test_setters.py`
- [ ] Aggiungere teardown (fixture o `setUp`/`tearDown`) che ripristina `key_price_ref = 0.0` e `key_price_usd = 0.0` dopo ogni test
- [ ] Verificare che `set_key_price_metal(66.33)` aggiorni `TF2Currency.key_price_ref` a `66.33`
- [ ] Verificare che istanze create dopo la chiamata al setter vedano il valore aggiornato (tramite accesso `TF2Currency.key_price_ref`)
- [ ] Verificare che `set_key_price_metal(0)` sollevi `TF2ValidationError`
- [ ] Verificare che `set_key_price_metal(-1.0)` sollevi `TF2ValidationError`
- [ ] Verificare che `set_key_price_metal(float('inf'))` sollevi `TF2ValidationError`
- [ ] Verificare che `set_key_price_metal(float('nan'))` sollevi `TF2ValidationError`
- [ ] Verificare che `set_key_price_usd(2.49)` aggiorni `TF2Currency.key_price_usd` a `2.49`
- [ ] Verificare che `set_key_price_usd(0)` sollevi `TF2ValidationError`
- [ ] Verificare che `set_key_price_usd(-1.0)` sollevi `TF2ValidationError`
- [ ] Verificare che `set_key_price_usd(float('inf'))` sollevi `TF2ValidationError`
- [ ] Verificare che `set_key_price_usd(float('nan'))` sollevi `TF2ValidationError`

---

## Feature 4 — TF2Currency: costruttore e rappresentazione interna

### Task 4.1 — Definizione dataclass
- [ ] Decorare `TF2Currency` con `@dataclass(frozen=True)`
- [ ] Dichiarare il campo `keys: int = 0`
- [ ] Dichiarare il campo `metal: float = 0.0`
- [ ] Dichiarare il campo `rounding_mode: RoundingMode = RoundingMode.ROUND`

### Task 4.2 — metal_to_weapons
- [ ] Implementare la funzione/metodo statico `metal_to_weapons(metal: float, rounding_mode: RoundingMode) -> int`
- [ ] Calcolare `raw = metal * WEAPONS_PER_REF`
- [ ] Applicare `round(raw)` se `rounding_mode == RoundingMode.ROUND`
- [ ] Applicare `math.floor(raw)` se `rounding_mode == RoundingMode.FLOOR`
- [ ] Applicare `math.ceil(raw)` se `rounding_mode == RoundingMode.CEIL`
- [ ] Restituire il risultato come `int`

### Task 4.3 — __post_init__
- [ ] Implementare `__post_init__` sulla dataclass
- [ ] Sollevare `TF2ValidationError` se `metal` è `float('inf')`, `float('-inf')` o `float('nan')`
- [ ] Sollevare `TF2ValidationError` se `keys > 0` e `TF2Currency.key_price_ref == 0.0`
- [ ] Calcolare `key_price_in_weapons = int(metal_to_weapons(TF2Currency.key_price_ref, self.rounding_mode))` quando `keys != 0`
- [ ] Calcolare `_weapons = keys * key_price_in_weapons + metal_to_weapons(metal, rounding_mode)`
- [ ] Assegnare `_weapons` tramite `object.__setattr__(self, "_weapons", _weapons)`

### Task 4.4 — [TEST] costruttore e _weapons
- [ ] Creare `tf2-metal/tests/test_constructor.py`
- [ ] Aggiungere teardown che ripristina `key_price_ref = 0.0` dopo ogni test che lo modifica
- [ ] Verificare costruzione nominale `TF2Currency(metal=18.0)` con `_weapons == 324` (18 × 18)
- [ ] Verificare costruzione nominale con `keys=1` e `key_price_ref=66.0`: `_weapons == 66*18 + 0 == 1188`
- [ ] Verificare `metal_to_weapons(1.5, RoundingMode.ROUND)`: atteso `27` (1.5 × 18 = 27.0 → 27)
- [ ] Verificare `metal_to_weapons(1.4, RoundingMode.ROUND)`: atteso `25` (1.4 × 18 = 25.2 → 25)
- [ ] Verificare `metal_to_weapons(1.4, RoundingMode.FLOOR)`: atteso `25`
- [ ] Verificare `metal_to_weapons(1.4, RoundingMode.CEIL)`: atteso `26`
- [ ] Verificare `metal_to_weapons(1.6, RoundingMode.FLOOR)`: atteso `28`
- [ ] Verificare `metal_to_weapons(1.6, RoundingMode.CEIL)`: atteso `29`
- [ ] Verificare che `TF2Currency(keys=1)` con `key_price_ref == 0.0` sollevi `TF2ValidationError`
- [ ] Verificare che `TF2Currency(metal=float('inf'))` sollevi `TF2ValidationError`
- [ ] Verificare che `TF2Currency(metal=float('-inf'))` sollevi `TF2ValidationError`
- [ ] Verificare che `TF2Currency(metal=float('nan'))` sollevi `TF2ValidationError`
- [ ] Verificare che il tentativo di assegnazione `instance.metal = 5.0` sollevi `FrozenInstanceError`
- [ ] Verificare che `TF2Currency(metal=1.0) == TF2Currency(metal=1.0)` (stesso hash e uguaglianza)
- [ ] Verificare che `hash(TF2Currency(metal=1.0)) == hash(TF2Currency(metal=1.0))`
- [ ] Verificare che `hash(TF2Currency(metal=1.0)) != hash(TF2Currency(metal=2.0))` (campione rappresentativo)
- [ ] Verificare che `TF2Currency(metal=-1.33)` non sollevi eccezioni e che `_weapons` sia negativo
- [ ] Verificare che `TF2Currency(keys=-1, metal=0.0)` con `key_price_ref > 0` non sollevi eccezioni e che `_weapons` sia negativo

---

## Feature 5 — TF2Currency: breakdown()

### Task 5.1 — Implementazione breakdown
- [ ] Implementare il metodo `breakdown(self) -> dict[str, int]`
- [ ] Se `TF2Currency.key_price_ref > 0`, calcolare `keys = self._weapons // (key_price_ref_in_weapons)` e il resto
- [ ] Se `TF2Currency.key_price_ref == 0.0`, omettere la chiave `"keys"` e partire da `_weapons` per il calcolo del refined
- [ ] Calcolare `refined = resto // WEAPONS_PER_REF` e aggiornare il resto
- [ ] Calcolare `reclaimed = resto // WEAPONS_PER_RECLAIMED` e aggiornare il resto
- [ ] Calcolare `scrap = resto // WEAPONS_PER_SCRAP` e aggiornare il resto
- [ ] Calcolare `weapons = resto` (residuo finale, 0 o 1)
- [ ] Restituire il dizionario con tutti i campi calcolati (incluso `keys` solo se `key_price_ref > 0`)
- [ ] Per valori negativi, il segno negativo deve riflettersi sul componente di testa non nullo

### Task 5.2 — [TEST] breakdown
- [ ] Creare `tf2-metal/tests/test_breakdown.py`
- [ ] Aggiungere teardown che ripristina `key_price_ref = 0.0`
- [ ] Verificare `TF2Currency(metal=1.0).breakdown()` con `key_price_ref == 0.0`: `{"refined": 1, "reclaimed": 0, "scrap": 0, "weapons": 0}`
- [ ] Verificare un valore con tutti i componenti non nulli, es. `metal = 1.0 + 6/18 + 2/18 + 1/18` con `key_price_ref == 0.0`: `{"refined": 1, "reclaimed": 1, "scrap": 1, "weapons": 1}`
- [ ] Impostare `key_price_ref = 18.0` e verificare che `TF2Currency(keys=1).breakdown()` contenga la chiave `"keys"` con valore `1`
- [ ] Verificare che con `key_price_ref == 0.0` la chiave `"keys"` sia assente dal dizionario restituito
- [ ] Verificare il comportamento con `_weapons` negativo: es. `TF2Currency(metal=-1.0).breakdown()` con `refined == -1` e gli altri a 0
- [ ] Verificare `TF2Currency(metal=0.0).breakdown()`: `{"refined": 0, "reclaimed": 0, "scrap": 0, "weapons": 0}` (senza `keys`)
- [ ] Verificare un valore pari a 1 weapon (`metal = 1/18`): `{"refined": 0, "reclaimed": 0, "scrap": 0, "weapons": 1}`

---

## Feature 6 — TF2Currency: __str__

### Task 6.1 — Implementazione __str__
- [ ] Implementare il metodo `__str__(self) -> str`
- [ ] Chiamare `self.breakdown()` per ottenere i componenti
- [ ] Includere nel formato solo i componenti con valore non nullo
- [ ] Applicare la regola singolare/plurale: `1 key` vs `N keys`, `1 weapon` vs `N weapons`, `1 ref` vs `N ref`, `1 scrap` vs `N scrap`, `1 reclaimed` vs `N reclaimed`
- [ ] Applicare la regola sub-ref: se `key_price_ref == 0.0` e il valore assoluto in weapons è inferiore a `WEAPONS_PER_REF`, formattare come `float` in ref (es. `"0.33 ref"`)
- [ ] Gestire il caso valore zero: restituire `"0 ref"`
- [ ] Gestire il segno negativo: prefissare il segno `-` sul primo componente non nullo

### Task 6.2 — [TEST] __str__
- [ ] Creare `tf2-metal/tests/test_str.py`
- [ ] Aggiungere teardown che ripristina `key_price_ref = 0.0`
- [ ] Impostare `key_price_ref = 18.0` e verificare `str(TF2Currency(keys=2, metal=12.0 + 1/18 + 2/18 + 1/18))` contiene `"2 keys"`, `"12 ref"`, `"1 reclaimed"`, `"1 scrap"`, `"1 weapon"`
- [ ] Verificare un output parziale, es. solo ref e scrap: `TF2Currency(metal=1.0 + 2/18)` → `"1 ref, 1 scrap"`
- [ ] Verificare singolare `1 key`: `TF2Currency(keys=1)` con `key_price_ref = 18.0` → stringa contenente `"1 key"` (non `"1 keys"`)
- [ ] Verificare singolare `1 weapon`: valore pari a 1 weapon → stringa contenente `"1 weapon"`
- [ ] Verificare singolare `1 ref`: `TF2Currency(metal=1.0)` → `"1 ref"`
- [ ] Verificare singolare `1 scrap`: valore pari a 1 scrap → stringa contenente `"1 scrap"`
- [ ] Verificare singolare `1 reclaimed`: valore pari a 1 reclaimed → stringa contenente `"1 reclaimed"`
- [ ] Verificare formato sub-ref: `str(TF2Currency(metal=0.33))` → `"0.33 ref"` (o equivalente float)
- [ ] Verificare valore negativo: `str(TF2Currency(metal=-1.0))` con `key_price_ref == 0.0` → contiene `"-1 ref"`
- [ ] Verificare valore zero: `str(TF2Currency())` → `"0 ref"`

---

## Feature 7 — TF2Currency: operatori +, -

### Task 7.1 — __add__
- [ ] Implementare `__add__(self, other: "TF2Currency") -> "TF2Currency"`
- [ ] Restituire `NotImplemented` se `other` non è istanza di `TF2Currency`
- [ ] Calcolare `new_weapons = self._weapons + other._weapons`
- [ ] Costruire la nuova istanza usando `rounding_mode` dell'operando sinistro (`self`)
- [ ] Restituire la nuova istanza ricavata da `new_weapons` (via metodo interno o costruzione da weapons)

### Task 7.2 — __sub__
- [ ] Implementare `__sub__(self, other: "TF2Currency") -> "TF2Currency"`
- [ ] Restituire `NotImplemented` se `other` non è istanza di `TF2Currency`
- [ ] Calcolare `new_weapons = self._weapons - other._weapons`
- [ ] Costruire la nuova istanza usando `rounding_mode` dell'operando sinistro
- [ ] Restituire la nuova istanza

### Task 7.3 — [TEST] +, -
- [ ] Creare `tf2-metal/tests/test_add_sub.py`
- [ ] Verificare somma di due istanze positive: `_weapons` risultante = somma dei singoli `_weapons`
- [ ] Verificare differenza con risultato positivo: `_weapons` risultante corretto
- [ ] Verificare differenza con risultato negativo: `_weapons` risultante è negativo
- [ ] Verificare che `rounding_mode` dell'operando sinistro sia preservato nel risultato
- [ ] Verificare che `TF2Currency(metal=1.0) + 5` sollevi `TypeError` (via `NotImplemented`)
- [ ] Verificare che `TF2Currency(metal=1.0) - "ciao"` sollevi `TypeError`
- [ ] Verificare somma con istanza a valore zero: `a + TF2Currency()` restituisce istanza con stesso `_weapons` di `a`
- [ ] Verificare che il risultato sia una nuova istanza (`result is not a` e `result is not b`)

---

## Feature 8 — TF2Currency: operatori *, /

### Task 8.1 — __mul__ e __rmul__
- [ ] Implementare `__mul__(self, scalar: int | float) -> "TF2Currency"`
- [ ] Restituire `NotImplemented` se `scalar` non è `int` o `float`
- [ ] Sollevare `TF2ValidationError` se `scalar` è `float('inf')`, `float('-inf')` o `float('nan')`
- [ ] Calcolare `new_weapons` applicando `rounding_mode` dell'istanza al prodotto `self._weapons * scalar`
- [ ] Restituire la nuova istanza
- [ ] Implementare `__rmul__(self, scalar: int | float) -> "TF2Currency"` come delega a `__mul__`

### Task 8.2 — __truediv__
- [ ] Implementare `__truediv__(self, scalar: int | float) -> "TF2Currency"`
- [ ] Restituire `NotImplemented` se `scalar` non è `int` o `float`
- [ ] Sollevare `TF2ValidationError` se `scalar == 0` (o `scalar == 0.0`)
- [ ] Sollevare `TF2ValidationError` se `scalar` è `float('inf')`, `float('-inf')` o `float('nan')`
- [ ] Calcolare `new_weapons` applicando `rounding_mode` al quoziente `self._weapons / scalar`
- [ ] Restituire la nuova istanza

### Task 8.3 — [TEST] *, /
- [ ] Creare `tf2-metal/tests/test_mul_div.py`
- [ ] Verificare moltiplicazione per intero positivo: `TF2Currency(metal=1.0) * 3` → `_weapons == 54`
- [ ] Verificare moltiplicazione per float positivo con verifica arrotondamento secondo `rounding_mode`
- [ ] Verificare `TF2Currency(metal=1.0) * -1` → `_weapons == -18`
- [ ] Verificare `TF2Currency(metal=1.0) * 0` → `_weapons == 0`
- [ ] Verificare `2 * TF2Currency(metal=1.0)` produce lo stesso risultato di `TF2Currency(metal=1.0) * 2`
- [ ] Verificare divisione per intero positivo: `TF2Currency(metal=2.0) / 2` → `_weapons == 18`
- [ ] Verificare divisione per float positivo con verifica arrotondamento
- [ ] Verificare `TF2Currency(metal=1.0) / 0` sollevi `TF2ValidationError`
- [ ] Verificare `TF2Currency(metal=1.0) / 0.0` sollevi `TF2ValidationError`
- [ ] Verificare `TF2Currency(metal=1.0) * float('inf')` sollevi `TF2ValidationError`
- [ ] Verificare `TF2Currency(metal=1.0) * float('nan')` sollevi `TF2ValidationError`
- [ ] Verificare `TF2Currency(metal=1.0) / float('inf')` sollevi `TF2ValidationError`
- [ ] Verificare `TF2Currency(metal=1.0) / float('nan')` sollevi `TF2ValidationError`
- [ ] Verificare `TF2Currency(metal=1.0) * "due"` sollevi `TypeError`
- [ ] Verificare che `rounding_mode` dell'istanza sia applicato al risultato frazionario di `*` e `/`
- [ ] Verificare che il risultato di `*` e `/` sia una nuova istanza distinta dall'originale

---

## Feature 9 — TF2Currency: operatori di confronto

### Task 9.1 — __lt__, __le__, __gt__, __ge__
- [ ] Implementare `__lt__(self, other: "TF2Currency") -> bool`
- [ ] Restituire `NotImplemented` se `other` non è istanza di `TF2Currency`
- [ ] Implementare `__le__(self, other: "TF2Currency") -> bool`
- [ ] Restituire `NotImplemented` se `other` non è istanza di `TF2Currency`
- [ ] Implementare `__gt__(self, other: "TF2Currency") -> bool`
- [ ] Restituire `NotImplemented` se `other` non è istanza di `TF2Currency`
- [ ] Implementare `__ge__(self, other: "TF2Currency") -> bool`
- [ ] Restituire `NotImplemented` se `other` non è istanza di `TF2Currency`
- [ ] Tutti i confronti operano su `self._weapons` vs `other._weapons`

### Task 9.2 — [TEST] confronto
- [ ] Creare `tf2-metal/tests/test_comparison.py`
- [ ] Verificare `TF2Currency(metal=2.0) > TF2Currency(metal=1.0)` → `True`
- [ ] Verificare `TF2Currency(metal=1.0) < TF2Currency(metal=2.0)` → `True`
- [ ] Verificare `TF2Currency(metal=1.0) == TF2Currency(metal=1.0)` → `True` (istanze distinte, stessi weapons)
- [ ] Verificare `TF2Currency(metal=1.0) != TF2Currency(metal=2.0)` → `True`
- [ ] Verificare `TF2Currency(metal=1.0) >= TF2Currency(metal=1.0)` → `True`
- [ ] Verificare `TF2Currency(metal=1.0) <= TF2Currency(metal=1.0)` → `True`
- [ ] Verificare confronto con valore negativo vs positivo: `TF2Currency(metal=-1.0) < TF2Currency(metal=1.0)` → `True`
- [ ] Verificare che `TF2Currency(metal=1.0) < 5` sollevi `TypeError`
- [ ] Verificare che `TF2Currency(metal=1.0) > "stringa"` sollevi `TypeError`

---

## Feature 10 — TF2Currency: from_string()

### Task 10.1 — Implementazione from_string
- [ ] Implementare il metodo statico `from_string(s: str, rounding_mode: RoundingMode = RoundingMode.ROUND) -> "TF2Currency"`
- [ ] Sollevare `TF2ValidationError` se `s` è stringa vuota o composta solo da whitespace
- [ ] Definire una regex che identifichi separatamente il gruppo keys (alias: `k`, `key`, `keys`) e il gruppo ref/metal (alias: `ref`, `metal`)
- [ ] Gestire la forma `"1.5 keys"` (keys frazionari): convertire tramite `key_price_ref * 1.5` in weapons, richiedendo `key_price_ref > 0`
- [ ] Gestire la forma `"2k, 5 ref"` (keys interi + metal)
- [ ] Gestire la forma `"2 keys 1.33 metal"` (forma alternativa)
- [ ] Gestire la forma `"13.33 ref"` (solo metal, nessuna key)
- [ ] Sollevare `TF2ValidationError` se la stringa contiene keys e `key_price_ref == 0.0`
- [ ] Sollevare `TF2ValidationError` se la stringa non è riconoscibile da nessuna regex
- [ ] Propagare `rounding_mode` all'istanza costruita

### Task 10.2 — [TEST] from_string
- [ ] Creare `tf2-metal/tests/test_from_string.py`
- [ ] Aggiungere teardown che ripristina `key_price_ref = 0.0`
- [ ] Verificare `TF2Currency.from_string("13.33 ref")` produce istanza con `metal ≈ 13.33` e `keys == 0`
- [ ] Impostare `key_price_ref = 66.0` e verificare `TF2Currency.from_string("2 keys")` produce istanza con `keys == 2` e `metal == 0.0`
- [ ] Verificare `TF2Currency.from_string("2k, 5 ref")` con `key_price_ref = 66.0` produce istanza con keys e metal corretti
- [ ] Verificare `TF2Currency.from_string("2 keys 1.33 metal")` con `key_price_ref = 66.0` come forma alternativa
- [ ] Verificare `TF2Currency.from_string("1.5 keys")` con `key_price_ref = 66.0`: weapons corrispondenti a 1.5 × 66 ref
- [ ] Verificare `TF2Currency.from_string("")` sollevi `TF2ValidationError`
- [ ] Verificare `TF2Currency.from_string("   ")` sollevi `TF2ValidationError`
- [ ] Verificare `TF2Currency.from_string("gibberish xyz 123abc")` sollevi `TF2ValidationError`
- [ ] Verificare `TF2Currency.from_string("2 keys")` con `key_price_ref == 0.0` sollevi `TF2ValidationError`
- [ ] Verificare che `rounding_mode=RoundingMode.FLOOR` venga propagato correttamente all'istanza risultante
- [ ] Verificare che valori negativi nella stringa (es. `"-2 keys"`) siano gestiti se la regex li supporta

---

## Feature 11 — TF2Currency: to_dict() e from_dict()

### Task 11.1 — to_dict
- [ ] Implementare il metodo `to_dict(self) -> dict[str, int | float]`
- [ ] Restituire `{"keys": int, "metal": float}` dove `metal` è espresso in Refined Metal arrotondato a 2 decimali
- [ ] Se `key_price_ref == 0.0`, restituire `keys` come `0` e calcolare `metal` da `_weapons / WEAPONS_PER_REF`
- [ ] Se `key_price_ref > 0`, calcolare prima i keys interi, poi il metal residuo

### Task 11.2 — from_dict
- [ ] Implementare il classmethod `from_dict(cls, data: dict[str, int | float], rounding_mode: RoundingMode = RoundingMode.ROUND) -> "TF2Currency"`
- [ ] Sollevare `TF2ValidationError` se il campo `"keys"` è assente da `data`
- [ ] Sollevare `TF2ValidationError` se il campo `"metal"` è assente da `data`
- [ ] Sollevare `TF2ValidationError` se `data["keys"]` ha tipo non numerico (`not isinstance(data["keys"], (int, float))`)
- [ ] Sollevare `TF2ValidationError` se `data["metal"]` ha tipo non numerico
- [ ] Sollevare `TF2ValidationError` se `data["keys"] > 0` e `key_price_ref == 0.0`
- [ ] Propagare `rounding_mode` all'istanza costruita

### Task 11.3 — [TEST] to_dict
- [ ] Creare `tf2-metal/tests/test_dict.py`
- [ ] Aggiungere teardown che ripristina `key_price_ref = 0.0`
- [ ] Impostare `key_price_ref = 66.33` e verificare `TF2Currency(keys=1, metal=13.33).to_dict()` restituisce `{"keys": 1, "metal": 13.33}`
- [ ] Verificare che il campo `"metal"` sia arrotondato a 2 decimali
- [ ] Verificare con `key_price_ref == 0.0`: `TF2Currency(metal=1.0).to_dict()` → `{"keys": 0, "metal": 1.0}`
- [ ] Verificare istanza con solo metal: `keys` è `0` nel dizionario risultante

### Task 11.4 — [TEST] from_dict
- [ ] Verificare costruzione da `{"keys": 0, "metal": 13.33}` senza `key_price_ref` → istanza corretta
- [ ] Impostare `key_price_ref = 66.33` e verificare costruzione da `{"keys": 1, "metal": 13.33}` → istanza corretta
- [ ] Verificare `from_dict({})` sollevi `TF2ValidationError` (campi mancanti)
- [ ] Verificare `from_dict({"keys": 1})` (manca `"metal"`) sollevi `TF2ValidationError`
- [ ] Verificare `from_dict({"metal": 1.0})` (manca `"keys"`) sollevi `TF2ValidationError`
- [ ] Verificare `from_dict({"keys": "uno", "metal": 1.0})` sollevi `TF2ValidationError`
- [ ] Verificare `from_dict({"keys": 1, "metal": "moltometal"})` sollevi `TF2ValidationError`
- [ ] Verificare `from_dict({"keys": 1, "metal": 0.0})` con `key_price_ref == 0.0` sollevi `TF2ValidationError`
- [ ] Verificare che `rounding_mode=RoundingMode.CEIL` venga propagato correttamente all'istanza risultante

---

## Feature 12 — __init__.py e interfaccia pubblica

### Task 12.1 — Esposizione simboli pubblici
- [ ] Creare (o completare) `tf2-metal/tf2_metal/__init__.py`
- [ ] Aggiungere `from tf2_metal.currency import TF2Currency`
- [ ] Aggiungere `from tf2_metal.constants import RoundingMode`
- [ ] Aggiungere `from tf2_metal.exceptions import TF2MetalError, TF2ValidationError`
- [ ] Definire `__all__ = ["TF2Currency", "RoundingMode", "TF2MetalError", "TF2ValidationError"]`

### Task 12.2 — [TEST] interfaccia pubblica
- [ ] Creare `tf2-metal/tests/test_public_api.py`
- [ ] Verificare che `from tf2_metal import TF2Currency` non sollevi `ImportError`
- [ ] Verificare che `from tf2_metal import RoundingMode` non sollevi `ImportError`
- [ ] Verificare che `from tf2_metal import TF2MetalError` non sollevi `ImportError`
- [ ] Verificare che `from tf2_metal import TF2ValidationError` non sollevi `ImportError`
- [ ] Verificare che `tf2_metal.__all__` contenga esattamente `["TF2Currency", "RoundingMode", "TF2MetalError", "TF2ValidationError"]`
- [ ] Verificare che nessun simbolo con prefisso `_` sia presente in `tf2_metal.__all__`
- [ ] Eseguire `from tf2_metal import *` e verificare che il namespace locale contenga esattamente i quattro simboli di `__all__`

---

## Feature 13 — Integrazione end-to-end

### Task 13.1 — Suite di test end-to-end
- [ ] Creare `tf2-metal/tests/test_e2e.py`
- [ ] Aggiungere teardown che ripristina `key_price_ref = 0.0` e `key_price_usd = 0.0` dopo ogni test

### Task 13.2 — [TEST] flusso completo dall'esempio canonico
- [ ] Impostare `TF2Currency.set_key_price_metal(66.33)` e `TF2Currency.set_key_price_usd(2.49)`
- [ ] Costruire `a = TF2Currency(keys=2, metal=13.33)` e verificare che `_weapons` sia coerente con il prezzo chiave impostato
- [ ] Costruire `b = TF2Currency(metal=1.33)` e verificare `_weapons`
- [ ] Verificare `(a + b)._weapons == a._weapons + b._weapons`
- [ ] Verificare `(a - b)._weapons == a._weapons - b._weapons`
- [ ] Verificare `(a * 2)._weapons == a._weapons * 2`
- [ ] Verificare `a > b` → `True`
- [ ] Verificare `TF2Currency.from_string("1.5 keys, 5 ref")` produce un'istanza con `_weapons` corretto
- [ ] Verificare `TF2Currency.from_dict({"keys": 1, "metal": 13.33}).to_dict()` restituisce `{"keys": 1, "metal": 13.33}`
- [ ] Verificare che `str(a)` contenga `"2 keys"` e `"13 ref"`
- [ ] Verificare che `a.breakdown()` restituisca `{"keys": 2, "refined": 13, "reclaimed": 0, "scrap": 1, "weapons": 1}` (con `key_price_ref = 66.33`, il calcolo esatto dipende dall'arrotondamento)

### Task 13.3 — [TEST] immutabilità post-costruzione
- [ ] Impostare `key_price_ref = 66.0` e costruire `a = TF2Currency(keys=1)`
- [ ] Memorizzare `weapons_before = a._weapons`
- [ ] Modificare `TF2Currency.set_key_price_metal(100.0)`
- [ ] Verificare che `a._weapons == weapons_before` (la modifica al prezzo non altera istanze già create)

### Task 13.4 — [TEST] isolamento tra sessioni di test
- [ ] Verificare che un test che chiama `set_key_price_metal` e poi ripristina `key_price_ref = 0.0` nel teardown non alteri lo stato per il test successivo
- [ ] Verificare che `key_price_ref == 0.0` e `key_price_usd == 0.0` siano i valori presenti all'inizio di ogni test della suite, grazie al teardown obbligatorio
