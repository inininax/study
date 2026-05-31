"use strict";
debugger;

let plusGen = function*(value) {
  console.log('plusGen 1 value', value);
  yield value + 5;

  console.log('plusGen 2 value', value);
  yield value + 10;
};
let gen = function*(value) {
  console.log('gen 1 value', value);
  yield* plusGen(value);

  console.log('gen 2 value', value);
  yield value + 20;
};
let genObj = gen(10);
console.log('--------------------------------');
console.log("1:", genObj.next()); // 15
console.log('--------------------------------');
console.log("2:", genObj.next()); // 20
console.log('--------------------------------');
console.log("3:", genObj.next()); // 30
console.log('--------------------------------');

// --------------------------------
// gen 1 value 10
// plusGen 1 value 10
// 1: { value: 15, done: false }
// --------------------------------
// plusGen 2 value 10
// 2: { value: 20, done: false }
// --------------------------------
// gen 2 value 10
// 3: { value: 30, done: false }
// --------------------------------

