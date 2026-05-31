"use strict";
debugger;

let one, two, three, four, five;
const values = [1, 2, 3];

[one, two, three] = values;
console.log("A:", one, two, three); // A: 1 2 3

[one, two] = values;
console.log("B:", one, two); // B: 1 2

[one, two, three, four] = values;
console.log("C:", one, two, three, four); // C: 1 2 3 undefined

[one, two, [three, four]] = [1, 2, [73, 74]];
console.log("D:", one, two, three, four); // D: 1 2 73 74

let dummy;
