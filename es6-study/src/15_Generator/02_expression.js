"use strict";
debugger;

let sports = function*(one, two){
  console.log("함수 블록");
  let value = one + two;
  yield value;
  yield value + one;
  yield value + two;
};
let genObj = sports(10, 20);

console.log(genObj.next()); // { value: 30, done: false }
console.log(genObj.next()); // { value: 40, done: false }
console.log(genObj.next()); // { value: 50, done: false }
console.log(genObj.next()); // { value: undefined, done: true }
console.log(genObj.next()); // { value: undefined, done: true }


let dummy;
