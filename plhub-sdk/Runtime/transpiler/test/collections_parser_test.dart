import 'package:test/test.dart';

import '../src/parser.dart';
import '../src/ast.dart';

void main() {
  group('Collections parsing', () {
    test('list literal forms', () {
      final p1 = Parser(['Set a to Make a list of 1, 2, 3']).parse();
      final assign1 = p1.program.statements.first as AssignStmt;
      expect(assign1.value, isA<ListLiteralExpr>());

      final p2 = Parser(['Set b to Make a mutable list of "x"']).parse();
      final assign2 = p2.program.statements.first as AssignStmt;
      final list2 = assign2.value as ListLiteralExpr;
      expect(list2.isMutable, true);

      final p3 = Parser(['Set c to List contains 1, 2']).parse();
      final list3 = (p3.program.statements.first as AssignStmt).value as ListLiteralExpr;
      expect(list3.isLegacy, true);
    });

    test('map literal forms', () {
      final p1 = Parser(['Set m to Make a dictionary with "a": 1, "b": 2']).parse();
      final m1 = (p1.program.statements.first as AssignStmt).value as MapLiteralExpr;
      expect(m1.keys.length, 2);

      final p2 = Parser(['Set n to Make a mutable dictionary with "k": "v"']).parse();
      final n = (p2.program.statements.first as AssignStmt).value as MapLiteralExpr;
      expect(n.isMutable, true);

      final p3 = Parser(['Set o to Dictionary contains "x": 1']).parse();
      final o = (p3.program.statements.first as AssignStmt).value as MapLiteralExpr;
      expect(o.isLegacy, true);
    });

    test('indexing and keys/values', () {
      final p = Parser([
        'Set a to Make a list of 1, 2',
        'Write a at 1',
        'Set d to Make a dictionary with "k": 3',
        'Write keys of d',
        'Write values of d',
      ]).parse();
      expect(p.program.statements[1], isA<PrintStmt>());
      expect((p.program.statements[1] as PrintStmt).expression, isA<IndexExpr>());
      expect((p.program.statements[3] as PrintStmt).expression, isA<KeysOfExpr>());
      expect((p.program.statements[4] as PrintStmt).expression, isA<ValuesOfExpr>());
    });

    test('add/remove statements', () {
      final p = Parser([
        'Add 3 to items',
        'Add "k": 1 to ages',
        'Remove "k" from ages',
      ]).parse();
      expect(p.program.statements[0], isA<AddToListStmt>());
      expect(p.program.statements[1], isA<AddToMapStmt>());
      expect(p.program.statements[2], isA<RemoveFromMapStmt>());
    });
  });
}
