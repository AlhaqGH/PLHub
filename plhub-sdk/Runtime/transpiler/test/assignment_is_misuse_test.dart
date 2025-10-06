import 'package:test/test.dart';

import '../src/parser.dart';

void main() {
  test("'is' used like assignment suggests Set", () {
    try {
      Parser(['x is 5']).parse();
      fail('Expected FormatException');
    } catch (e) {
      expect(e.toString(), contains('Did you mean: Set x to'));
    }
  });
}
