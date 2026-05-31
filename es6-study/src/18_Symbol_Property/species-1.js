"use strict";
debugger;

let arrayObj = [1, 2, 3];
let sliceOne = arrayObj.slice(1, 3);
let sliceTwo = sliceOne.slice(1, 2);

console.log(arrayObj);
// [ 1, 2, 3 ]

console.log(sliceOne);
// [ 2, 3 ]

console.log(sliceTwo);
// [ 3 ]

let dummy;
