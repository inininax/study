class Car {
  int maxSpeed = 100;
  num price = 0;
  String name = '';

  Car(int maxSpeed, num price, String name) {
    this.maxSpeed = maxSpeed;
    this.price = price;
    this.name = name;
  }

  int saleCar() {
    price = price * 0.9;
    return price.toInt();
  }
}

void main() {
  Car one = Car(100, 100000, "one");
  Car two = Car(200, 200000, "two");
  Car three = Car(300, 300000, "three");

  one.saleCar();
  one.saleCar();
  one.saleCar();
  print(one.price);

  two.saleCar();
  two.saleCar();
  print(two.price);

  print(three.price);
}
