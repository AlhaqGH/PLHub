import 'dart:io';
import 'dart:isolate';
import 'ast.dart';
import 'parser.dart';
import 'package:path/path.dart' as p;

void main(List<String> args) async {
  // Simple arg parser: file.poh [--no-run] [-o output.dart]
  if (args.isEmpty) {
    stderr.writeln(
        'Usage: dart run src/transpiler.dart <file.poh> [--no-run] [--compile] [--strict-phrases] [-o <output.dart>]');
    exit(64);
  }
  final inputPath = args[0];
  bool run = true;
  bool compile = false;
  bool strictPhrasal = false;
  String? outPath;
  for (int i = 1; i < args.length; i++) {
    final a = args[i];
    if (a == '--no-run') {
      run = false;
    } else if (a == '--compile') {
      compile = true;
    } else if (a == '--strict-phrases') {
      strictPhrasal = true;
    } else if (a == '-o' && i + 1 < args.length) {
      outPath = args[++i];
    }
  }
  try {
    final generated = await transpileFile(inputPath,
        outputPath: outPath,
        run: run,
        compile: compile,
        strictPhrasal: strictPhrasal);
    if (!run) {
      stdout.writeln('Generated: $generated');
    }
  } catch (e) {
    stderr.writeln('$e');
    exit(65);
  }
}

/// Transpile a .poh file to Dart and optionally run it.
/// Returns the generated Dart file path.
Future<String> transpileFile(String inputPath,
    {String? outputPath,
    bool run = true,
    bool compile = false,
    bool strictPhrasal = false}) async {
  final file = File(inputPath);
  if (!await file.exists()) {
    throw FormatException('File not found: $inputPath');
  }
  final lines = await file.readAsLines();
  if (strictPhrasal) {
    _warnSymbolOperators(lines, inputPath);
  }
  final parser = Parser(lines);
  late ParseResult result;
  try {
    result = parser.parse();
  } catch (e) {
    throw FormatException('Parse error: $e');
  }
  // Determine output path
  final inputAbs = p.normalize(p.absolute(inputPath));
  final inputDir = p.dirname(inputAbs);
  final inputBase = p.basenameWithoutExtension(inputAbs);
  final outPath = p
      .normalize(p.absolute(outputPath ?? p.join(inputDir, '$inputBase.dart')));
  final dartCode = await _emitDart(result.program, outPath);
  await File(outPath).writeAsString(dartCode);
  stdout.writeln('Generated: $outPath');
  if (compile) {
    // Compile to native executable next to the Dart file
    final outDir = p.dirname(outPath);
    final exeBase = p.basenameWithoutExtension(outPath);
    final exePath = p.normalize(
        p.join(outDir, Platform.isWindows ? '$exeBase.exe' : exeBase));
    try {
      final proc = await Process.start(
          'dart', ['compile', 'exe', outPath, '-o', exePath],
          mode: ProcessStartMode.inheritStdio);
      final code = await proc.exitCode;
      if (code != 0) {
        throw ProcessException(
            'dart',
            ['compile', 'exe', outPath, '-o', exePath],
            'Exited with $code',
            code);
      }
      stdout.writeln('Compiled: $exePath');
      if (!run) return exePath;
      // Run compiled binary
      final runProc =
          await Process.start(exePath, [], mode: ProcessStartMode.inheritStdio);
      final runCode = await runProc.exitCode;
      if (runCode != 0) {
        throw ProcessException(
            exePath, const [], 'Exited with $runCode', runCode);
      }
      return exePath;
    } catch (e) {
      throw FormatException('Failed to compile/run native executable: $e');
    }
  }
  if (!run) return outPath;
  // Auto-run the generated program (Dart VM)
  try {
    final proc = await Process.start('dart', ['run', outPath],
        mode: ProcessStartMode.inheritStdio);
    final code = await proc.exitCode;
    if (code != 0) {
      throw ProcessException(
          'dart', ['run', outPath], 'Exited with $code', code);
    }
  } catch (e) {
    throw FormatException('Failed to run generated program: $e');
  }
  return outPath;
}

Future<String> _emitDart(Program program, String outPath) async {
  final b = StringBuffer();
  b.writeln("import 'dart:io';");
  // Resolve the runtime via package config; if found embed its concrete file: URI.
  final pkgUri = await Isolate.resolvePackageUri(Uri.parse('package:pohlang/runtime.dart'));
  if (pkgUri != null) {
    b.writeln("import '${pkgUri.toString()}';");
  } else {
    // Fallback: relative path to lib/runtime.dart (development / local runs outside package context)
    final outDir = p.normalize(p.dirname(p.absolute(outPath)));
    final runtimeAbs = p.normalize(p.join(Directory.current.path, 'lib', 'runtime.dart'));
    final rel = p.relative(runtimeAbs, from: outDir).replaceAll('\\', '/');
    b.writeln("import '$rel';");
  }
  // Expand imports before emission
  final expanded = await _expandImports(program, outPath);

  // Emit functions (from Make) before main
  final funcDefs = <FunctionDefStmt>[];
  for (final node in expanded.statements) {
    if (node is FunctionDefStmt) funcDefs.add(node);
  }
  for (final f in funcDefs) {
    b.writeln(_emitFunctionFull(f));
  }
  b.writeln('Future<void> main() async {');
  final declared = <String>{};
  for (final node in expanded.statements) {
    final stmt = node as Statement;
    if (stmt is FunctionDefStmt) continue; // already emitted above
    final code = _emitStmt(stmt, declared);
    if (code.isNotEmpty) b.writeln(code);
  }
  b.writeln('}');
  return b.toString();
}

Future<Program> _expandImports(Program program, String outPath) async {
  final seen = <String>{};
  Future<List<Node>> expandList(List<Node> nodes, String baseDir) async {
    final out = <Node>[];
    for (final n in nodes) {
      if (n is ImportStmt) {
        final raw = n.path;
        final candidate = p.normalize(p.join(baseDir, raw));
        if (seen.contains(candidate)) continue; // avoid cycles / duplicates
        seen.add(candidate);
        final f = File(candidate);
        if (!await f.exists()) {
          throw FormatException('Import not found: $raw');
        }
        final lines = await f.readAsLines();
        final parsed = Parser(lines).parse();
        final inner =
            await expandList(parsed.program.statements, p.dirname(candidate));
        out.addAll(inner);
      } else {
        out.add(n);
      }
    }
    return out;
  }

  final baseDir = p.dirname(p.absolute(outPath));
  final expanded = await expandList(program.statements, baseDir);
  return Program(expanded);
}

String _emitStmt(Statement s, Set<String> declared) {
  if (s is PrintStmt) {
    return '  print(${_emitExpr(s.expression)});';
  } else if (s is InputStmt) {
    final name = s.name;
    final decl = declared.contains(name) ? '' : 'var ';
    declared.add(name);
    return "  ${decl}${name} = PohRuntime.inputText('$name');";
  } else if (s is InputNumberStmt) {
    final name = s.name;
    final decl = declared.contains(name) ? '' : 'var ';
    declared.add(name);
    // Default to 0 when user input cannot be parsed to int.
    return "  ${decl}${name} = (PohRuntime.inputInt('$name') ?? 0);";
  } else if (s is InputDecimalStmt) {
    final name = s.name;
    final decl = declared.contains(name) ? '' : 'var ';
    declared.add(name);
    // Default to 0.0 when user input cannot be parsed to double.
    return "  ${decl}${name} = (PohRuntime.inputDouble('$name') ?? 0.0);";
  } else if (s is AssignStmt) {
    final decl = declared.contains(s.name) ? '' : 'var ';
    declared.add(s.name);
    return '  ${decl}${s.name} = ${_emitExpr(s.value)};';
  } else if (s is IfStmt) {
    final thenCode =
        s.thenBranch.map((Statement st) => _emitStmt(st, declared)).join('\n');
    final elseCode = (s.elseBranch != null)
        ? s.elseBranch!
            .map((Statement st) => _emitStmt(st, declared))
            .join('\n')
        : null;
    return '  if (${_emitExpr(s.condition)}) {\n$thenCode\n  }' +
        (elseCode != null ? ' else {\n$elseCode\n  }' : '');
  } else if (s is RepeatStmt) {
    final body =
        s.body.map((Statement st) => _emitStmt(st, declared)).join('\n');
    final countExpr = _emitExpr(s.count);
    final loopVar = '_i';
    return '  for (var $loopVar = 0; $loopVar < $countExpr; $loopVar++) {\n$body\n  }';
  } else if (s is WhileStmt) {
    final cond = _emitExpr(s.condition);
    final body =
        s.body.map((Statement st) => _emitStmt(st, declared)).join('\n');
    return '  while ($cond) {\n$body\n  }';
  } else if (s is StopStmt) {
    return '  break;';
  } else if (s is SkipStmt) {
    return '  continue;';
  } else if (s is FunctionDefStmt) {
    return '';
  } else if (s is CallStmt) {
    final args = s.args.map(_emitExpr).join(', ');
    return '  ${s.name}($args);';
  } else if (s is OpenFileStmt) {
    // Reads into a conventional variable name: fileContent
    const varName = 'fileContent';
    final decl = declared.contains(varName) ? '' : 'var ';
    declared.add(varName);
    return "  ${decl}${varName} = PohRuntime.readFile(${_emitExpr(s.path)});";
  } else if (s is WriteFileStmt) {
    final append = s.append ? 'true' : 'false';
    return "  PohRuntime.writeFile(${_emitExpr(s.path)}, ${_emitExpr(s.content)}, append: $append);";
  } else if (s is DeleteFileStmt) {
    return "  PohRuntime.deleteFile(${_emitExpr(s.path)});";
  } else if (s is ListFilesStmt) {
    const varName = 'fileList';
    final decl = declared.contains(varName) ? '' : 'var ';
    declared.add(varName);
    return "  ${decl}${varName} = PohRuntime.listFiles(${_emitExpr(s.directory)});";
  } else if (s is ChangeDirectoryStmt) {
    return "  PohRuntime.changeDirectory(${_emitExpr(s.path)});";
  } else if (s is CreateDirectoryStmt) {
    return "  PohRuntime.createDirectory(${_emitExpr(s.path)});";
  } else if (s is DeleteDirectoryStmt) {
    return "  PohRuntime.deleteDirectory(${_emitExpr(s.path)});";
  } else if (s is RunProgramStmt) {
    if (s.mode == 'wait') {
      return "  await PohRuntime.runProgramWait(${_emitExpr(s.command)});";
    } else if (s.mode == 'background') {
      return "  PohRuntime.runProgramBackground(${_emitExpr(s.command)});";
    } else {
      // plain: fire and forget without waiting
      return "  PohRuntime.runProgramBackground(${_emitExpr(s.command)});";
    }
  } else if (s is ReturnStmt) {
    return '  return ${s.value != null ? _emitExpr(s.value!) : ''};';
  } else if (s is AddToListStmt) {
    // Enforce immutability by default; only allow if target is a PohList (mutable)
    return '  PohRuntime.listAdd(${s.targetName}, ${_emitExpr(s.value)});';
  } else if (s is AddToMapStmt) {
    return '  PohRuntime.mapAdd(${s.targetName}, ${_emitExpr(s.key)}, ${_emitExpr(s.value)});';
  } else if (s is RemoveFromListStmt) {
    return '  PohRuntime.collectionRemove(${s.targetName}, ${_emitExpr(s.value)});';
  } else if (s is RemoveFromMapStmt) {
    return '  PohRuntime.collectionRemove(${s.targetName}, ${_emitExpr(s.key)});';
  }
  return '  // Unhandled statement ${s.runtimeType}';
}

String _emitFunctionFull(FunctionDefStmt f) {
  final params = f.params.join(', ');
  final sb = StringBuffer();
  sb.writeln('dynamic ${f.name}($params) {');
  // Emit body statements; function-level declarations are local
  final declared = <String>{};
  for (final st in f.body) {
    if (st is ReturnStmt) {
      final expr = st.value != null ? _emitExpr(st.value!) : '';
      sb.writeln('  return $expr;');
    } else {
      final code = _emitStmt(st, declared);
      if (code.isNotEmpty) sb.writeln(code);
    }
  }
  // Ensure implicit return null if none provided
  sb.writeln('  return null;');
  sb.writeln('}');
  return sb.toString();
}

String _emitExpr(Expression e) {
  if (e is LiteralExpr) {
    if (e.value is String) {
      return '"${e.value}"';
    }
    if (e.value == null) return 'null';
    return e.value.toString();
  } else if (e is IdentifierExpr) {
    return e.name;
  } else if (e is BinaryExpr) {
    // If '+' is used and any side is or contains a string literal, coerce both to String
    if (e.op == '+') {
      final leftHasStr = _containsStringLiteral(e.left);
      final rightHasStr = _containsStringLiteral(e.right);
      if (leftHasStr || rightHasStr) {
        return '(${_emitForConcat(e.left)} + ${_emitForConcat(e.right)})';
      }
    }
    return '(${_emitExpr(e.left)} ${e.op} ${_emitExpr(e.right)})';
  } else if (e is UnaryExpr) {
    return '(${e.op}${_emitExpr(e.expr)})';
  } else if (e is CallExpr) {
    final args = e.args.map(_emitExpr).join(', ');
    return '${e.name}($args)';
  } else if (e is ListLiteralExpr) {
    final items = e.items.map(_emitExpr).join(', ');
    final mut = e.isMutable ? 'true' : 'false';
    final legacy = e.isLegacy ? 'true' : 'false';
    return 'PohRuntime.listLiteral([$items], mutable: $mut, legacy: $legacy)';
  } else if (e is MapLiteralExpr) {
    final entries = <String>[];
    for (var i = 0; i < e.keys.length; i++) {
      entries.add('${_emitExpr(e.keys[i])}: ${_emitExpr(e.values[i])}');
    }
    final mut = e.isMutable ? 'true' : 'false';
    final legacy = e.isLegacy ? 'true' : 'false';
    return 'PohRuntime.mapLiteral({${entries.join(', ')}}, mutable: $mut, legacy: $legacy)';
  } else if (e is IndexExpr) {
    return 'PohRuntime.indexAt(${_emitExpr(e.container)}, ${_emitExpr(e.index)})';
  } else if (e is KeysOfExpr) {
    return 'PohRuntime.keysOf(${_emitExpr(e.mapExpr)})';
  } else if (e is ValuesOfExpr) {
    return 'PohRuntime.valuesOf(${_emitExpr(e.mapExpr)})';
  }
  return '/*expr*/';
}

// Detect whether an expression subtree contains any string literal.
bool _containsStringLiteral(Expression e) {
  if (e is LiteralExpr) return e.value is String;
  if (e is BinaryExpr)
    return _containsStringLiteral(e.left) || _containsStringLiteral(e.right);
  return false;
}

// Emit an expression ensured to be a String for concatenation context.
String _emitForConcat(Expression e) {
  if (e is LiteralExpr && e.value is String) {
    return '"${e.value}"';
  }
  // For everything else, rely on toString to avoid type errors.
  return '(${_emitExpr(e)}).toString()';
}

void _warnSymbolOperators(List<String> lines, String path) {
  final warnings = collectStrictPhrasalWarnings(lines, path: path);
  for (final w in warnings) {
    stderr.writeln(w);
  }
}

/// Scan lines and return strict-phrasal warnings (without printing).
/// Rules:
/// - Ignore anything after a '#' comment marker (outside strings)
/// - Ignore symbols inside string literals ("")
/// - Warn once per line if any of + - * / occurs outside strings/comments
List<String> collectStrictPhrasalWarnings(List<String> lines, {String? path}) {
  final warnings = <String>[];
  for (var idx = 0; idx < lines.length; idx++) {
    final raw = lines[idx];
    String line = raw;
    // Strip comments starting with # (outside strings)
    bool inStr = false;
    for (int i = 0; i < line.length; i++) {
      final ch = line[i];
      if (ch == '"') {
        inStr = !inStr;
      } else if (!inStr && ch == '#') {
        line = line.substring(0, i);
        break;
      }
    }
    final trimmed = line.trim();
    if (trimmed.isEmpty) continue;
    // Scan for symbolic + - * / outside strings
    inStr = false;
    for (int i = 0; i < line.length; i++) {
      final ch = line[i];
      if (ch == '"') {
        inStr = !inStr;
        continue;
      }
      if (inStr) continue;
      if (ch == '+' || ch == '-' || ch == '*' || ch == '/') {
        final loc = path != null ? '$path:${idx + 1}' : 'Line ${idx + 1}';
        warnings.add(
            'Strict phrasal: $loc: Avoid symbolic operator "$ch"; use words (plus/minus/times/divided by).');
        break; // once per line
      }
    }
  }
  return warnings;
}
