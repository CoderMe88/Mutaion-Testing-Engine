# Mutation Testing Engine Implementation Plan

Implement `find_mutations` and `apply_mutation` in `mutator.py` to identify and apply code mutations for testing purposes.

## Mutation Rules (Inferred from tests)

| Type | Original | Mutants |
| :--- | :--- | :--- |
| **AOR** | `+` | `['-']` |
| **AOR** | `-` | `['+']` |
| **AOR** | `*` | `['/']` |
| **AOR** | `/` | `['*']` |
| **ROR** | `<` | `['>=']` |
| **ROR** | `<=` | `['>']` |
| **ROR** | `>` | `['<=']` |
| **ROR** | `>=` | `['<']` |
| **ROR** | `==` | `['!=']` |
| **ROR** | `!=` | `['==']` |
| **BCR** | `True` | `['False']` |
| **BCR** | `False` | `['True']` |
| **COR** | Integer `n` | `[str(n-1), str(n+1)]` |

### Notes on COR
- Only applies to integers.
- Skips floats (`1.5`, `1e3`), hex (`0x10`), and other literal types.
- For `0`, mutants are `['-1', '1']`.

## Proposed Changes

### [mutator.py](file:///f:/Mutaion%20Testing%20Engine/mutator.py)

#### [MODIFY] `find_mutations`
- Use `tokenize.tokenize` (or `io.BytesIO` + `tokenize.tokenize`) to iterate through tokens.
- For each token:
    - Check if it's an operator or keyword matching the rules.
    - If it's a `NUMBER`:
        - Check if it's an integer (doesn't contain `.`, `e`, `x`).
        - Generate `n-1` and `n+1`.
    - If it's `NAME` and matches `True` or `False`.
    - If it's `OP` and matches arithmetic or relational operators.
- Return a list of dicts as specified.

#### [MODIFY] `apply_mutation`
- Since we need to preserve everything exactly, we can't just use `untokenize`.
- We can use the line and column information to replace the specific range in the original string.
- Python's `tokenize` gives `start` and `end` as `(line, col)`.
- I'll split the source into lines and replace the substring at the specific location.

## Verification Plan

### Automated Tests
- Run `python test_public.py` and ensure all tests pass.

### Manual Verification
- Review the output of `find_mutations` for a few sample snippets.
