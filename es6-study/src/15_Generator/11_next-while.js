"use strict";
debugger;

let gen = function*(value) {
  let count = 0;
  while (value){
    yield ++count;
  }
};
let genObj = gen(true);

console.log(genObj.next()); // 1
console.log(genObj.next()); // 2
console.log(genObj.next()); // 3
console.log(genObj.next()); // 4
// infinite loop


let dummy;
