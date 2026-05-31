export {};

// enum number 할당 시 양방향 매핑

enum Fruit {
    Apple,
    Banana = 5,
    Orange
}

const v1: Fruit = Fruit.Apple;
const v2: Fruit = Fruit.Banana;

console.log(v1, v2, Fruit.Orange, Fruit[5]);
console.log(Fruit.Banana);
console.log(Fruit['Banana']);
console.log(Fruit[5]);

/*
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Fruit;
(function (Fruit) {
    Fruit[Fruit["Apple"] = 0] = "Apple";
    Fruit[Fruit["Banana"] = 5] = "Banana";
    Fruit[Fruit["Orange"] = 6] = "Orange";
})(Fruit || (Fruit = {}));
const v1 = Fruit.Apple;
const v2 = Fruit.Banana;
console.log(v1, v2);
*/