"use strict";
debugger;

console.log("1:", Number.MAX_SAFE_INTEGER); // 9007199254740991
console.log("2:", Math.pow(2, 53) - 1); // 9007199254740991
console.log("3:", Number.MIN_SAFE_INTEGER); // -9007199254740991
console.log("4:", -(Math.pow(2, 53) - 1)); // -9007199254740991

let dummy;

