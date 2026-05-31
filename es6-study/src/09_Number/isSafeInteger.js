"use strict";
debugger;

console.log("1:", Number.isSafeInteger(7)); // true
console.log("2:", Number.isSafeInteger(7.0)); // true
console.log("3:", Number.isSafeInteger(Number.MAX_SAFE_INTEGER)); // true
console.log("4:", Number.isSafeInteger(Number.MIN_SAFE_INTEGER)); // true
console.log("5:", Number.isSafeInteger(7.1)); // false
console.log("6:", Number.isSafeInteger("123")); // false
console.log("7:", Number.isSafeInteger(Number.MAX_SAFE_INTEGER + 1)); // false
console.log("8:", Number.isSafeInteger(Number.MIN_SAFE_INTEGER - 1)); // false

let dummy;