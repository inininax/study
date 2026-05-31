export {};

const enum Fruit {
    Apple,
    Banana,
    Orange
}

const v1: Fruit = Fruit.Apple;
const v2: Fruit = Fruit.Banana | Fruit.Orange;

console.log(v1, v2);
