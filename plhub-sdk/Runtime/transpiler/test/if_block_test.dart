import 'package:test/test.dart';

import '../src/parser.dart';
import '../src/ast.dart';

void main() {
  group('If block parsing', () {
    test('if-then block', () {
      final src = [
        'If x > 1',
        'Write "big"',
        'End',
      ];
      final p = Parser(src).parse();
      expect(p.program.statements.length, 1);
      final ifs = p.program.statements.first as IfStmt;
      expect(ifs.thenBranch.length, 1);
      expect(ifs.elseBranch, isNull);
      expect(ifs.thenBranch.first, isA<PrintStmt>());
    });

    test('if-then-else block', () {
      final src = [
        'If x > 1',
        'Write "big"',
        'Otherwise',
        'Write "small"',
        'End',
      ];
      final p = Parser(src).parse();
      final ifs = p.program.statements.first as IfStmt;
      expect(ifs.thenBranch.length, 1);
      expect(ifs.elseBranch, isNotNull);
      expect(ifs.elseBranch!.length, 1);
    });

    test('missing End error with line number', () {
      final src = [
        'If x > 1',
        'Write "big"',
      ];
      try {
        Parser(src).parse();
        fail('Expected FormatException');
      } catch (e) {
        expect(e.toString(), contains('If block missing End'));
        expect(e.toString(), contains('Line'));
      }
    });
  });
}
