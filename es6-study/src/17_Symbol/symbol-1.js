"use strict";
debugger;

const sym = Symbol();
console.log("1:", sym);
console.log("2:", typeof sym);
console.log("3:", Symbol("주석"));
console.log("4:", sym == Symbol());

// 1: Symbol()
// 2: symbol
// 3: Symbol(주석)
// 4: false