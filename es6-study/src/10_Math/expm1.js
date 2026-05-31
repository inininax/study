"use strict";
debugger;

console.log("1:", Math.expm1(-1));
console.log("2:", Math.expm1(0));
console.log("3:", Math.expm1(1));

console.log("4:", Math.expm1(Infinity));
console.log("5:", Math.expm1(-Infinity));

// 1: -0.6321205588285577
// 2: 0
// 3: 1.718281828459045
// 4: Infinity
// 5: -1

let dummy;
