void main() {
  checkVersion();
}

Future checkVersion() async {
  var version = await lookUpVersion();
  print(version);
}

int lookUpVersion() {
  return 12;
}
