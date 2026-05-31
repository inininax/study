"use strict";
debugger;

let gen = function* () {
  return yield yield yield;
}
let genObj = gen();

console.log(genObj.next());
console.log(genObj.next(10));
console.log(genObj.next(20));
console.log(genObj.next(30));

// { value: undefined, done: false }
// { value: 10, done: false }
// { value: 20, done: false }
// { value: 30, done: true }
