import 'dart:convert';

var scores = [
  {"score": 40},
  {"score": 60}
];

void main() {
  var jsonText = jsonEncode(scores);

  print(jsonText ==
      '''[{"score":40},{"score":60}]''');
}
