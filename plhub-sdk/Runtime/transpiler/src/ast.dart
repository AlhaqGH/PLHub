// AST definitions for PohLang v0.1

sealed class Node {}

class Program extends Node {
  final List<Node> statements;
  Program(this.statements);
}

sealed class Statement extends Node {}

sealed class Expression extends Node {}

// Statements
class PrintStmt extends Statement {
  final Expression expression;
  PrintStmt(this.expression);
}

class InputStmt extends Statement {
  final String name;
  InputStmt(this.name);
}

class InputNumberStmt extends Statement {
  final String name;
  InputNumberStmt(this.name);
}

class InputDecimalStmt extends Statement {
  final String name;
  InputDecimalStmt(this.name);
}

class AssignStmt extends Statement {
  final String name;
  final Expression value;
  AssignStmt(this.name, this.value);
}

class IfStmt extends Statement {
  final Expression condition;
  final List<Statement> thenBranch;
  final List<Statement>? elseBranch;
  IfStmt(this.condition, this.thenBranch, [this.elseBranch]);
}

class RepeatStmt extends Statement {
  final Expression count;
  final List<Statement> body;
  RepeatStmt(this.count, this.body);
}

class WhileStmt extends Statement {
  final Expression condition;
  final List<Statement> body;
  WhileStmt(this.condition, this.body);
}

class FunctionDefStmt extends Statement {
  final String name;
  final List<String> params;
  final List<Statement> body; // last ReturnStmt optional
  FunctionDefStmt(this.name, this.params, this.body);
}

class ReturnStmt extends Statement {
  final Expression? value;
  ReturnStmt([this.value]);
}

class CallStmt extends Statement {
  final String name;
  final List<Expression> args;
  CallStmt(this.name, this.args);
}

class ImportStmt extends Statement {
  final String path; // as provided in source (usually relative)
  ImportStmt(this.path);
}

// System/OS operations (phrase-based)
class OpenFileStmt extends Statement {
  final Expression path;
  OpenFileStmt(this.path);
}

class WriteFileStmt extends Statement {
  final Expression path;
  final Expression content;
  final bool append;
  WriteFileStmt(this.path, this.content, {this.append = false});
}

class DeleteFileStmt extends Statement {
  final Expression path;
  DeleteFileStmt(this.path);
}

class ListFilesStmt extends Statement {
  final Expression directory;
  ListFilesStmt(this.directory);
}

class ChangeDirectoryStmt extends Statement {
  final Expression path;
  ChangeDirectoryStmt(this.path);
}

class CreateDirectoryStmt extends Statement {
  final Expression path;
  CreateDirectoryStmt(this.path);
}

class DeleteDirectoryStmt extends Statement {
  final Expression path;
  DeleteDirectoryStmt(this.path);
}

class RunProgramStmt extends Statement {
  final Expression command;
  // mode: 'plain' | 'wait' | 'background'
  final String mode;
  RunProgramStmt(this.command, {this.mode = 'plain'});
}

// Loop control
class StopStmt extends Statement {} // break

class SkipStmt extends Statement {} // continue

// Collection mutation statements
class AddToListStmt extends Statement {
  final String targetName; // identifier to mutate
  final Expression value;
  AddToListStmt(this.targetName, this.value);
}

class AddToMapStmt extends Statement {
  final String targetName; // identifier to mutate
  final Expression key;
  final Expression value;
  AddToMapStmt(this.targetName, this.key, this.value);
}

class RemoveFromListStmt extends Statement {
  final String targetName; // identifier to mutate
  final Expression value; // value to remove
  RemoveFromListStmt(this.targetName, this.value);
}

class RemoveFromMapStmt extends Statement {
  final String targetName; // identifier to mutate
  final Expression key; // key to remove
  RemoveFromMapStmt(this.targetName, this.key);
}

// Expressions
class BinaryExpr extends Expression {
  final String op;
  final Expression left;
  final Expression right;
  BinaryExpr(this.op, this.left, this.right);
}

class UnaryExpr extends Expression {
  final String op; // e.g., '!'
  final Expression expr;
  UnaryExpr(this.op, this.expr);
}

class LiteralExpr extends Expression {
  final Object? value;
  LiteralExpr(this.value);
}

class IdentifierExpr extends Expression {
  final String name;
  IdentifierExpr(this.name);
}

class CallExpr extends Expression {
  final String name;
  final List<Expression> args;
  CallExpr(this.name, this.args);
}

// Utility for pretty printing (optional future)

// Collection expressions
class ListLiteralExpr extends Expression {
  final List<Expression> items;
  final bool isMutable; // explicit mutable opt-in
  final bool isLegacy; // legacy literal (List contains ...)
  ListLiteralExpr(this.items, {this.isMutable = false, this.isLegacy = false});
}

class MapLiteralExpr extends Expression {
  final List<Expression> keys;
  final List<Expression> values;
  final bool isMutable; // explicit mutable opt-in
  final bool isLegacy; // legacy literal (Dictionary contains ...)
  MapLiteralExpr(this.keys, this.values,
      {this.isMutable = false, this.isLegacy = false});
}

class IndexExpr extends Expression {
  final Expression container;
  final Expression index;
  IndexExpr(this.container, this.index);
}

class KeysOfExpr extends Expression {
  final Expression mapExpr;
  KeysOfExpr(this.mapExpr);
}

class ValuesOfExpr extends Expression {
  final Expression mapExpr;
  ValuesOfExpr(this.mapExpr);
}
