"use strict";
debugger;

console.log("1:", Number.isFinite(Infinity), isFinite(Infinity));
console.log("2:", Number.isFinite(-Infinity), isFinite(-Infinity));

console.log("3:", Number.isFinite(0), isFinite(0));
console.log("4:", Number.isFinite("0"), isFinite("0"));

console.log("5:", Number.isFinite(null), isFinite(null));
console.log("6:", Number.isFinite(NaN), isFinite(NaN));

console.log("7:", Number.isFinite(undefined), isFinite(undefined));
console.log("8:", Number.isFinite(true), isFinite(true));

// 1: false false
// 2: false false
// 3: true true
// 4: false true
// 5: false true
// 6: false false
// 7: false false
// 8: false true

let dummy;

