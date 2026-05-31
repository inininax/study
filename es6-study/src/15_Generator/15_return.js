"use strict";
debugger;

let gen = function* (start) {
  console.log('start', start);
  let count = start;
  console.log('count', count);
  while (true) {
    yield ++count;
  }
}
let genObj = gen(10);

console.log(genObj.next()); // 11
console.log('----------------------------');
console.log(genObj.return(77)); // 77
console.log('----------------------------');
console.log(genObj.next(55));
console.log('----------------------------');
console.log(genObj.next(55));

// start 10
// count 10
// { value: 11, done: false }
// ----------------------------
// { value: 77, done: true }
// ----------------------------
// { value: undefined, done: true }
// ----------------------------
// { value: undefined, done: true }