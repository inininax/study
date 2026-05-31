"use strict";
debugger;

console.log("1:", 1 + undefined);
console.log("2:", 1 + null);

console.log("3:", "1" + undefined);
console.log("4:", "1" + null);

// 1: NaN
// 2: 1
// 3: 1undefined
// 4: 1null
