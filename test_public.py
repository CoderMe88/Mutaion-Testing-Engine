"""
Public self-check tests. Run with:  python3 test_public.py

Passing every test here is necessary but not sufficient — the hidden grader
uses additional programs of the same shape.
"""

from mutator import find_mutations, apply_mutation


def check(label, got, expected):
    if got == expected:
        print(f"  PASS  {label}")
        return True
    print(f"  FAIL  {label}")
    print(f"     expected: {expected!r}")
    print(f"     got:      {got!r}")
    return False


def test_simple_arithmetic():
    print("test_simple_arithmetic")
    src = "x = 1 + 2\n"
    expected = [
        {"type": "COR", "line": 1, "col": 4, "original": "1", "mutants": ["0", "2"]},
        {"type": "AOR", "line": 1, "col": 6, "original": "+", "mutants": ["-"]},
        {"type": "COR", "line": 1, "col": 8, "original": "2", "mutants": ["1", "3"]},
    ]
    ok = check("find_mutations", find_mutations(src), expected)
    ok &= check("apply +→-", apply_mutation(src, 1, 6, "-"), "x = 1 - 2\n")
    ok &= check("apply 1→0", apply_mutation(src, 1, 4, "0"), "x = 0 + 2\n")
    return ok


def test_boolean():
    print("test_boolean")
    src = "flag = True\n"
    expected = [
        {"type": "BCR", "line": 1, "col": 7, "original": "True", "mutants": ["False"]},
    ]
    ok = check("find_mutations", find_mutations(src), expected)
    ok &= check("apply True→False",
                apply_mutation(src, 1, 7, "False"),
                "flag = False\n")
    return ok


def test_two_char_relational():
    print("test_two_char_relational")
    src = "if a <= 5:\n    pass\n"
    expected = [
        {"type": "ROR", "line": 1, "col": 5, "original": "<=", "mutants": [">"]},
        {"type": "COR", "line": 1, "col": 8, "original": "5", "mutants": ["4", "6"]},
    ]
    ok = check("find_mutations", find_mutations(src), expected)
    ok &= check("apply <=→>",
                apply_mutation(src, 1, 5, ">"),
                "if a > 5:\n    pass\n")
    return ok


def test_zero_constant():
    print("test_zero_constant")
    src = "n = 0\n"
    expected = [
        {"type": "COR", "line": 1, "col": 4, "original": "0", "mutants": ["-1", "1"]},
    ]
    return check("find_mutations", find_mutations(src), expected)


def test_skips_floats_and_hex():
    print("test_skips_floats_and_hex")
    src = "a = 1.5\nb = 0x10\nc = 1e3\n"
    return check("find_mutations", find_mutations(src), [])


def test_multi_line():
    print("test_multi_line")
    src = "y = -5 * 3\nz = y == 0\n"
    expected = [
        {"type": "AOR", "line": 1, "col": 4, "original": "-", "mutants": ["+"]},
        {"type": "COR", "line": 1, "col": 5, "original": "5", "mutants": ["4", "6"]},
        {"type": "AOR", "line": 1, "col": 7, "original": "*", "mutants": ["/"]},
        {"type": "COR", "line": 1, "col": 9, "original": "3", "mutants": ["2", "4"]},
        {"type": "ROR", "line": 2, "col": 6, "original": "==", "mutants": ["!="]},
        {"type": "COR", "line": 2, "col": 9, "original": "0", "mutants": ["-1", "1"]},
    ]
    ok = check("find_mutations", find_mutations(src), expected)
    ok &= check("apply ==→!= on line 2",
                apply_mutation(src, 2, 6, "!="),
                "y = -5 * 3\nz = y != 0\n")
    return ok


def test_no_mutations():
    print("test_no_mutations")
    src = "x = 'hello'\n"
    return check("find_mutations", find_mutations(src), [])


if __name__ == "__main__":
    tests = [
        test_simple_arithmetic,
        test_boolean,
        test_two_char_relational,
        test_zero_constant,
        test_skips_floats_and_hex,
        test_multi_line,
        test_no_mutations,
    ]
    passed = sum(1 for t in tests if t())
    print(f"\n{passed}/{len(tests)} test groups fully passed")
