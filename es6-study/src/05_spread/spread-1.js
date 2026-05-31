"use strict";
debugger;

let one = [11, 12];
let two = [21, 22];
let spreadObj = [51, ...one, 52, ...two];

console.log(spreadObj); // [ 51, 11, 12, 52, 21, 22 ]
console.log(spreadObj.length); // 6

let dummy;
