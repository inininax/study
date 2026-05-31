"use strict";
debugger;

let arrayObj = [1, 2];
let iteratorObj = arrayObj[Symbol.iterator]();

console.log(iteratorObj); // Object [Array Iterator] {}
console.log("1:", typeof iteratorObj); // object
console.log("2:", iteratorObj.next()); // {value: 1, done: false}
console.log("3:", iteratorObj.next()); // {value: 1, done: false}
console.log("4:", iteratorObj.next()); // {value: undefined, done: true}

let dummy;
