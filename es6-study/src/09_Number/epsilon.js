"use strict";
debugger;

let total = 0.1 + 0.2;
console.log(total); // 0.30000000000000004

let result = (Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON);
console.log(result); // true

let value = (Math.pow(10, 1) * 0.1) + (Math.pow(10, 1) * 0.2);
console.log(value / 10 === 0.3); // true

let dummy;

