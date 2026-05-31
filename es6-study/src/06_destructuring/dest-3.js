"use strict";
debugger;

let {one, two} = {one: 1, nine: 9};
console.log(one, two); // 1, undefined

let three, four;
({three, four} = {three: 3, four: 4});
console.log(three, four); // 3, 4

let dummy;
