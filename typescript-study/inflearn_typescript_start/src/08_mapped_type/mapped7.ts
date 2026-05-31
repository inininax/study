export {};

enum Fruit {
    Apple,
    Banana,
    Orange,
}

const FRUIT_PRICE: { [K in Fruit]: number } = {
    [Fruit.Apple]: 10000,
    [Fruit.Banana]: 20000,
    [Fruit.Orange]: 20000,
};