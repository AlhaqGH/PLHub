// Moved from root/program.dart
// Example invoice calculation (originally root program.dart). No external runtime needed.

Future<void> main() async {
  var subtotal = 120;
  var discount = 10;
  var taxRate = 0.07;
  var discounted = (subtotal - discount);
  var tax = (discounted * taxRate);
  var total = (discounted + tax);
  print(("Subtotal: " + (subtotal).toString()));
  print(("Discount: " + (discount).toString()));
  print(("Tax: " + (tax).toString()));
  print(("Total: " + (total).toString()));
}
