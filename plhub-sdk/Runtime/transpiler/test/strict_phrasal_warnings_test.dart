import 'package:test/test.dart';

import '../src/transpiler.dart';

void main() {
  group('--strict-phrases warnings', () {
    test('warns on + - * / outside strings and comments', () {
      final lines = [
        'Set x to 1 + 2',
        'Set y to x - 3',
        'Set z to 2 * 5',
        'Set q to 8 / 2',
      ];
      final warnings = collectStrictPhrasalWarnings(lines, path: 'test.poh');
      expect(warnings.length, 4);
      expect(warnings[0], contains('test.poh:1'));
      expect(warnings[1], contains('test.poh:2'));
      expect(warnings[2], contains('test.poh:3'));
      expect(warnings[3], contains('test.poh:4'));
    });

    test('does not warn for phrasal operators', () {
      final lines = [
        'Set x to 1 plus 2',
        'Set y to x minus 3',
        'Set z to 2 times 5',
        'Set q to 8 divided by 2',
      ];
      final warnings = collectStrictPhrasalWarnings(lines, path: 'test.poh');
      expect(warnings, isEmpty);
    });

    test('ignores symbols inside strings', () {
      final lines = [
        'Write "1 + 2 = 3"',
        'Write "a - b"',
        'Write "x * y"',
        'Write "m / n"',
      ];
      final warnings = collectStrictPhrasalWarnings(lines, path: 'test.poh');
      expect(warnings, isEmpty);
    });

    test('ignores symbols after # comments', () {
      final lines = [
        'Set x to 1 plus 2 # + should be ignored',
        'Set y to x minus 3 # - should be ignored',
        'Set z to 2 times 5 # * should be ignored',
        'Set q to 8 divided by 2 # / should be ignored',
      ];
      final warnings = collectStrictPhrasalWarnings(lines, path: 'test.poh');
      expect(warnings, isEmpty);
    });

    test('warns once per line even with multiple symbols', () {
      final lines = [
        'Set r to 1 + 2 * 3 - 4 / 2',
      ];
      final warnings = collectStrictPhrasalWarnings(lines, path: 'test.poh');
      expect(warnings.length, 1);
      expect(warnings.first, contains('test.poh:1'));
    });
  });
}
