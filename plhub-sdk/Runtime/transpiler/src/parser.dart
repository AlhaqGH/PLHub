import 'ast.dart';

// Lightweight line-based parser for phrasal PohLang v0.1 (symbol mode removed).

class ParseResult {
  final Program program;
  ParseResult(this.program);
}

class Parser {
  final List<String> lines;
  Parser(this.lines);

  ParseResult parse() {
    // Build filtered lines and keep mapping to original 1-based line numbers
    final filtered = <String>[];
    final lineNumbers = <int>[];
    for (var idx = 0; idx < lines.length; idx++) {
      var raw = lines[idx];
      // Remove inline comments starting with '#'.
      // Note: We don't currently parse strings, so '#' inside strings is not supported.
      final hashIdx = raw.indexOf('#');
      if (hashIdx != -1) raw = raw.substring(0, hashIdx);
      final trimmed = raw.trim();
      if (trimmed.isEmpty) continue;
      if (trimmed == 'Start Program' || trimmed == 'End Program') continue;
      filtered.add(trimmed);
      lineNumbers.add(idx + 1);
    }
    final stmts = <Statement>[];
    var i = 0;
    while (i < filtered.length) {
      final line = filtered[i];
      // Function block: Make name with params ... End
      if (line.startsWith('Make ')) {
        if (line.contains(' Say ')) {
          throw FormatException(
              "In 'Make', use 'Write', not 'Say'. Example: Make f with x Write x + 1");
        }
        final withIdx = line.indexOf(' with ');
        if (withIdx == -1) {
          throw FormatException(
              'Line ${lineNumbers[i]}: Invalid Make syntax. Expected: Make name with a, b');
        }
        final name = line.substring(5, withIdx).trim();
        final paramsStr = line.substring(withIdx + 6).trim();
        // Inline short form if same line contains Write
        final writeIdx = paramsStr.indexOf(' Write ');
        if (writeIdx != -1) {
          final paramsOnly = paramsStr.substring(0, writeIdx).trim();
          final exprStr =
              paramsStr.substring(writeIdx + ' Write '.length).trim();
          final params = paramsOnly.isEmpty
              ? <String>[]
              : paramsOnly.split(',').map((s) => s.trim()).toList();
          final bodyExpr = _parseExpression(exprStr);
          stmts.add(FunctionDefStmt(name, params, [ReturnStmt(bodyExpr)]));
          i++;
          continue;
        }
        final params = paramsStr.isEmpty
            ? <String>[]
            : paramsStr.split(',').map((s) => s.trim()).toList();
        final body = <Statement>[];
        i++;
        while (i < filtered.length &&
            filtered[i] != 'End' &&
            filtered[i] != 'End If') {
          // Allow Return X inside functions
          if (filtered[i].startsWith('Return')) {
            final after = filtered[i].substring('Return'.length).trim();
            if (after.isEmpty) {
              body.add(ReturnStmt());
            } else {
              body.add(ReturnStmt(_parseExpression(after)));
            }
            i++;
            continue;
          }
          try {
            body.add(_parsePhraseLine(filtered[i]));
          } catch (e) {
            throw FormatException('Line ${lineNumbers[i]}: $e');
          }
          i++;
        }
        if (i >= filtered.length ||
            (filtered[i] != 'End' && filtered[i] != 'End If')) {
          final lastLine = i > 0 && i - 1 < lineNumbers.length
              ? lineNumbers[i - 1]
              : lineNumbers.last;
          throw FormatException('Line $lastLine: Make block missing End');
        }
        i++; // consume End
        stmts.add(FunctionDefStmt(name, params, body));
        continue;
      }
      // While blocks (multi-line)
      if (line.startsWith('While ')) {
        if (line.contains(' Say ')) {
          throw FormatException(
              "In 'While', use 'Write', not 'Say'. Example: While cond Write X");
        }
        final inlineIdx = line.indexOf(' Write ', 6);
        if (inlineIdx != -1) {
          // Inline While handled by phrase parser
          try {
            stmts.add(_parsePhraseLine(line));
          } catch (e) {
            throw FormatException('Line ${lineNumbers[i]}: $e');
          }
          i++;
          continue;
        }
        final condStr = line.substring(6).trim();
        final cond = _parseBooleanExpression(condStr);
        final body = <Statement>[];
        i++;
        while (i < filtered.length &&
            filtered[i] != 'End' &&
            filtered[i] != 'End While') {
          try {
            body.add(_parsePhraseLine(filtered[i]));
          } catch (e) {
            throw FormatException('Line ${lineNumbers[i]}: $e');
          }
          i++;
        }
        if (i >= filtered.length ||
            (filtered[i] != 'End' && filtered[i] != 'End While')) {
          final lastLine = i > 0 && i - 1 < lineNumbers.length
              ? lineNumbers[i - 1]
              : lineNumbers.last;
          throw FormatException('Line $lastLine: While block missing End');
        }
        // consume End
        i++;
        stmts.add(WhileStmt(cond, body));
        continue;
      }
      // If blocks (multi-line) or inline If
      if (line.startsWith('If ')) {
        if (line.contains(' Say ')) {
          throw FormatException(
              "In 'If', use 'Write', not 'Say'. Example: If cond Write X Otherwise Write Y");
        }
        final writeIdx = line.indexOf(' Write ', 3);
        if (writeIdx != -1) {
          // Inline form, delegate to phrase parser so it shares the same checks
          try {
            stmts.add(_parsePhraseLine(line));
          } catch (e) {
            throw FormatException('Line ${lineNumbers[i]}: $e');
          }
          i++;
          continue;
        }
        // Block form: If <cond> then lines until End; optional Otherwise section
        final condStr = line.substring(3).trim();
        final cond = _parseBooleanExpression(condStr);
        final thenBody = <Statement>[];
        final elseBody = <Statement>[];
        var inElse = false;
        i++;
        while (i < filtered.length &&
            filtered[i] != 'End' &&
            filtered[i] != 'End If') {
          if (filtered[i] == 'Otherwise') {
            if (inElse) {
              throw FormatException(
                  'Line ${lineNumbers[i]}: Duplicate Otherwise in If block');
            }
            inElse = true;
            i++;
            continue;
          }
          try {
            final stmt = _parsePhraseLine(filtered[i]);
            if (!inElse) {
              thenBody.add(stmt);
            } else {
              elseBody.add(stmt);
            }
          } catch (e) {
            throw FormatException('Line ${lineNumbers[i]}: $e');
          }
          i++;
        }
        if (i >= filtered.length ||
            (filtered[i] != 'End' && filtered[i] != 'End If')) {
          final lastLine = i > 0 && i - 1 < lineNumbers.length
              ? lineNumbers[i - 1]
              : lineNumbers.last;
          throw FormatException('Line $lastLine: If block missing End');
        }
        // consume End
        i++;
        stmts.add(IfStmt(cond, thenBody, inElse ? elseBody : null));
        continue;
      }
      if (line.startsWith('Repeat ')) {
        // Inline: Repeat N [times] Write X
        if (line.contains(' Say ')) {
          throw FormatException(
              'In \'Repeat\', use \'Write\', not \'Say\'. Example: Repeat 3 Write "Hi"');
        }
        int splitIdx = line.indexOf(' Write ');
        var tokenLen = ' Write '.length;
        var countStr = '';
        if (splitIdx != -1) {
          countStr = line.substring(7, splitIdx).trim();
          if (countStr.endsWith(' times')) {
            countStr =
                countStr.substring(0, countStr.length - ' times'.length).trim();
          }
          final bodyExprStr = line.substring(splitIdx + tokenLen).trim();
          try {
            final countExpr = _parseExpression(countStr);
            final bodyExpr = _parseExpression(bodyExprStr);
            stmts.add(RepeatStmt(countExpr, [PrintStmt(bodyExpr)]));
          } catch (e) {
            throw FormatException('Line ${lineNumbers[i]}: $e');
          }
          i++;
          continue;
        }
        // Block: Repeat N [times] ... End
        var header = line.substring(7).trim();
        if (header.endsWith(' times')) {
          header = header.substring(0, header.length - ' times'.length).trim();
        }
        final countExpr = _parseExpression(header);
        final body = <Statement>[];
        i++;
        while (i < filtered.length && filtered[i] != 'End') {
          try {
            body.add(_parsePhraseLine(filtered[i]));
          } catch (e) {
            throw FormatException('Line ${lineNumbers[i]}: $e');
          }
          i++;
        }
        if (i >= filtered.length || filtered[i] != 'End') {
          throw FormatException(
              'Line ${lineNumbers[i - 1]}: Repeat block missing End');
        }
        // consume End
        i++;
        stmts.add(RepeatStmt(countExpr, body));
        continue;
      }
      // default single-line statement
      try {
        stmts.add(_parsePhraseLine(line));
      } catch (e) {
        throw FormatException('Line ${lineNumbers[i]}: $e');
      }
      i++;
    }
    final desugared = _desugar(stmts);
    return ParseResult(Program(desugared));
  }

  Statement _parsePhraseLine(String line) {
    // Fast checks for forbidden synonyms inside the line
    if (line.contains(' Else ')) {
      throw FormatException(
          "Use 'Otherwise' instead of 'Else'. Example: If cond Write X Otherwise Write Y");
    }
    if (line.startsWith('Print ')) {
      throw FormatException(
          'Use \"Write\" instead of \"Print\". Example: Write "Hello"');
    }
    if (line.startsWith('Ask the user for ')) {
      throw FormatException(
          "Use 'Ask for <name>' instead of 'Ask the user for'. Example: Ask for name");
    }
    if (line.startsWith('Sya ') || line == 'Sya') {
      throw FormatException('Did you mean "Write"? Example: Write "Hi"');
    }
    if (line.startsWith('Say ')) {
      throw FormatException(
          'Say is not supported. Use "Write <expression>". Example: Write "Hello"');
    }

    // Misuse: bare '<name> is <expr>' looks like assignment, but 'is' is for comparison.
    // Provide a helpful error.
    final isIdx = line.indexOf(' is ');
    if (isIdx > 0 &&
        !line.startsWith('If ') &&
        !line.startsWith('While ') &&
        !line.startsWith('Repeat ') &&
        !line.startsWith('Make ') &&
        !line.startsWith('Use ') &&
        !line.startsWith('Import ') &&
        !line.startsWith('Write ') &&
        !line.startsWith('Ask for ') &&
        !line.startsWith('Increase ') &&
        !line.startsWith('Decrease ') &&
        !line.startsWith('Set ') &&
        !line.startsWith('Return') &&
        !line.startsWith('Open file ') &&
        !line.startsWith('Write file ') &&
        !line.startsWith('Append file ') &&
        !line.startsWith('Delete file ') &&
        !line.startsWith('List files in ') &&
        !line.startsWith('Change directory to ') &&
        !line.startsWith('Create directory ') &&
        !line.startsWith('Delete directory ') &&
        !line.startsWith('Run program ')) {
      final before = line.substring(0, isIdx).trim();
      if (before.isNotEmpty && _looksLikeIdentifier(before)) {
        throw FormatException(
            "Did you mean: Set $before to <expression>? 'is' is for comparison in conditions.");
      }
    }

    // Write/Print
    if (line.startsWith('Write ') && !line.startsWith('Write file ')) {
      final expr = _parseExpression(line.substring('Write '.length));
      return PrintStmt(expr);
    }

    // Loop control: Stop (break), Skip (continue)
    if (line == 'Stop') return StopStmt();
    if (line == 'Skip') return SkipStmt();

    // Ask for
    if (line.startsWith('Ask for ')) {
      final rest = line.substring(8).trim();
      // Legacy prefix form: "number <name>"
      if (rest.toLowerCase().startsWith('number ')) {
        final name = rest.substring('number '.length).trim();
        return InputNumberStmt(name);
      }
      // Legacy prefix form: "decimal <name>"
      if (rest.toLowerCase().startsWith('decimal ')) {
        final name = rest.substring('decimal '.length).trim();
        return InputDecimalStmt(name);
      }
      // New canonical suffix form: "<name> number" (case-insensitive)
      final lower = rest.toLowerCase();
      if (lower.endsWith(' number')) {
        final name = rest.substring(0, rest.length - ' number'.length).trim();
        return InputNumberStmt(name);
      }
      if (lower.endsWith(' decimal')) {
        final name = rest.substring(0, rest.length - ' decimal'.length).trim();
        return InputDecimalStmt(name);
      }
      return InputStmt(rest);
    }

    // Set
    if (line.startsWith('Set ')) {
      // Supports: Set x to 5  | Set x 5
      final afterSet = line.substring(4).trim();
      final toIdx = afterSet.indexOf(' to ');
      late String name;
      late String valueStr;
      if (toIdx != -1) {
        name = afterSet.substring(0, toIdx).trim();
        valueStr = afterSet.substring(toIdx + 4).trim();
      } else {
        final firstSpace = afterSet.indexOf(' ');
        if (firstSpace == -1)
          throw FormatException('Invalid Set syntax: $line');
        name = afterSet.substring(0, firstSpace);
        valueStr = afterSet.substring(firstSpace + 1).trim();
      }
      return AssignStmt(name, _parseExpression(valueStr));
    }

    // Increase/Decrease (friendly)
    if (line.startsWith('Increase ')) {
      final after = line.substring('Increase '.length).trim();
      final byIdx = after.indexOf(' by ');
      final name = byIdx == -1 ? after : after.substring(0, byIdx).trim();
      final incExpr = byIdx == -1
          ? LiteralExpr(1)
          : _parseExpression(after.substring(byIdx + 4).trim());
      return AssignStmt(name, BinaryExpr('+', IdentifierExpr(name), incExpr));
    }
    if (line.startsWith('Decrease ')) {
      final after = line.substring('Decrease '.length).trim();
      final byIdx = after.indexOf(' by ');
      final name = byIdx == -1 ? after : after.substring(0, byIdx).trim();
      final decExpr = byIdx == -1
          ? LiteralExpr(1)
          : _parseExpression(after.substring(byIdx + 4).trim());
      return AssignStmt(name, BinaryExpr('-', IdentifierExpr(name), decExpr));
    }
    // Old terms with suggestions
    if (line.startsWith('Increment ')) {
      throw FormatException(
          "Use 'Increase <name> by <number>' (make number bigger). Example: Increase x by 1");
    }
    if (line.startsWith('Decrement ')) {
      throw FormatException(
          "Use 'Decrease <name> by <number>' (make number smaller). Example: Decrease x by 1");
    }

    // If (inline only here; block handled in top-level parse loop)
    if (line.startsWith('If ')) {
      if (line.contains(' Say ')) {
        throw FormatException(
            "In 'If', use 'Write', not 'Say'. Example: If cond Write X Otherwise Write Y");
      }
      final writeIdx = line.indexOf(' Write ', 3);
      if (writeIdx != -1) {
        // Inline form: If <cond> Write <expr> [Otherwise Write <expr>]
        // If the line contains 'Otherwise' but not the required 'Otherwise Write', treat as malformed.
        // Handle both cases: ' Otherwise ' (with trailing space) and end-of-line ' Otherwise'.
        final otherwiseIdx =
            line.indexOf(' Otherwise ', writeIdx + ' Write '.length);
        final otherwiseTailIdx =
            line.indexOf(' Otherwise', writeIdx + ' Write '.length);
        final elseIdx =
            line.indexOf(' Otherwise Write ', writeIdx + ' Write '.length);
        if ((otherwiseIdx != -1 || otherwiseTailIdx != -1) && elseIdx == -1) {
          throw FormatException(
              "After 'Otherwise' you must add 'Write <expression>'. Example: If cond Write X Otherwise Write Y");
        }
        if (elseIdx != -1) {
          final condStr = line.substring(3, writeIdx).trim();
          final thenExprStr =
              line.substring(writeIdx + ' Write '.length, elseIdx).trim();
          final elseExprStr =
              line.substring(elseIdx + ' Otherwise Write '.length).trim();
          final cond = _parseBooleanExpression(condStr);
          return IfStmt(cond, [PrintStmt(_parseExpression(thenExprStr))],
              [PrintStmt(_parseExpression(elseExprStr))]);
        } else {
          final condStr = line.substring(3, writeIdx).trim();
          final thenExprStr =
              line.substring(writeIdx + ' Write '.length).trim();
          final cond = _parseBooleanExpression(condStr);
          return IfStmt(cond, [PrintStmt(_parseExpression(thenExprStr))]);
        }
      }
      throw FormatException(
          "Missing 'Write' in If. For blocks, use multi-line form with End. For inline, use: If cond Write X Otherwise Write Y");
    }

    // While (single-line)
    if (line.startsWith('While ')) {
      if (line.contains(' Say ')) {
        throw FormatException(
            "In 'While', use 'Write', not 'Say'. Example: While cond Write X");
      }
      final splitIdx = line.indexOf(' Write ');
      if (splitIdx == -1)
        throw FormatException(
            "Missing 'Write' in While. Example: While cond Write X");
      final condStr = line.substring(6, splitIdx).trim();
      final bodyExprStr = line.substring(splitIdx + ' Write '.length).trim();
      final cond = _parseBooleanExpression(condStr);
      final bodyExpr = _parseExpression(bodyExprStr);
      return WhileStmt(cond, [PrintStmt(bodyExpr)]);
    }

    // Collections: Add/Remove for list and dictionary
    // Add "x" to items  | Add "k": v to ages
    if (line.startsWith('Add ')) {
      final toIdx = line.indexOf(' to ');
      if (toIdx == -1) {
        throw FormatException(
            "Invalid Add syntax. Examples: Add \"x\" to items | Add \"k\": 1 to ages");
      }
      final before = line.substring(4, toIdx).trim();
      final target = line.substring(toIdx + 4).trim();
      // Map form: <key>: <expr>
      final colonIdx = _indexOfTopLevelColon(before);
      if (colonIdx != -1) {
        final keyStr = before.substring(0, colonIdx).trim();
        final valStr = before.substring(colonIdx + 1).trim();
        if (!_looksLikeIdentifier(target)) {
          throw FormatException('Add target must be an identifier (got: $target)');
        }
        return AddToMapStmt(target, _parseExpression(keyStr), _parseExpression(valStr));
      }
      // List form
      if (!_looksLikeIdentifier(target)) {
        throw FormatException('Add target must be an identifier (got: $target)');
      }
      return AddToListStmt(target, _parseExpression(before));
    }
    if (line.startsWith('Remove ')) {
      // Remove "x" from items | Remove "k" from ages
      final fromIdx = line.indexOf(' from ');
      if (fromIdx == -1) {
        throw FormatException(
            "Invalid Remove syntax. Examples: Remove \"x\" from items | Remove \"k\" from ages");
      }
      final itemStr = line.substring(7, fromIdx).trim();
      final target = line.substring(fromIdx + 6).trim();
      if (!_looksLikeIdentifier(target)) {
        throw FormatException('Remove target must be an identifier (got: $target)');
      }
      // Heuristic: quoted string or not doesn't matter; for maps we treat as key removal
      return RemoveFromMapStmt(target, _parseExpression(itemStr));
    }

    // System/OS phrase commands
    if (line.startsWith('Import ')) {
      final rest = line.substring('Import '.length).trim();
      if (!(rest.startsWith('"') && rest.endsWith('"'))) {
        throw FormatException(
            'Import expects a quoted path. Example: Import "lib/util.poh"');
      }
      final path = rest.substring(1, rest.length - 1);
      return ImportStmt(path);
    }
    if (line.startsWith('Open file ')) {
      final pathStr = line.substring('Open file '.length).trim();
      return OpenFileStmt(_parseExpression(pathStr));
    }
    if (line.startsWith('Write file ')) {
      final withIdx = line.indexOf(' with ');
      if (withIdx == -1) {
        throw FormatException(
            'Invalid Write file syntax, expected: Write file "name" with <expr>');
      }
      final pathStr = line.substring('Write file '.length, withIdx).trim();
      final contentStr = line.substring(withIdx + 6).trim();
      return WriteFileStmt(
          _parseExpression(pathStr), _parseExpression(contentStr),
          append: false);
    }
    if (line.startsWith('Append file ')) {
      final withIdx = line.indexOf(' with ');
      if (withIdx == -1) {
        throw FormatException(
            'Invalid Append file syntax, expected: Append file "name" with <expr>');
      }
      final pathStr = line.substring('Append file '.length, withIdx).trim();
      final contentStr = line.substring(withIdx + 6).trim();
      return WriteFileStmt(
          _parseExpression(pathStr), _parseExpression(contentStr),
          append: true);
    }
    if (line.startsWith('Delete file ')) {
      final pathStr = line.substring('Delete file '.length).trim();
      return DeleteFileStmt(_parseExpression(pathStr));
    }
    if (line.startsWith('List files in ')) {
      final dirStr = line.substring('List files in '.length).trim();
      return ListFilesStmt(_parseExpression(dirStr));
    }
    if (line.startsWith('Change directory to ')) {
      final pathStr = line.substring('Change directory to '.length).trim();
      return ChangeDirectoryStmt(_parseExpression(pathStr));
    }
    if (line.startsWith('Create directory ')) {
      final pathStr = line.substring('Create directory '.length).trim();
      return CreateDirectoryStmt(_parseExpression(pathStr));
    }
    if (line.startsWith('Delete directory ')) {
      final pathStr = line.substring('Delete directory '.length).trim();
      return DeleteDirectoryStmt(_parseExpression(pathStr));
    }
    if (line.startsWith('Run program ')) {
      // Run program "cmd" [and wait|in background]
      final base = line.substring('Run program '.length).trim();
      String mode = 'plain';
      String cmdStr = base;
      if (base.endsWith(' and wait')) {
        mode = 'wait';
        cmdStr = base.substring(0, base.length - ' and wait'.length).trim();
      } else if (base.endsWith(' in background')) {
        mode = 'background';
        cmdStr =
            base.substring(0, base.length - ' in background'.length).trim();
      }
      return RunProgramStmt(_parseExpression(cmdStr), mode: mode);
    }

    // Make/Use (functions)
    if (line.startsWith('Make ')) {
      if (line.contains(' Say ')) {
        throw FormatException(
            "In 'Make', use 'Write', not 'Say'. Example: Make f with x Write x + 1");
      }
      final withIndex = line.indexOf(' with ');
      final writeIndex = line.indexOf(' Write ');
      if (withIndex == -1 || writeIndex == -1) {
        throw FormatException(
            "Invalid Make syntax. Example: Make greet with who Write \"Hi \" + who");
      }
      final name = line.substring(5, withIndex).trim();
      final paramsStr = line.substring(withIndex + 6, writeIndex).trim();
      final exprStr = line.substring(writeIndex + ' Write '.length).trim();
      final params = paramsStr.isEmpty
          ? <String>[]
          : paramsStr.split(',').map((s) => s.trim()).toList();
      final bodyExpr = _parseExpression(exprStr);
      return FunctionDefStmt(name, params, [ReturnStmt(bodyExpr)]);
    }
    if (line.startsWith('Use ')) {
      final withIndex = line.indexOf(' with ');
      if (withIndex == -1) {
        final name = line.substring(4).trim();
        return CallStmt(name, []);
      }
      final name = line.substring(4, withIndex).trim();
      final argsStr = line.substring(withIndex + 6).trim();
      final args = argsStr.isEmpty
          ? <Expression>[]
          : argsStr.split(',').map((s) => _parseExpression(s.trim())).toList();
      return CallStmt(name, args);
    }
    // Old function terms with suggestions
    if (line.startsWith('Define ')) {
      throw FormatException(
          "Use 'Make <name> with <params> Write <expr>' (create a function).");
    }
    if (line.startsWith('Call ')) {
      throw FormatException("Use 'Use <name> with <args>' (run a function).");
    }

    throw FormatException('Unknown phrase statement: $line');
  }

  bool _looksLikeIdentifier(String s) {
    final re = RegExp(r'^[A-Za-z][A-Za-z0-9_]*$');
    return re.hasMatch(s);
  }

  List<Statement> _desugar(List<Statement> input) {
    return input; // future expansion
  }

  Expression _parseExpression(String src) {
    src = src.trim();
    // Normalize phrase-based arithmetic operators to symbolic ones
    src = _normalizeArithmetic(src);
    // Collection special forms first
    final listExpr = _tryParseListLiteral(src);
    if (listExpr != null) return listExpr;
    final mapExpr = _tryParseMapLiteral(src);
    if (mapExpr != null) return mapExpr;
    final idxExpr = _tryParseIndexing(src);
    if (idxExpr != null) return idxExpr;
    final keysVals = _tryParseKeysValues(src);
    if (keysVals != null) return keysVals;
    return _parseAddSub(src);
  }

  // Boolean grammar with simple precedence:
  // Or (lowest), And, Not (highest), then comparisons, then +,-,*, primary
  Expression _parseBooleanExpression(String src) {
    var raw = src.trim();
    // Specific hint if user typed '=='
    if (raw.contains('==')) {
      throw FormatException(
          "Use 'is' for equality (and 'is not' for inequality) in conditions.");
    }
    var s = _normalizeComparators(raw);
    s = _normalizeLogic(s);
    // Discourage '=' in conditions by detecting bare single '=' first
    // If found, throw a friendly error suggesting 'is'
    final containsSingleEq = _containsBareEquality(s);
    if (containsSingleEq) {
      throw FormatException(
          "Use phrasal equality in conditions (e.g., 'is', 'is not'). '=' is reserved for assignment.");
    }
    return _parseOr(s);
  }

  Expression _parseOr(String src) {
    // split by ' Or ' at top level
    final parts = _splitTopLevel(src, ' Or ');
    if (parts.length == 1) return _parseAnd(src);
    Expression expr = _parseAnd(parts[0]);
    for (var i = 1; i < parts.length; i++) {
      expr = BinaryExpr('||', expr, _parseAnd(parts[i]));
    }
    return expr;
  }

  Expression _parseAnd(String src) {
    final parts = _splitTopLevel(src, ' And ');
    if (parts.length == 1) return _parseNot(src);
    Expression expr = _parseNot(parts[0]);
    for (var i = 1; i < parts.length; i++) {
      expr = BinaryExpr('&&', expr, _parseNot(parts[i]));
    }
    return expr;
  }

  Expression _parseNot(String src) {
    final trimmed = src.trim();
    if (trimmed.startsWith('Not ')) {
      return UnaryExpr('!', _parseNot(trimmed.substring(4)));
    }
    return _parseComparison(trimmed);
  }

  Expression _parseComparison(String src) {
    // Look for symbolic operators (normalized earlier): >=, <=, ==, !=, >, <
    final ops = ['>=', '<=', '==', '!=', '>', '<'];
    for (final op in ops) {
      final idx = src.indexOf(op);
      if (idx != -1) {
        final left = _parseAddSub(src.substring(0, idx));
        final right = _parseAddSub(src.substring(idx + op.length));
        return BinaryExpr(op, left, right);
      }
    }
    // Single '=' used as equality (avoid '==')
    int eqIdx = -1;
    for (int i = 0; i < src.length; i++) {
      if (src[i] == '=') {
        final isDouble = (i + 1 < src.length && src[i + 1] == '=');
        if (!isDouble) {
          eqIdx = i;
          break;
        }
      }
    }
    if (eqIdx != -1) {
      return BinaryExpr('==', _parseAddSub(src.substring(0, eqIdx)),
          _parseAddSub(src.substring(eqIdx + 1)));
    }
    return _parseAddSub(src);
  }

  Expression _parseAddSub(String src) {
    // Left-to-right scan for + and - at top level, respecting unary minus
    final terms = <String>[];
    final ops = <String>[]; // '+' | '-'
    final buf = StringBuffer();
    String? prevNonSpace;
    for (int i = 0; i < src.length; i++) {
      final ch = src[i];
      if (ch == '+' || ch == '-') {
        // Determine if this is a binary operator or unary sign
        // It's binary if previous non-space char exists and is not an operator
        if (prevNonSpace != null &&
            prevNonSpace != '+' &&
            prevNonSpace != '-' &&
            prevNonSpace != '*' &&
            prevNonSpace != '/') {
          terms.add(buf.toString().trim());
          buf.clear();
          ops.add(ch);
          prevNonSpace = null;
          continue;
        }
      }
      buf.write(ch);
      if (ch.trim().isNotEmpty) prevNonSpace = ch;
    }
    if (ops.isEmpty) return _parseMul(src);
    terms.add(buf.toString().trim());
    Expression expr = _parseMul(terms[0]);
    for (var i = 0; i < ops.length; i++) {
      expr = BinaryExpr(ops[i], expr, _parseMul(terms[i + 1]));
    }
    return expr;
  }

  Expression _parseMul(String src) {
    // Support both '*' and '/' at the same precedence (left-associative)
    final tokens = <String>[];
    final ops = <String>[]; // '*', '/'
    var current = StringBuffer();
    for (int i = 0; i < src.length; i++) {
      final ch = src[i];
      if (ch == '*' || ch == '/') {
        tokens.add(current.toString().trim());
        current = StringBuffer();
        ops.add(ch);
      } else {
        current.write(ch);
      }
    }
    final last = current.toString().trim();
    if (tokens.isEmpty) {
      return _parsePrimary(src);
    }
    tokens.add(last);
    Expression expr = _parsePrimary(tokens[0]);
    for (var i = 0; i < ops.length; i++) {
      final right = _parsePrimary(tokens[i + 1]);
      expr = BinaryExpr(ops[i], expr, right);
    }
    return expr;
  }

  Expression _parsePrimary(String src) {
    final s = src.trim();
    // Verb arithmetic forms
    if (s.startsWith('Add ')) {
      // Add a and b
      final andIdx = s.indexOf(' and ');
      if (andIdx == -1) throw FormatException('Invalid Add syntax');
      final a = s.substring(4, andIdx).trim();
      final b = s.substring(andIdx + 5).trim();
      return BinaryExpr('+', _parseExpression(a), _parseExpression(b));
    }
    if (s.startsWith('Subtract ')) {
      // Subtract a from b  => b - a
      final fromIdx = s.indexOf(' from ');
      if (fromIdx == -1) throw FormatException('Invalid Subtract syntax');
      final a = s.substring(9, fromIdx).trim();
      final b = s.substring(fromIdx + 6).trim();
      return BinaryExpr('-', _parseExpression(b), _parseExpression(a));
    }
    if (s.startsWith('Multiply ')) {
      // Multiply a and b
      final andIdx = s.indexOf(' and ');
      if (andIdx == -1) throw FormatException('Invalid Multiply syntax');
      final a = s.substring(9, andIdx).trim();
      final b = s.substring(andIdx + 5).trim();
      return BinaryExpr('*', _parseExpression(a), _parseExpression(b));
    }
    if (s.startsWith('Divide ')) {
      // Divide a by b
      final byIdx = s.indexOf(' by ');
      if (byIdx == -1) throw FormatException('Invalid Divide syntax');
      final a = s.substring(7, byIdx).trim();
      final b = s.substring(byIdx + 4).trim();
      return BinaryExpr('/', _parseExpression(a), _parseExpression(b));
    }
    // future: parentheses
    // literal number
    final numVal = num.tryParse(s);
    if (numVal != null) return LiteralExpr(numVal);
    // boolean literals
    if (s == 'true' || s == 'false') return LiteralExpr(s == 'true');
    // string
    if (s.startsWith('"') && s.endsWith('"')) {
      return LiteralExpr(s.substring(1, s.length - 1));
    }
    // 'nothing' literal (maps to null in emitted code)
    if (s == 'nothing' || s == 'Nothing') return LiteralExpr(null);
    return IdentifierExpr(s);
  }

  // Helpers for collections parsing
  Expression? _tryParseListLiteral(String src) {
    // Forms:
    // - Make a list of a, b, c
    // - Make a mutable list of a, b
    // - List contains a, b, c  (legacy)
    final s = src.trim();
    bool mutable = false;
    bool legacy = false;
    String? itemsStr;
    if (s.startsWith('Make a ')) {
      var rest = s.substring('Make a '.length).trim();
      if (rest.startsWith('mutable list of ')) {
        mutable = true;
        itemsStr = rest.substring('mutable list of '.length).trim();
      } else if (rest.startsWith('list of ')) {
        itemsStr = rest.substring('list of '.length).trim();
      }
    } else if (s.startsWith('List contains ')) {
      legacy = true;
      itemsStr = s.substring('List contains '.length).trim();
    }
    if (itemsStr == null) return null;
    final parts = itemsStr.isEmpty
        ? <Expression>[]
        : itemsStr.split(',').map((e) => _parseExpression(e.trim())).toList();
    return ListLiteralExpr(parts, isMutable: mutable, isLegacy: legacy);
  }

  Expression? _tryParseMapLiteral(String src) {
    // Forms:
    // - Make a dictionary with "k": v, "k2": v2
    // - Make a mutable dictionary with ...
    // - Dictionary contains "k": v, ... (legacy)
    final s = src.trim();
    bool mutable = false;
    bool legacy = false;
    String? itemsStr;
    if (s.startsWith('Make a ')) {
      var rest = s.substring('Make a '.length).trim();
      if (rest.startsWith('mutable dictionary with ')) {
        mutable = true;
        itemsStr = rest.substring('mutable dictionary with '.length).trim();
      } else if (rest.startsWith('dictionary with ')) {
        itemsStr = rest.substring('dictionary with '.length).trim();
      }
    } else if (s.startsWith('Dictionary contains ')) {
      legacy = true;
      itemsStr = s.substring('Dictionary contains '.length).trim();
    }
    if (itemsStr == null) return null;
    if (itemsStr.isEmpty) return MapLiteralExpr(<Expression>[], <Expression>[], isMutable: mutable, isLegacy: legacy);
    final pairs = _splitTopLevel(itemsStr, ',');
    final keys = <Expression>[];
    final values = <Expression>[];
    for (final p in pairs) {
      final idx = _indexOfTopLevelColon(p);
      if (idx == -1) {
        throw FormatException('Dictionary pair missing ":": $p');
      }
      final k = p.substring(0, idx).trim();
      final v = p.substring(idx + 1).trim();
      keys.add(_parseExpression(k));
      values.add(_parseExpression(v));
    }
    return MapLiteralExpr(keys, values, isMutable: mutable, isLegacy: legacy);
  }

  Expression? _tryParseIndexing(String src) {
    // '<expr> at <expr>'
    final s = src.trim();
    final atIdx = s.lastIndexOf(' at ');
    if (atIdx == -1) return null;
    final base = s.substring(0, atIdx).trim();
    final idxStr = s.substring(atIdx + 4).trim();
    return IndexExpr(_parseExpression(base), _parseExpression(idxStr));
  }

  Expression? _tryParseKeysValues(String src) {
    // 'keys of <expr>' | 'values of <expr>'
    final s = src.trim();
    if (s.startsWith('keys of ')) {
      return KeysOfExpr(_parseExpression(s.substring('keys of '.length).trim()));
    }
    if (s.startsWith('values of ')) {
      return ValuesOfExpr(_parseExpression(s.substring('values of '.length).trim()));
    }
    return null;
  }

  int _indexOfTopLevelColon(String src) {
    // No parentheses parsing yet; just find the first ':' not inside quotes
    bool inStr = false;
    for (int i = 0; i < src.length; i++) {
      final ch = src[i];
      if (ch == '"') inStr = !inStr;
      if (!inStr && ch == ':') return i;
    }
    return -1;
  }

  // Split by a delimiter string at top level (no parentheses parsing yet)
  List<String> _splitTopLevel(String src, String delimiter) {
    final parts = <String>[];
    int start = 0;
    int i = 0;
    while (i <= src.length - delimiter.length) {
      if (src.substring(i, i + delimiter.length) == delimiter) {
        parts.add(src.substring(start, i).trim());
        i += delimiter.length;
        start = i;
      } else {
        i++;
      }
    }
    if (start == 0) return [src.trim()];
    parts.add(src.substring(start).trim());
    return parts;
  }

  String _normalizeComparators(String src) {
    // Order matters: longest phrases first
    var s = src;
    // Canonical worded comparators (title case)
    s = s.replaceAll(' Greater Or Equal ', ' >= ');
    s = s.replaceAll(' Less Or Equal ', ' <= ');
    s = s.replaceAll(' Not Equals ', ' != ');
    s = s.replaceAll(' Equals ', ' == ');
    s = s.replaceAll(' Greater Than ', ' > ');
    s = s.replaceAll(' Less Than ', ' < ');
    // Legacy/back-compat verbal forms (lowercase)
    s = s.replaceAll(' is not equal to ', ' != ');
    s = s.replaceAll(' is equal to ', ' == ');
    s = s.replaceAll(' is greater than ', ' > ');
    s = s.replaceAll(' is less than ', ' < ');
    // v0.2 forms
    s = s.replaceAll(' is at least ', ' >= ');
    s = s.replaceAll(' is at most ', ' <= ');
    s = s.replaceAll(' is not ', ' != ');
    // Finally, simple ' is ' -> equality (avoid consuming parts of the longer phrases handled above)
    s = s.replaceAll(' is ', ' == ');
    // Case variants for leading capital (e.g., ' Is ')
    s = s.replaceAll(' Is ', ' == ');
    s = s.replaceAll(' Is not ', ' != ');
    s = s.replaceAll(' Is at least ', ' >= ');
    s = s.replaceAll(' Is at most ', ' <= ');
    return s;
  }

  String _normalizeLogic(String src) {
    var s = src;
    // Lowercase connectors to canonical tokens used by parser
    s = s.replaceAll(' and ', ' And ');
    s = s.replaceAll(' or ', ' Or ');
    s = s.replaceAll(' not ', ' Not ');
    // Handle leading 'not '
    if (s.startsWith('not ')) {
      s = 'Not ' + s.substring(4);
    }
    return s;
  }

  bool _containsBareEquality(String src) {
    for (int i = 0; i < src.length; i++) {
      if (src[i] != '=') continue;
      final prev = i > 0 ? src[i - 1] : null;
      final next = i + 1 < src.length ? src[i + 1] : null;
      final prevIsComparator =
          prev == '!' || prev == '<' || prev == '>' || prev == '=';
      final nextIsEq = next == '=';
      if (prevIsComparator || nextIsEq) {
        // Part of !=, <=, >= or == — allowed
        continue;
      }
      return true; // bare '=' found
    }
    return false;
  }

  String _normalizeArithmetic(String src) {
    // Replace phrase operators with symbolic ones to reuse arithmetic parsing
    // Handle both lowercase and Capitalized initial forms.
    final replacements = <String, String>{
      ' divided by ': ' / ',
      ' Divided by ': ' / ',
      ' times ': ' * ',
      ' Times ': ' * ',
      ' plus ': ' + ',
      ' Plus ': ' + ',
      ' minus ': ' - ',
      ' Minus ': ' - ',
    };
    var s = src;
    replacements.forEach((k, v) {
      s = s.replaceAll(k, v);
    });
    return s;
  }
}
