"use strict";
debugger;

let iterator = [10, 20, 30].keys();
console.log('iterator', iterator);

for (var key of iterator){
  console.log(key, ":", iterator[key]);
};
// 0 : undefined
// 1 : undefined
// 2 : undefined
