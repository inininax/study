"use strict";
debugger;

let gen = function*(){
  try {
    yield 10;
    console.log('test');
  } catch (message) {
    console.log('message', message);
    yield message;
  }
  yield 20;
}
let genObj = gen();

console.log(genObj.next()); // 10
console.log('---------------------------');
console.log(genObj.throw("에러 발생")); // 
console.log('---------------------------');
console.log(genObj.next());

// { value: 10, done: false }
// ---------------------------
// message 에러 발생
// { value: '에러 발생', done: false }
// ---------------------------
// { value: 20, done: false }