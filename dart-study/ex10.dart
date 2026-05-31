import 'dart:math' as math;

void main() {
  var rand = math.Random();
  Set<int> lotteryNumber = Set();

  while (lotteryNumber.length < 6) {
    lotteryNumber.add(rand.nextInt(45));
  }

  print(lotteryNumber);
}
