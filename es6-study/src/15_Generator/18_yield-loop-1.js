"use strict";
debugger;

function* gen() {
  yield* [10, 20, 30];
}
let genObj = gen();

console.log(genObj.next());
console.log('------------------------');
console.log(genObj.next());
console.log('------------------------');
console.log(genObj.next());
console.log('------------------------');
console.log(genObj.next(77));

// { value: 10, done: false }
// ------------------------
// { value: 20, done: false }
// ------------------------
// { value: 30, done: false }
// ------------------------
// { value: undefined, done: true }