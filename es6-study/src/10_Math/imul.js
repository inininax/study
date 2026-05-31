"use strict";
debugger;

// 2의 32승 값은 4,294,967,296
console.log("1:", Math.imul(2, 4));
console.log("2:", Math.imul(-3, -4));

console.log("3:", Math.imul(123456, 1000));
console.log("4:", Math.imul(123456, 10000));
console.log("5:", Math.imul(123456, 100000));

// 1: 8
// 2: 12
// 3: 123456000
// 4: 1234560000
// 5: -539301888


let dummy;

