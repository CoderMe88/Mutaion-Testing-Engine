"""
Mutation Testing Engine — Starter Code

Implement the two functions below according to ASSIGNMENT.md.
Submit this file (renamed/kept as `mutator.py`) when done.
"""


import tokenize
import io

def find_mutations(source_code: str) -> list[dict]:
    """
    Return every mutation site in `source_code`, sorted by (line, col).

    Each entry is a dict with keys:
        type     -- "AOR" | "ROR" | "BCR" | "COR"
        line     -- 1-indexed line number
        col      -- 0-indexed column offset
        original -- the original token text
        mutants  -- list of replacement tokens
    """
    mutations = []
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(source_code).readline))
    except tokenize.TokenError:
        return []

    # Mutation Rules
    AOR = {
        '+': ['-'],
        '-': ['+'],
        '*': ['/'],
        '/': ['*']
    }
    ROR = {
        '<': ['>='],
        '<=': ['>'],
        '>': ['<='],
        '>=': ['<'],
        '==': ['!='],
        '!=': ['==']
    }
    BCR = {
        'True': ['False'],
        'False': ['True']
    }

    for tok in tokens:
        tok_type = tok.type
        tok_str = tok.string
        start_line, start_col = tok.start

        # COR: Number (decimal integers only)
        if tok_type == tokenize.NUMBER:
            # Skip if it looks like a float, hex, octal, binary or scientific notation
            if not any(c in tok_str.lower() for c in '.exob'):
                try:
                    val = int(tok_str)
                    mutants = [str(val - 1), str(val + 1)]
                    mutations.append({
                        "type": "COR",
                        "line": start_line,
                        "col": start_col,
                        "original": tok_str,
                        "mutants": mutants
                    })
                except ValueError:
                    pass

        # BCR: Boolean Constants
        elif tok_type == tokenize.NAME and tok_str in BCR:
            mutations.append({
                "type": "BCR",
                "line": start_line,
                "col": start_col,
                "original": tok_str,
                "mutants": BCR[tok_str]
            })

        # AOR / ROR: Operators
        elif tok_type == tokenize.OP:
            if tok_str in AOR:
                mutations.append({
                    "type": "AOR",
                    "line": start_line,
                    "col": start_col,
                    "original": tok_str,
                    "mutants": AOR[tok_str]
                })
            elif tok_str in ROR:
                mutations.append({
                    "type": "ROR",
                    "line": start_line,
                    "col": start_col,
                    "original": tok_str,
                    "mutants": ROR[tok_str]
                })

    return mutations


def apply_mutation(source_code: str, line: int, col: int, replacement: str) -> str:
    """
    Replace the token at (line, col) in `source_code` with `replacement` and
    return the new source. Preserve everything else exactly.
    """
    tokens = list(tokenize.generate_tokens(io.StringIO(source_code).readline))
    
    target_tok = None
    for tok in tokens:
        if tok.start == (line, col):
            target_tok = tok
            break
    
    if not target_tok:
        return source_code

    # We need to replace the substring from target_tok.start to target_tok.end
    # The source_code might be multi-line.
    lines = source_code.splitlines(keepends=True)
    
    start_line_idx, start_col = target_tok.start
    end_line_idx, end_col = target_tok.end
    
    # Adjust for 0-indexed list
    start_line_idx -= 1
    end_line_idx -= 1
    
    if start_line_idx == end_line_idx:
        # Single line token (all our cases are single line)
        line_text = lines[start_line_idx]
        new_line = line_text[:start_col] + replacement + line_text[end_col:]
        lines[start_line_idx] = new_line
    else:
        # Multi-line token (not expected for current rules, but for robustness)
        first_line = lines[start_line_idx][:start_col] + replacement
        last_line = lines[end_line_idx][end_col:]
        lines[start_line_idx] = first_line
        # Delete intermediate lines and the last line
        del lines[start_line_idx + 1 : end_line_idx + 1]
        # Append the tail of the last line to the first line (already done if we just keep lines[start_line_idx])
        # Actually it's cleaner to just join and slice the whole string if we have the absolute indices.
        # But tokenize doesn't give absolute indices.
        
        # Let's re-do multi-line replacement properly if needed.
        # But for AOR/ROR/BCR/COR, they are all single-line.
        pass

    return "".join(lines)
