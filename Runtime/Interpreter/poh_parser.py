from __future__ import annotations
from typing import List, Tuple, Optional
import re
import difflib

from .poh_ast import (
    Program,
    Stmt,
    WriteStmt,
    AskStmt,
    SetStmt,
    IncStmt,
    DecStmt,
    IfStmt,
    WhileStmt,
    RepeatStmt,
    BlockStmt,
    FunctionDefStmt,
    ReturnStmt,
    UseStmt,
    ImportStmt,
    StopStmt,
    SkipStmt,
    LiteralExpr,
    IdentifierExpr,
    BinaryExpr,
    UnaryExpr,
    CallExpr,
    PredicateExpr,
    RandomIntBetweenExpr,
    RandomFloatBetweenExpr,
    RandomFromExpr,
    ContainsExpr,
    AllPredicateExpr,
    AnyPredicateExpr,
    ListLiteralExpr,
    DictLiteralExpr,
    AtExpr,
    KeysOfExpr,
    ValuesOfExpr,
    AddToListStmt,
    RemoveFromListStmt,
    AddToDictStmt,
    RemoveFromDictStmt,
    DebugStmt,
    NthItemExpr,
    SetNthItemStmt,
    RemoveLastItemStmt,
    CallValueStmt,
)


class ParseError(Exception):
    def __init__(self, msg: str, line: Optional[int] = None, col: Optional[int] = None, file: Optional[str] = None):
        self.line = line
        self.col = col
        self.file = file or '<stdin>'
        parts = [self.file]
        if line is not None:
            parts.append(f"Line {line}")
        if col is not None:
            parts.append(f"Col {col}")
        prefix = f"[{':'.join(parts)}] "
        super().__init__(prefix + msg)


# Public API ---------------------------------------------------------------

def parse_program(lines: List[str], filename: Optional[str] = None) -> Program:
    cleaned: List[Tuple[int, str]] = []
    for i, raw in enumerate(lines, 1):
        line = _strip_comment(raw.rstrip("\n"))
        if line.strip():
            cleaned.append((i, line))
    i = 0
    stmts: List[Stmt] = []
    while i < len(cleaned):
        stmt, i = _parse_stmt_or_block(cleaned, i)
        stmts.append(stmt)
    return Program(stmts)


# Statement Parsing -------------------------------------------------------

def _parse_stmt_or_block(cleaned: List[Tuple[int, str]], i: int) -> Tuple[Stmt, int]:
    ln, line = cleaned[i]
    # Keep original line for column calculations on unknown keywords; use stripped for keyword detection
    raw_line = line
    s = line.strip()
    low = s.lower()

    # Block IF
    if low.startswith("if ") and " write " not in low:
        cond_src = s[3:].strip()
        i += 1
        then_body: List[Stmt] = []
        else_body: Optional[List[Stmt]] = None
        while i < len(cleaned):
            ln2, raw2 = cleaned[i]
            t = raw2.strip()
            l2 = t.lower()
            if l2 == "otherwise":
                else_body = []
                i += 1
                while i < len(cleaned):
                    ln3, raw3 = cleaned[i]
                    t3 = raw3.strip()
                    l3 = t3.lower()
                    if l3 in ("end", "end if"):
                        i += 1
                        return IfStmt(_parse_bool_expr(cond_src, ln), then_body, else_body, ln), i
                    if l3.startswith("end "):
                        raise ParseError(f"Mismatched '{t3}'; expected 'End' or 'End If'", ln3)
                    stmt3, i = _parse_stmt_or_block(cleaned, i)
                    else_body.append(stmt3)
                raise ParseError("If block not closed with End/End If", ln)
            if l2 in ("end", "end if"):
                i += 1
                return IfStmt(_parse_bool_expr(cond_src, ln), then_body, else_body, ln), i
            if l2.startswith("end "):
                raise ParseError(f"Mismatched '{t}'; expected 'End' or 'End If'", ln2)
            stmt2, i = _parse_stmt_or_block(cleaned, i)
            then_body.append(stmt2)
        raise ParseError("If block not closed with End/End If", ln)

    # Block WHILE
    if low.startswith("while ") and " write " not in low:
        cond_src = s[6:].strip()
        i += 1
        body: List[Stmt] = []
        while i < len(cleaned):
            ln2, raw2 = cleaned[i]
            t = raw2.strip()
            l2 = t.lower()
            if l2 in ("end", "end while"):
                i += 1
                return WhileStmt(_parse_bool_expr(cond_src, ln), body, ln), i
            if l2.startswith("end "):
                raise ParseError(f"Mismatched '{t}'; expected 'End' or 'End While'", ln2)
            stmt2, i = _parse_stmt_or_block(cleaned, i)
            body.append(stmt2)
        raise ParseError("While block not closed with End/End While", ln)

    # Block REPEAT
    if low.startswith("repeat ") and " write " not in low:
        count_src = s[7:].strip()
        i += 1
        body: List[Stmt] = []
        while i < len(cleaned):
            ln2, raw2 = cleaned[i]
            t = raw2.strip()
            l2 = t.lower()
            if l2 in ("end", "end repeat"):
                i += 1
                return RepeatStmt(_parse_expr(count_src, ln), body, ln), i
            if l2.startswith("end "):
                raise ParseError(f"Mismatched '{t}'; expected 'End' or 'End Repeat'", ln2)
            stmt2, i = _parse_stmt_or_block(cleaned, i)
            body.append(stmt2)
        raise ParseError("Repeat block not closed with End/End Repeat", ln)

    # Anonymous Block: Begin ... End
    if low == "begin":
        i += 1
        body: List[Stmt] = []
        while i < len(cleaned):
            ln2, raw2 = cleaned[i]
            t = raw2.strip()
            l2 = t.lower()
            if l2 == "end":
                i += 1
                return BlockStmt(body, ln), i
            if l2.startswith("end "):
                raise ParseError(f"Mismatched '{t}'; expected 'End'", ln2)
            stmt2, i = _parse_stmt_or_block(cleaned, i)
            body.append(stmt2)
        raise ParseError("Block starting at Begin not closed with End", ln)

    # Function block (with optional 'function' keyword and defaults)
    # Make function name with A, B set to 0
    if low.startswith("make ") and " write " not in low and not re.match(r"(?i)^make\s+a\s+(mutable\s+)?(list|dictionary)\b", s.strip()):
        rest = s[5:].strip()
        # Optional 'function' keyword
        if rest.lower().startswith('function '):
            rest = rest[9:].strip()
        name, params, defaults = _parse_func_sig_with_defaults(rest, ln)
        i += 1
        body: List[Stmt] = []
        while i < len(cleaned):
            ln2, raw2 = cleaned[i]
            t = raw2.strip()
            l2 = t.lower()
            if l2 == "end":
                i += 1
                return FunctionDefStmt(name, params, defaults, body, ln), i
            if l2.startswith("end "):
                raise ParseError(f"Mismatched '{t}'; expected 'End'", ln2)
            if l2.startswith("return"):
                expr_src = t[6:].strip()
                body.append(ReturnStmt(_parse_expr(expr_src, ln2) if expr_src else None, ln2))
                i += 1
                continue
            stmt2, i = _parse_stmt_or_block(cleaned, i)
            body.append(stmt2)
        raise ParseError("Function block not closed with End", ln)

    # Fallback single-line
    st = _parse_single_stmt(ln, raw_line)
    return st, i + 1


def _parse_single_stmt(ln: int, s: str) -> Stmt:
    orig = s
    trim = s.strip()
    low = trim.lower()

    # Phrasal list/dict statements first (specific forms)
    # Make a (mutable) list of X, Y, and Z
    m = re.match(r"(?i)^make\s+a\s+(mutable\s+)?list\s+of(?:\s+(.*))?$", trim)
    if m:
        is_mutable = bool(m.group(1))
        items_src = m.group(2) or ""
        # Allow optional 'and' before last item
        items_src = re.sub(r"(?i)\s+and\s+", ",", items_src)
        items = _split_top_level(items_src)
        return SetStmt("it", ListLiteralExpr([_parse_expr(it.strip(), ln) for it in items if it.strip()], mutable=is_mutable), ln)

    # Make a (mutable) dictionary with k1 as v1 and k2 as v2
    m = re.match(r"(?i)^make\s+a\s+(mutable\s+)?dictionary\s+with\s+(.+)$", trim)
    if m:
        is_mutable = bool(m.group(1))
        pairs_src = m.group(2)
        # Replace ' and ' between pairs with comma to split
        pairs_src = re.sub(r"(?i)\s+and\s+", ",", pairs_src)
        # Pairs of form KEY as VAL
        parts = _split_top_level(pairs_src)
        kv_exprs = []
        for part in parts:
            mm = re.match(r"(?i)^(.*)\s+as\s+(.*)$", part.strip())
            if not mm:
                raise ParseError("dictionary entry must be '<key> as <value>'", ln)
            k_src = mm.group(1).strip()
            v_src = mm.group(2).strip()
            kv_exprs.append((_parse_expr(k_src, ln), _parse_expr(v_src, ln)))
        return SetStmt("it", DictLiteralExpr(kv_exprs, mutable=is_mutable), ln)

    # Set the Nth item in <list> to VALUE
    m = re.match(r"(?i)^set\s+the\s+(.*)\s+item\s+in\s+(.*)\s+to\s+(.*)$", trim)
    if m:
        idx_src = m.group(1)
        cont_src = m.group(2)
        val_src = m.group(3)
        return SetNthItemStmt(_parse_expr(idx_src, ln), _parse_expr(cont_src, ln), _parse_expr(val_src, ln), ln)

    # Remove the last item from <list>
    m = re.match(r"(?i)^remove\s+the\s+last\s+item\s+from\s+(.*)$", trim)
    if m:
        return RemoveLastItemStmt(_parse_expr(m.group(1).strip(), ln), ln)

    # Add VALUE to <list> (already supported but keep compatibility with phrasing)
    # handled later by existing AddToListStmt rule

    # Tell me the length of <list>
    m = re.match(r"(?i)^tell\s+me\s+the\s+length\s+of\s+(.*)$", trim)
    if m:
        return WriteStmt(CallExpr('length', [_parse_expr(m.group(1).strip(), ln)], line=ln), ln)

    # Give me the keys of <dict>
    m = re.match(r"(?i)^give\s+me\s+the\s+keys\s+of\s+(.*)$", trim)
    if m:
        return WriteStmt(KeysOfExpr(_parse_expr(m.group(1).strip(), ln)), ln)

    # Give me the values of <dict>
    m = re.match(r"(?i)^give\s+me\s+the\s+values\s+of\s+(.*)$", trim)
    if m:
        return WriteStmt(ValuesOfExpr(_parse_expr(m.group(1).strip(), ln)), ln)

    # Check if <dict> has KEY
    m = re.match(r"(?i)^check\s+if\s+(.*)\s+has\s+(.*)$", trim)
    if m:
        dict_src = m.group(1).strip()
        key_src = m.group(2).strip()
        return WriteStmt(ContainsExpr(_parse_expr(dict_src, ln), _parse_expr(key_src, ln)), ln)

    # Write
    if low.startswith("write "):
        return WriteStmt(_parse_expr(trim[6:].strip(), ln), ln)

    # Ask for
    if low.startswith("ask for "):
        body = trim[8:].strip()
        parts = body.split()
        if len(parts) >= 2 and parts[-1].lower() in ("number", "decimal"):
            kind = "number" if parts[-1].lower() == "number" else "decimal"
            name = " ".join(parts[:-1])
            return AskStmt(name, kind, ln)
        return AskStmt(body, "text", ln)

    # Set
    if low.startswith("set "):
        rest = trim[4:].strip()
        if " to " in rest.lower():
            name, expr_src = re.split(r"(?i)\s+to\s+", rest, maxsplit=1)
        else:
            parts = rest.split(" ", 1)
            if len(parts) != 2:
                raise ParseError("Malformed Set statement", ln)
            name, expr_src = parts
        return SetStmt(name.strip(), _parse_expr(expr_src.strip(), ln), ln)

    # Return (allowed inside function bodies, including nested blocks). We don't enforce
    # context here; if used outside a function the interpreter will raise at runtime
    # when the _ReturnSignal escapes to top-level (which we could optionally refine later).
    if low.startswith("return"):
        expr_src = trim[6:].strip()
        return ReturnStmt(_parse_expr(expr_src, ln) if expr_src else None, ln)

    # Increase / Decrease
    if low.startswith("increase "):
        rest = trim[9:].strip()
        if " by " in rest.lower():
            name, amt = re.split(r"(?i)\s+by\s+", rest, maxsplit=1)
        else:
            name, amt = rest, "1"
        return IncStmt(name.strip(), _parse_expr(amt.strip(), ln), ln)
    if low.startswith("decrease "):
        rest = trim[9:].strip()
        if " by " in rest.lower():
            name, amt = re.split(r"(?i)\s+by\s+", rest, maxsplit=1)
        else:
            name, amt = rest, "1"
        return DecStmt(name.strip(), _parse_expr(amt.strip(), ln), ln)

    # Add / Remove (list or dict)
    if low.startswith("add ") and " to " in low:
        value_src, target_src = re.split(r"(?i)\s+to\s+", trim[4:].strip(), maxsplit=1)
        if ":" in value_src:
            k, v = value_src.split(":", 1)
            return AddToDictStmt(_parse_expr(k.strip(), ln), _parse_expr(v.strip(), ln), _parse_expr(target_src.strip(), ln), ln)
        return AddToListStmt(_parse_expr(value_src.strip(), ln), _parse_expr(target_src.strip(), ln), ln)
    if low.startswith("remove ") and " from " in low:
        value_src, target_src = re.split(r"(?i)\s+from\s+", trim[7:].strip(), maxsplit=1)
        if value_src.strip().startswith(('"', "'")):
            return RemoveFromDictStmt(_parse_expr(value_src.strip(), ln), _parse_expr(target_src.strip(), ln), ln)
        return RemoveFromListStmt(_parse_expr(value_src.strip(), ln), _parse_expr(target_src.strip(), ln), ln)

    # Inline If / While / Repeat / Make
    if low.startswith("if ") and " write " in low:
        # If cond Write expr [Otherwise Write expr]
        m = re.match(r"(?i)if (.*) write (.*)", trim)
        if not m:
            raise ParseError("Malformed inline If", ln)
        cond_part = m.group(1)
        then_part = m.group(2)
        ow = re.search(r"(?i) otherwise write ", then_part)
        else_block = None
        if ow:
            then_expr_src = then_part[: ow.start()].strip()
            else_expr_src = then_part[ow.end():].strip()
            then_stmt = WriteStmt(_parse_expr(then_expr_src, ln), ln)
            else_block = [WriteStmt(_parse_expr(else_expr_src, ln), ln)]
        else:
            then_stmt = WriteStmt(_parse_expr(then_part.strip(), ln), ln)
        return IfStmt(_parse_bool_expr(cond_part, ln), [then_stmt], else_block, ln)

    if low.startswith("while ") and " write " in low:
        m = re.match(r"(?i)while (.*) write (.*)", trim)
        if not m:
            raise ParseError("Malformed inline While", ln)
        cond_src = m.group(1)
        expr_src = m.group(2)
        return WhileStmt(_parse_bool_expr(cond_src, ln), [WriteStmt(_parse_expr(expr_src, ln), ln)], ln)

    if low.startswith("repeat ") and " write " in low:
        m = re.match(r"(?i)repeat (.*) write (.*)", trim)
        if not m:
            raise ParseError("Malformed inline Repeat", ln)
        count_src = m.group(1)
        expr_src = m.group(2)
        return RepeatStmt(_parse_expr(count_src, ln), [WriteStmt(_parse_expr(expr_src, ln), ln)], ln)

    if low.startswith("make ") and " write " in low:
        rest = trim[5:].strip()
        # Split signature and expression at the first ' write '
        m = re.search(r"(?i)\swrite\s", rest)
        if not m:
            raise ParseError("Malformed inline Make", ln)
        sig_part = rest[:m.start()].rstrip()
        expr_src = rest[m.end():].strip()
        if sig_part.lower().startswith('function '):
            sig_part = sig_part[9:].strip()
        name, params, defaults = _parse_func_sig_with_defaults(sig_part, ln)
        return FunctionDefStmt(name, params, defaults, [ReturnStmt(_parse_expr(expr_src, ln), ln)], ln)

    if low.startswith("use "):
        rest = trim[4:].strip()
        name, args = _parse_call_sig(rest, ln)
        return UseStmt(name, [_parse_expr(a, ln) for a in args], ln)

    # Direct call form: Call <name> [with args]
    if low.startswith('call '):
        rest = trim[5:].strip()
        # allow calling function via variable: Call fvar with 1,2
        if ' with ' in rest.lower():
            target, tail = re.split(r"(?i)\swith\s", rest, maxsplit=1)
            args = [a.strip() for a in _split_top_level(tail) if a.strip()]
        else:
            target, args = rest, []
        # If target is identifier, parse as IdentifierExpr; else generic expr
        target_expr = IdentifierExpr(target) if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", target) else _parse_expr(target, ln)
        return CallValueStmt(target_expr, [_parse_expr(a, ln) for a in args], ln)

    if low.startswith("import "):
        # Import system "name" | Import "path"
        m_sys = re.match(r"(?i)^import\s+system\s+\"(.*)\"$", trim)
        if m_sys:
            return ImportStmt(m_sys.group(1), ln, system=True)
        m = re.match(r"(?i)^import\s+\"(.*)\"$", trim)
        if not m:
            raise ParseError("Import expects a quoted path", ln)
        return ImportStmt(m.group(1), ln)

    if low == "stop":
        return StopStmt(ln)
    if low == "skip":
        return SkipStmt(ln)

    if low in ("debug on", "debug off"):
        return DebugStmt(enabled=(low == "debug on"), line=ln)

    # Unknown statement suggestion
    KNOWN = [
        'write','ask','set','increase','decrease','if','while','repeat','make','use','import','stop','skip','debug'
    ]
    head = trim.split()[0].lower() if trim.split() else trim.lower()
    suggestion = difflib.get_close_matches(head, KNOWN, n=1)
    # Compute column (first non-space char = 1-based)
    stripped_index = 0
    while stripped_index < len(orig) and orig[stripped_index].isspace():
        stripped_index += 1
    col = stripped_index + 1
    if suggestion:
        raise ParseError(f"Unknown statement '{s}'. Did you mean '{suggestion[0]}'?", ln, col=col)
    raise ParseError(f"Unknown statement: {s}", ln, col=col)


# Helpers -----------------------------------------------------------------

def _parse_func_sig_with_defaults(src: str, ln: int) -> Tuple[str, List[str], List[Optional[object]]]:
    # Parse: name [with A [set to expr], B [set to expr], ...]
    if " with " in src.lower():
        name, tail = re.split(r"(?i)\swith\s", src, maxsplit=1)
        raw_params = [p.strip() for p in _split_top_level(tail) if p.strip()]
    else:
        name, raw_params = src, []
    params: list[str] = []
    defaults: list[Optional[object]] = []
    for rp in raw_params:
        m = re.match(r"(?i)^([A-Za-z_][A-Za-z0-9_]*)\s+set\s+to\s+(.*)$", rp)
        if m:
            pname = m.group(1)
            pexpr = m.group(2)
            params.append(pname)
            defaults.append(_parse_expr(pexpr, ln))
        else:
            params.append(rp)
            defaults.append(None)
    return name.strip(), params, defaults


def _parse_call_sig(src: str, ln: int) -> Tuple[str, List[str]]:
    if " with " in src.lower():
        name, tail = re.split(r"(?i)\swith\s", src, maxsplit=1)
        args = [p.strip() for p in tail.split(',') if p.strip()]
    else:
        name, args = src, []
    return name.strip(), args


# Boolean / Logical -------------------------------------------------------

def _parse_bool_expr(src: str, ln: int):
    s = src.strip()
    s = re.sub(r"(?i)\bis not\b", " != ", s)
    s = re.sub(r"(?i)\bis at least\b", " >= ", s)
    s = re.sub(r"(?i)\bis at most\b", " <= ", s)
    s = re.sub(r"(?i)\bis greater than\b", " > ", s)
    s = re.sub(r"(?i)\bis less than\b", " < ", s)
    pred_match = re.search(r"(?i)^(.*)\bis\s+(even|odd|positive|negative)\s*$", s)
    if pred_match:
        value_src = pred_match.group(1).strip()
        pred = pred_match.group(2).lower()
        return PredicateExpr(pred, _parse_expr(value_src, ln))
    s = re.sub(r"(?i)\bis\b", " == ", s)
    s = re.sub(r"(?i)\band\b", " && ", s)
    s = re.sub(r"(?i)\bor\b", " || ", s)
    s = re.sub(r"(?i)\bnot\b", " ! ", s)
    return _parse_logic_expr(s, ln)


# Expression Parsing ------------------------------------------------------

def _parse_expr(src: str, ln: int):
    # Random expressions
    s = src.strip()
    # Phrasal access: Take the Nth item from <list>
    m = re.match(r"(?i)^take\s+the\s+(.*)\s+item\s+from\s+(.*)$", s)
    if m:
        idx_src = m.group(1).strip()
        cont_src = m.group(2).strip()
        return NthItemExpr(_parse_expr(idx_src, ln), _parse_expr(cont_src, ln), line=ln)
    # Phrasal dict lookup: Take the value of KEY from <dict>
    m = re.match(r"(?i)^take\s+the\s+value\s+of\s+(.*)\s+from\s+(.*)$", s)
    if m:
        key_src = m.group(1).strip()
        dict_src = m.group(2).strip()
        return AtExpr(_parse_expr(dict_src, ln), _parse_expr(key_src, ln), line=ln)
    m = re.match(r"(?i)^random\s+decimal\s+between\s+(.*)\s+(?:and|to)\s+(.*)$", s)
    if m:
        return RandomFloatBetweenExpr(_parse_expr(m.group(1).strip(), ln), _parse_expr(m.group(2).strip(), ln))
    m = re.match(r"(?i)^random\s+between\s+(.*)\s+(?:and|to)\s+(.*)$", s)
    if m:
        return RandomIntBetweenExpr(_parse_expr(m.group(1).strip(), ln), _parse_expr(m.group(2).strip(), ln))
    m = re.match(r"(?i)^random\s+from\s+(.*)$", s)
    if m:
        return RandomFromExpr(_parse_expr(m.group(1).strip(), ln))
    m = re.match(r"(?i)^contains\s+(.*)\s+in\s+(.*)$", s)
    if m:
        return ContainsExpr(_parse_expr(m.group(2).strip(), ln), _parse_expr(m.group(1).strip(), ln))
    m = re.match(r"(?i)^all\s+(.*)\s+are\s+(even|odd|positive|negative)$", s)
    if m:
        return AllPredicateExpr(_parse_expr(m.group(1).strip(), ln), m.group(2).lower())
    m = re.match(r"(?i)^any\s+(.*)\s+is\s+(even|odd|positive|negative)$", s)
    if m:
        return AnyPredicateExpr(_parse_expr(m.group(1).strip(), ln), m.group(2).lower())
    # List literal (legacy mutable): List contains a, b, c
    if re.match(r"(?i)^list\s+contains\b", s):
        # Allow zero or more spaces after 'contains' to support empty default like 'List contains'
        tail = re.sub(r"(?i)^list\s+contains\b\s*", "", s)
        items = _split_top_level(tail)
        return ListLiteralExpr([_parse_expr(it.strip(), ln) for it in items if it.strip()], mutable=True, legacy_literal=True)
    # Dict literal (legacy mutable): Dictionary contains key: value, key: value
    if re.match(r"(?i)^dictionary\s+contains\b", s):
        tail = re.sub(r"(?i)^dictionary\s+contains\b\s*", "", s)
        pairs = _split_top_level(tail)
        kvs: list[tuple] = []
        for p in pairs:
            if ":" not in p:
                raise ParseError("dictionary entry must be 'key: value'", ln)
            k, v = p.split(":", 1)
            kvs.append((_parse_expr(k.strip(), ln), _parse_expr(v.strip(), ln)))
        return DictLiteralExpr(kvs, mutable=True, legacy_literal=True)
    # keys/values of
    if re.match(r"(?i)^keys\s+of\s+", s):
        tail = re.sub(r"(?i)^keys\s+of\s+", "", s)
        return KeysOfExpr(_parse_expr(tail.strip(), ln))
    if re.match(r"(?i)^values\s+of\s+", s):
        tail = re.sub(r"(?i)^values\s+of\s+", "", s)
        return ValuesOfExpr(_parse_expr(tail.strip(), ln))

    # Arithmetic phrase normalization
    s = re.sub(r"(?i)\bdivided by\b", " / ", s)
    s = re.sub(r"(?i)\btimes\b", " * ", s)
    s = re.sub(r"(?i)\bplus\b", " + ", s)
    s = re.sub(r"(?i)\bminus\b", " - ", s)
    return _parse_add_sub(s, ln)


# Pratt-style precedence --------------------------------------------------

def _parse_add_sub(src: str, ln: int):
    tokens = _tokenize(src, ln)
    expr, rest = _parse_mul_div(tokens, ln)
    while rest and rest[0][0] in ('+', '-'):
        op = rest[0][0]
        rhs, rest = _parse_mul_div(rest[1:], ln)
        expr = BinaryExpr(expr, op, rhs, line=ln)
    return expr


def _parse_mul_div(tokens, ln: int):
    expr, rest = _parse_unary(tokens, ln)
    while rest and rest[0][0] in ('*', '/'):
        op = rest[0][0]
        rhs, rest = _parse_unary(rest[1:], ln)
        expr = BinaryExpr(expr, op, rhs, line=ln)
    return expr, rest


def _parse_unary(tokens, ln: int):
    if tokens and tokens[0][0] in ('+', '-', '!'):
        op = tokens[0][0]
        expr, rest = _parse_primary(tokens[1:], ln)
        return UnaryExpr(op, expr, line=ln), rest
    return _parse_primary(tokens, ln)


def _parse_primary(tokens, ln: int):
    if not tokens:
        raise ParseError("expected expression", ln)
    kind, val, col = tokens[0]
    if kind == 'NUMBER':
        if '.' in val:
            return LiteralExpr(float(val), line=ln, col=col), tokens[1:]
        return LiteralExpr(int(val), line=ln, col=col), tokens[1:]
    if kind == 'STRING':
        return LiteralExpr(_unescape(val[1:-1]), line=ln, col=col), tokens[1:]
    if kind == 'IDENT':
        # possible call
        if len(tokens) > 1 and tokens[1][0] == '(':
            args: List = []
            rest = tokens[2:]
            if rest and rest[0][0] == ')':
                return CallExpr(val, [], line=ln, col=col), rest[1:]
            while True:
                arg, rest = _parse_add_sub_tokens(rest, ln)
                args.append(arg)
                if not rest:
                    raise ParseError("expected ')' in call", ln)
                if rest[0][0] == ')':
                    rest = rest[1:]
                    expr: object = CallExpr(val, args, line=ln, col=col)
                    break
                if rest[0][0] != ',':
                    raise ParseError("expected ',' between args", ln)
                rest = rest[1:]
        else:
            expr = IdentifierExpr(val, line=ln, col=col)
            rest = tokens[1:]
        # postfix 'at'
        while rest and rest[0][0] == 'IDENT' and rest[0][1].lower() == 'at':
            # Restrict key to a primary expression (identifier, string, number, grouped) to
            # avoid unintended parsing like d at "a" + d at "b" turning into key 'a' + (...)
            key_expr, rest2 = _parse_at_key(rest[1:], ln)
            expr = AtExpr(expr, key_expr, line=ln, col=col)
            rest = rest2
        return expr, rest
    if kind == '(':
        expr, rest = _parse_add_sub_tokens(tokens[1:], ln)
        if not rest or rest[0][0] != ')':
            raise ParseError("expected ')' to close group", ln)
        rest = rest[1:]
        while rest and rest[0][0] == 'IDENT' and rest[0][1].lower() == 'at':
            key_expr, rest2 = _parse_at_key(rest[1:], ln)
            expr = AtExpr(expr, key_expr, line=ln, col=col)
            rest = rest2
        return expr, rest
    return IdentifierExpr(val, line=ln, col=col), tokens[1:]


def _parse_add_sub_tokens(tokens, ln: int):
    expr, rest = _parse_mul_div(tokens, ln)
    while rest and rest[0][0] in ('+', '-'):
        op = rest[0][0]
        rhs, rest = _parse_mul_div(rest[1:], ln)
        expr = BinaryExpr(expr, op, rhs, line=ln)
    return expr, rest


def _parse_at_key(tokens, ln: int):
    """Parse a restricted key expression for 'at' postfix: only primary without further + or - chaining.
    Allows grouped additive inside parentheses if user wants complex key.
    """
    if not tokens:
        raise ParseError("expected key after 'at'", ln)
    kind, val, col = tokens[0]
    if kind == 'STRING':
        return LiteralExpr(_unescape(val[1:-1]), line=ln, col=col), tokens[1:]
    if kind == 'NUMBER':
        if '.' in val:
            return LiteralExpr(float(val), line=ln, col=col), tokens[1:]
        return LiteralExpr(int(val), line=ln, col=col), tokens[1:]
    if kind == 'IDENT':
        return IdentifierExpr(val, line=ln, col=col), tokens[1:]
    if kind == '(':
        # full expression inside parentheses
        expr, rest = _parse_add_sub_tokens(tokens[1:], ln)
        if not rest or rest[0][0] != ')':
            raise ParseError("expected ')' to close key group", ln)
        return expr, rest[1:]
    raise ParseError("invalid key after 'at'", ln)


def _parse_logic_expr(src: str, ln: int):
    tokens = _tokenize(src, ln)

    def parse_and(rest):
        left, rest = _parse_compare(rest, ln)
        while rest and rest[0][0] == '&&':
            right, rest = _parse_compare(rest[1:], ln)
            left = BinaryExpr(left, '&&', right, line=ln)
        return left, rest

    def parse_or(rest):
        left, rest = parse_and(rest)
        while rest and rest[0][0] == '||':
            right, rest = parse_and(rest[1:])
            left = BinaryExpr(left, '||', right, line=ln)
        return left, rest

    expr, rest = parse_or(tokens)
    return expr


def _parse_compare(tokens, ln: int):
    left, rest = _parse_add_sub_tokens(tokens, ln)
    if rest and rest[0][0] in ('==', '!=', '>=', '<=', '>', '<'):
        op = rest[0][0]
        right, rest = _parse_add_sub_tokens(rest[1:], ln)
        return BinaryExpr(left, op, right, line=ln), rest
    return left, rest


# Tokenizer ---------------------------------------------------------------

def _tokenize(src: str, line: int) -> List[Tuple[str, str, int]]:
    spec = r"""
        (?P<SPACE>\s+)
      | (?P<NUMBER>\d+(?:\.\d+)?)
      | (?P<STRING>"([^"\\]|\\.)*")
      | (?P<OP>==|!=|>=|<=|&&|\|\||\+|\-|\*|/|\(|\)|,|>|<|!)
      | (?P<IDENT>[A-Za-z_][A-Za-z0-9_]*)
    """
    tokens: List[Tuple[str, str, int]] = []
    for m in re.finditer(spec, src, flags=re.VERBOSE):
        kind = m.lastgroup
        val = m.group()
        if kind == 'SPACE':
            continue
        if kind == 'OP':
            tokens.append((val, val, m.start() + 1))  # 1-based column
        else:
            tokens.append((kind, val, m.start() + 1))
    return tokens


# Utilities ---------------------------------------------------------------

def _split_top_level(s: str) -> list[str]:
    items: list[str] = []
    buf: list[str] = []
    in_str = False
    depth = 0
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == '"':
            in_str = not in_str
            buf.append(ch)
        elif ch == '(' and not in_str:
            depth += 1
            buf.append(ch)
        elif ch == ')' and not in_str and depth > 0:
            depth -= 1
            buf.append(ch)
        elif ch == ',' and not in_str and depth == 0:
            items.append(''.join(buf).strip())
            buf = []
        else:
            buf.append(ch)
        i += 1
    if buf:
        items.append(''.join(buf).strip())
    return items


def _strip_comment(line: str) -> str:
    out = []
    in_str = False
    for ch in line:
        if ch == '"':
            in_str = not in_str
            out.append(ch)
        elif ch == '#' and not in_str:
            break
        else:
            out.append(ch)
    return ''.join(out)


def _unescape(s: str) -> str:
    return s.replace('\\"', '"').replace('\\n', '\n')
