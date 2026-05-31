"use strict";
debugger;

let sym = Symbol("123");
let obj = {[sym]: "456"};

console.log(obj);
console.log('----------------------');
console.log(obj[sym]);
console.log('----------------------');
console.log(obj.sym);

// { [Symbol(123)]: '456' }
// 456
// undefined
