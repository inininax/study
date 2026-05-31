"use strict";
debugger;

let gen = function*(){
  return [yield yield];
};
let genObj = gen();

console.log(genObj.next());
console.log(genObj.next(10)); // 10
console.log(genObj.next(20)); // [20]

// { value: undefined, done: false }
// { value: 10, done: false }
// { value: [ 20 ], done: true }
