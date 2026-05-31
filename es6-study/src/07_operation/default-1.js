"use strict";
debugger;

let [one, two, five = 5] = [1, 2];
console.log(five); // 5

[one, two, five = 5] = [1, 2, 77];
console.log(five); // 77

let {six, seven = 7} = {six: 6};
console.log(six, seven); // 6, 7


let dummy;
