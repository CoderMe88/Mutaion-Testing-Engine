# Mutation Testing Engine

A Python-based mutation testing tool that evaluates test suite quality by introducing small, intentional faults (mutants) into source code.

## Overview

Mutation testing is a powerful technique to verify if your tests are actually capable of catching bugs. This engine scans Python source code, identifies "mutation sites," and generates mutated versions of the code according to predefined rules.

## Features

### Supported Mutation Types

The engine supports four core mutation categories:

1.  **AOR (Arithmetic Operator Replacement)**
    *   Swaps `+` with `-`
    *   Swaps `*` with `/`
    *   Example: `x + y` becomes `x - y`

2.  **ROR (Relational Operator Replacement)**
    *   Swaps comparison operators with their boundary opposites:
        *   `<` ↔ `>=`
        *   `<=` ↔ `>`
        *   `>` ↔ `<=`
        *   `>=` ↔ `<`
        *   `==` ↔ `!=`

3.  **BCR (Boolean Constant Replacement)**
    *   Swaps `True` with `False` and vice versa.

4.  **COR (Constant Operator Replacement)**
    *   Mutates decimal integer constants by adding or subtracting 1.
    *   Example: `n = 5` creates mutants `n = 4` and `n = 6`.
    *   *Note: Floats, hexadecimal, and scientific notation are ignored to prevent invalid mutations.*

## Usage

### Finding Mutation Sites

Use `find_mutations(source_code)` to get a list of all possible mutations.

```python
from mutator import find_mutations

src = "x = 1 + 2"
sites = find_mutations(src)
# Returns:
# [
#   {"type": "COR", "line": 1, "col": 4, "original": "1", "mutants": ["0", "2"]},
#   {"type": "AOR", "line": 1, "col": 6, "original": "+", "mutants": ["-"]},
#   ...
# ]
```

### Applying a Mutation

Use `apply_mutation(source_code, line, col, replacement)` to generate a mutated version of the source.

```python
from mutator import apply_mutation

mutated_src = apply_mutation(src, 1, 6, "-")
print(mutated_src) # Output: x = 1 - 2
```

## Running Tests

To verify the implementation, run the public test suite:

```bash
python test_public.py
```

## Implementation Details

The engine uses Python's `tokenize` module for robust source analysis. This ensures that mutations are applied only to valid code tokens and that all whitespace, comments, and formatting are preserved exactly in the generated mutants.
