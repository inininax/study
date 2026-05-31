"use strict";
debugger;

function* sports(one){
  yield one;
  let check = 10;
}
let genObj = sports(10);

console.log(genObj.next());
console.log(genObj.next());

// { value: 10, done: false }
// { value: undefined, done: true }

let dummy;
