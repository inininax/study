"use strict";
debugger;

let one = 1, two = 2;
let result = String.raw({raw: "ABCDE"}, one, two, 3);
console.log(result); // A1B2C3DE

let dummy;
