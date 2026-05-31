"use strict";
debugger;

let gen = function*(value){
  console.log('1 value', value);
  value = value + 10;
  let d = yield ++value; // 12

  console.log('2 d', d);
  console.log('2 value', value);
  value = value + 7;
  yield ++value; // 20
};
let genObj = gen(1);

console.log(genObj.next()); // 12
console.log('-----------');
console.log(genObj.next(1)); // 20
console.log('-----------');
console.log(genObj.next()); // undefined

// 1 value 1
// { value: 12, done: false }
// -----------
// 2 d 1
// 2 value 12
// { value: 20, done: false }
// -----------
// { value: undefined, done: true }