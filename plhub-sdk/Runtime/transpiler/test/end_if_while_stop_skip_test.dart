import 'package:test/test.dart';

import '../src/parser.dart';
import '../src/ast.dart';

void main() {
  group('End If / End While', () {
    test('If block with End If', () {
      final src = [
        'If x is 1',
        'Write "one"',
        'End If',
      ];
      final p = Parser(src).parse();
      expect(p.program.statements.first, isA<IfStmt>());
    });

    test('While block with End While', () {
      final src = [
        'While x is less than 3',
        'Write "tick"',
        'End While',
      ];
      final p = Parser(src).parse();
      expect(p.program.statements.first, isA<WhileStmt>());
    });
  });

  group('Stop/Skip', () {
    test('parse Stop/Skip as loop control', () {
      final src = [
        'While x is less than 3',
        'Skip',
        'Stop',
        'End',
      ];
      final p = Parser(src).parse();
      final w = p.program.statements.first as WhileStmt;
      expect(w.body[0], isA<SkipStmt>());
      expect(w.body[1], isA<StopStmt>());
    });
  });

  group('Equals in conditions warning', () {
    test('single = rejected with hint', () {
      try {
        Parser(['If x = 1 Write "ok" Otherwise Write "no"']).parse();
        fail('Expected FormatException');
      } catch (e) {
        expect(e.toString(), contains("phrasal equality"));
      }
    });
  });
}
