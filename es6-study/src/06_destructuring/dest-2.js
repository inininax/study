"use strict";
debugger;

let one, two, three, four, other;
[one, , , four] = [1, 2, 3, 4];
console.log(one, four); // 1, 4

[one, ...other] = [1, 2, 3, 4];
console.log(other); // [2, 3, 4]

let dummy;
