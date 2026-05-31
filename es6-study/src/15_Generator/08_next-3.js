"use strict";
debugger;

let gen = function*(param){
  let one = param + 1;
  yield one; // 11
  var two = 2;
  yield one + two; // 13
};
let genObj = gen(10);

console.log(genObj.next());
console.log(genObj.next());


let dummy;
