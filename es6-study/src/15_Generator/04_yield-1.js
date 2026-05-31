"use strict";
debugger;

function* sports(one) {
  console.log('1 one', one);
  let two = yield one;

  console.log('2 two', two);
  let param = yield two + one; // <- eneratorObj.next({test: 35})
  
  console.log('3 one', one); // 10
  console.log('3 two', two); // undefined
  console.log('3 param', param); // {test: 35}
  yield param.test + one;
  yield two;
}
let generatorObj = sports(10);

console.log(generatorObj.next());
console.log('-----------------');
console.log(generatorObj.next());
console.log('-----------------');
console.log(generatorObj.next({test: 35}));
console.log('-----------------');
console.log(generatorObj.next());

// 1 one 10
// { value: 10, done: false }
// -----------------
// 2 two undefined
// { value: NaN, done: false }
// -----------------
// 3 one 10
// 3 two undefined
// 3 param { test: 35 }
// { value: 45, done: false }
// -----------------
// { value: undefined, done: false }