"use strict";
debugger;

let obj = {};
obj[Symbol.iterator] = function*(){
  yield 10;
  yield 20;
  yield 30;
};

let result = [...obj];
console.log(result);
// [ 10, 20, 30 ]

console.log(obj);
// { [Symbol(Symbol.iterator)]: [GeneratorFunction (anonymous)] }

console.log(obj[0]);
// undefined
