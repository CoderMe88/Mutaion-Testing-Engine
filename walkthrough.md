# Mutation Testing Engine Walkthrough

I have implemented the core functionality for finding and applying mutations in Python source code.

## Changes Made

### [mutator.py](file:///f:/Mutaion%20Testing%20Engine/mutator.py)

#### `find_mutations(source_code: str)`
- Leverages `tokenize.generate_tokens` to parse the source code.
- **Arithmetic (AOR)**: Swaps `+` with `-`, `*` with `/`, and vice versa.
- **Relational (ROR)**: Implements boundary-opposite mutations for all standard relational operators (`<`, `<=`, `>`, `>=`, `==`, `!=`).
- **Boolean (BCR)**: Swaps `True` and `False`.
- **Constant (COR)**: Identifies decimal integers and generates `n-1` and `n+1`. It correctly ignores floats, hex, and scientific notation as per the requirements.

#### `apply_mutation(source_code: str, line: int, col: int, replacement: str)`
- Tokenizes the source to find the exact token starting at the specified coordinates.
- Slices the original string to replace the token, ensuring that all other characters (whitespace, comments, etc.) are preserved exactly.
- Handles multi-line input by splitting and joining lines appropriately.

## Verification

### Automated Tests
I executed `test_public.py` with `PYTHONUTF8=1` to handle Unicode characters in the test output.

**Result**: All 7 test groups passed.

```text
test_simple_arithmetic
  PASS  find_mutations
  PASS  apply +→-
  PASS  apply 1→0
test_boolean
  PASS  find_mutations
  PASS  apply True→False
test_two_char_relational
  PASS  find_mutations
  PASS  apply <=→>
test_zero_constant
  PASS  find_mutations
test_skips_floats_and_hex
  PASS  find_mutations
test_multi_line
  PASS  find_mutations
  PASS  apply ==→!= on line 2
test_no_mutations
  PASS  find_mutations

7/7 test groups fully passed
```
