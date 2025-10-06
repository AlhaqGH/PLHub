from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List, Optional


# Program
@dataclass
class Program:
    statements: List["Stmt"]


# Statements
class Stmt: ...


@dataclass
class WriteStmt(Stmt):
    expr: "Expr"
    line: int
    col: int = 1


@dataclass
class AskStmt(Stmt):
    name: str
    kind: str  # "text" | "number" | "decimal"
    line: int
    col: int = 1


@dataclass
class SetStmt(Stmt):
    name: str
    expr: "Expr"
    line: int
    col: int = 1


@dataclass
class IncStmt(Stmt):
    name: str
    amount: "Expr"
    line: int
    col: int = 1


@dataclass
class DecStmt(Stmt):
    name: str
    amount: "Expr"
    line: int
    col: int = 1


@dataclass
class IfStmt(Stmt):
    condition: "Expr"
    then_body: List[Stmt]
    else_body: Optional[List[Stmt]]
    line: int
    col: int = 1


@dataclass
class WhileStmt(Stmt):
    condition: "Expr"
    body: List[Stmt]
    line: int
    col: int = 1


@dataclass
class RepeatStmt(Stmt):
    count: "Expr"
    body: List[Stmt]
    line: int
    col: int = 1


@dataclass
class BlockStmt(Stmt):
    body: List[Stmt]
    line: int
    col: int = 1


@dataclass
class FunctionDefStmt(Stmt):
    name: str
    params: List[str]
    defaults: List[Optional["Expr"]]  # aligned with params; None if no default
    body: List[Stmt]
    line: int
    col: int = 1


@dataclass
class ReturnStmt(Stmt):
    value: Optional["Expr"]
    line: int
    col: int = 1


@dataclass
class UseStmt(Stmt):
    name: str
    args: List["Expr"]
    line: int
    col: int = 1


@dataclass
class ImportStmt(Stmt):
    path: str
    line: int
    col: int = 1
    system: bool = False  # Import system "name"


# Expressions
class Expr: ...


@dataclass
class LiteralExpr(Expr):
    value: Any
    line: int = 0
    col: int = 0


@dataclass
class IdentifierExpr(Expr):
    name: str
    line: int = 0
    col: int = 0


@dataclass
class BinaryExpr(Expr):
    left: Expr
    op: str
    right: Expr
    line: int = 0
    col: int = 0


@dataclass
class UnaryExpr(Expr):
    op: str
    expr: Expr
    line: int = 0
    col: int = 0


@dataclass
class CallExpr(Expr):
    name: str
    args: List[Expr]
    line: int = 0
    col: int = 0


@dataclass
class CallValueStmt(Stmt):
    callee: Expr  # expression that should evaluate to a function value
    args: List[Expr]
    line: int
    col: int = 1


@dataclass
class PredicateExpr(Expr):
    name: str  # 'even' | 'odd' | 'positive' | 'negative'
    value: Expr
    line: int = 0
    col: int = 0


@dataclass
class StopStmt(Stmt):
    line: int
    col: int = 1


@dataclass
class SkipStmt(Stmt):
    line: int
    col: int = 1


# Collections

@dataclass
class ListLiteralExpr(Expr):
    items: list[Expr]
    mutable: bool = False
    legacy_literal: bool = False  # True when created via legacy 'List contains ...'
    line: int = 0
    col: int = 0


@dataclass
class DictLiteralExpr(Expr):
    items: list[tuple[Expr, Expr]]  # key, value (allow Expr keys for flexibility)
    mutable: bool = False
    legacy_literal: bool = False  # True when created via legacy 'Dictionary contains ...'
    line: int = 0
    col: int = 0


@dataclass
class AtExpr(Expr):
    container: Expr
    key: Expr  # index or dict key
    line: int = 0
    col: int = 0


@dataclass
class KeysOfExpr(Expr):
    container: Expr
    line: int = 0
    col: int = 0


@dataclass
class ValuesOfExpr(Expr):
    container: Expr
    line: int = 0
    col: int = 0


@dataclass
class AddToListStmt(Stmt):
    value: Expr
    target: Expr
    line: int
    col: int = 1


@dataclass
class RemoveFromListStmt(Stmt):
    value: Expr
    target: Expr
    line: int
    col: int = 1


@dataclass
class AddToDictStmt(Stmt):
    key: Expr
    value: Expr
    target: Expr
    line: int
    col: int = 1


@dataclass
class RemoveFromDictStmt(Stmt):
    key: Expr
    target: Expr
    line: int
    col: int = 1

@dataclass
class DebugStmt(Stmt):
    enabled: bool
    line: int
    col: int = 1

# Phrasal list/dict extended forms

@dataclass
class NthItemExpr(Expr):
    index: Expr  # 1-based index expression
    container: Expr
    line: int = 0
    col: int = 0

@dataclass
class SetNthItemStmt(Stmt):
    index: Expr  # 1-based
    container: Expr
    value: Expr
    line: int
    col: int = 1

@dataclass
class RemoveLastItemStmt(Stmt):
    container: Expr
    line: int
    col: int = 1

# Random / Collection predicates

@dataclass
class RandomIntBetweenExpr(Expr):
    low: Expr
    high: Expr
    line: int = 0
    col: int = 0


@dataclass
class RandomFloatBetweenExpr(Expr):
    low: Expr
    high: Expr
    line: int = 0
    col: int = 0


@dataclass
class RandomFromExpr(Expr):
    collection: Expr
    line: int = 0
    col: int = 0


@dataclass
class ContainsExpr(Expr):
    collection: Expr
    needle: Expr
    line: int = 0
    col: int = 0


@dataclass
class AllPredicateExpr(Expr):
    collection: Expr
    predicate: str  # 'even' | 'odd' | 'positive' | 'negative'
    line: int = 0
    col: int = 0


@dataclass
class AnyPredicateExpr(Expr):
    collection: Expr
    predicate: str  # 'even' | 'odd' | 'positive' | 'negative'
    line: int = 0
    col: int = 0
