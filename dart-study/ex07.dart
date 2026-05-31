main() async {
  var stream = Stream.fromIterable([1, 2, 3, 4, 5]);

  await stream.first.then((value) => print('First: $value'));
  await stream.last.then((value) => print('Last: $value'));
  await stream.isEmpty.then((value) => print('isEmpty: $value'));
  await stream.length.then((value) => print('Length: $value'));
  await stream.toList().then((value) => print('toList: $value'));
  await stream.toSet().then((value) => print('toSet: $value'));
  await stream.any((value) => value > 2).then((value) => print('Any: $value'));
  await stream.contains(3).then((value) => print('Contains: $value'));
  await stream.elementAt(2).then((value) => print('ElementAt: $value'));
  await stream
      .every((value) => value > 2)
      .then((value) => print('Every: $value'));
  await stream.join(',').then((value) => print('Join: $value'));
  await stream
      .lastWhere((value) => value > 2)
      .then((value) => print('LastWhere: $value'));
  await stream
      .singleWhere((value) => value == 3)
      .then((value) => print('SingleWhere: $value'));
  await stream
      .where((value) => value > 2)
      .toList()
      .then((value) => print('Where: $value'));
}
