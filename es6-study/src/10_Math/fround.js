"use strict";
debugger;

let value = 0.1 + 0.2;
console.log("1:", value);
console.log("2:", Math.fround(value));

console.log("3:", 1.23);
console.log("4:", Math.fround(1.23));

// 1: 0.30000000000000004
// 2: 0.30000001192092896
// 3: 1.23
// 4: 1.2300000190734863


let dummy;