void main() {
  printOne();
  printTwo();
  printThree();
}

void printOne() {
  print("One");
}

void printTwo() async {
  Future.delayed(Duration(seconds: 1), () {
    print("Future!!");
  });
  print("Two");
}

void printThree() {
  print("Three");
}
