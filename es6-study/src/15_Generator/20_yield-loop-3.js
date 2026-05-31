"use strict";
debugger;

let gen = function*(value) {
  yield value;
  yield* gen(value + 10);
}
let genObj = gen(1);

console.log(genObj.next()); // 1
console.log(genObj.next()); // 11
console.log(genObj.next()); // 21
console.log(genObj.next()); // 31

// { value: 1, done: false }
// { value: 11, done: false }
// { value: 21, done: false }
// { value: 31, done: false }