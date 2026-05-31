"use strict";
debugger;

let numberArray = [10, 20];
for (let value of numberArray){
  console.log(value);
  // 10
  // 20
};
let iteratorObj = numberArray[Symbol.iterator]();

console.log('----------------');
console.log(iteratorObj.next());
// { value: 10, done: false }

console.log('----------------');
console.log(iteratorObj.next());
// { value: 20, done: false }

console.log('----------------');
console.log(iteratorObj.next());
// { value: undefined, done: true }

console.log('----------------');
console.log(iteratorObj.next());
// { value: undefined, done: true }

let dummy;
