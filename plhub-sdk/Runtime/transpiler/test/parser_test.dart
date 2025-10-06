import 'package:test/test.dart';

import '../src/parser.dart';
import '../src/ast.dart';

void main() {
  group('Parser', () {
    test('skips # comments and blank lines', () {
      final src = [
        '  # leading comment',
        'Set x to 1  # inline',
        '',
        'Write "Hi"  # another',
      ];
      final parser = Parser(src);
      final result = parser.parse();
      expect(result.program.statements.length, 2);
      expect(result.program.statements[0], isA<AssignStmt>());
      expect(result.program.statements[1], isA<PrintStmt>());
    });

    test('error message includes line number', () {
      final src = [
        'Set x to 1',
        'If x Write "ok" Otherwise', // malformed
      ];
      final parser = Parser(src);
      try {
        parser.parse();
        fail('Expected FormatException');
      } catch (e) {
        expect(e.toString(), contains('Line 2'));
      }
    });
  });
}
