import 'package:test/test.dart';

import '../src/parser.dart';
import '../src/ast.dart';

void main() {
  group('Phrase-based arithmetic', () {
    test('plus and minus', () {
      final p = Parser([
        'Set x to 1 plus 2',
        'Set y to x minus 3',
      ]).parse();
      final a = p.program.statements[0] as AssignStmt;
      expect((a.value as BinaryExpr).op, '+');
      final b = p.program.statements[1] as AssignStmt;
      expect((b.value as BinaryExpr).op, '-');
    });

    test('times and divided by', () {
      final p = Parser([
        'Set a to 2 times 3',
        'Set b to a divided by 4',
      ]).parse();
      final a = p.program.statements[0] as AssignStmt;
      expect((a.value as BinaryExpr).op, '*');
      final b = p.program.statements[1] as AssignStmt;
      expect((b.value as BinaryExpr).op, '/');
    });

    test('precedence: times/div before plus/minus', () {
      final p = Parser([
        'Set r to 1 plus 2 times 3 minus 4 divided by 2',
      ]).parse();
      final r = p.program.statements[0] as AssignStmt;
      // Should parse as ((1) + (2 * 3)) - (4 / 2)
      final top = r.value as BinaryExpr; // '-'
      expect(top.op, '-');
      final left = top.left as BinaryExpr; // '+'
      final right = top.right as BinaryExpr; // '/'
      expect(left.op, '+');
      expect(right.op, '/');
      expect((left.right as BinaryExpr).op, '*');
    });
  });
}
