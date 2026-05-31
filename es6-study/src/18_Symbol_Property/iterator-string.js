"use strict";
debugger;

let stringValue = "1A";
for (let value of stringValue) {
  console.log(value);
  // 1
  // A
}
let iterObj = stringValue[Symbol.iterator]();

console.log(iterObj.next());
// { value: '1', done: false }

console.log(iterObj.next());
// { value: 'A', done: false }

console.log(iterObj.next());
// { value: undefined, done: true }
