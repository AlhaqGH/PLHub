// Moved from transpiler/example/phrase_logic.dart
void main() {
  var age = 20;
  var hasID = true;
  var isStudent = false;
  var hasPaid = false;
  if (((age > 18) && (hasID == true))) {
    print("You may enter");
  }
  if (((age <= 12) || (isStudent == true))) {
    print("Discount");
  }
  if ((!hasPaid)) {
    print("Payment required");
  }
}
