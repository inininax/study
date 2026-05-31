"use strict";
debugger;

let plus = (one, two = 2) => one + two;
console.log(plus(1)); // 3

console.log(plus(1, undefined)); // 3

console.log(plus(1, 70)); // 71


let dummy;
