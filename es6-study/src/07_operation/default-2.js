"use strict";
debugger;

let [one, two = one + 1, five = two + 3] = [1];
console.log(one, two, five); // 1, 2, 5

let dummy;
