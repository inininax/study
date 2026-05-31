"use strict";
debugger;

console.log("1:", Object.is(1, "1")); // false
console.log("2:", Object.is(NaN, NaN), NaN === NaN); // true false

console.log("3:", Object.is(0, -0), 0 === -0); // false true
console.log("4:", Object.is(-0, 0), -0 === 0); // false true

console.log("5:", Object.is(-0, -0), -0 === -0); // true true
console.log("6:", Object.is(NaN, 0 / 0), NaN === 0 / 0); // true false

console.log("7:", Object.is(null, null), null === null); // true true
console.log("8:", Object.is(undefined, null), undefined === null); // false false

let dummy;
