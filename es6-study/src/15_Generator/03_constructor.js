"use strict";
debugger;

let GenConst = Object.getPrototypeOf(function*(){}).constructor;
let sports = new GenConst(
  "one", "two",
  "console.log('함수 블록'); yield one + two"
);
let genObj = sports(3, 4);

console.log(genObj.next()); // 함수 블록, { value: 7, done: false }
console.log(genObj.next()); // { value: undefined, done: true }



let dummy;
