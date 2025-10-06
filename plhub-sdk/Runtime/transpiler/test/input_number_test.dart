import 'package:test/test.dart';

import '../src/parser.dart';
import '../src/ast.dart';

void main() {
  group('Numeric input syntax', () {
    test('suffix form', () {
      final p = Parser(['Ask for age number']).parse();
      expect(p.program.statements.first, isA<InputNumberStmt>());
      expect((p.program.statements.first as InputNumberStmt).name, 'age');
    });

    test('legacy prefix form', () {
      final p = Parser(['Ask for number count']).parse();
      expect(p.program.statements.first, isA<InputNumberStmt>());
      expect((p.program.statements.first as InputNumberStmt).name, 'count');
    });

    test('case-insensitive NUMBER keyword', () {
      final p = Parser(['Ask for total NUMBER']).parse();
      expect(p.program.statements.first, isA<InputNumberStmt>());
      expect((p.program.statements.first as InputNumberStmt).name, 'total');
    });
  });
}
