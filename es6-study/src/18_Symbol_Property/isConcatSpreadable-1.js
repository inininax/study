"use strict";
debugger;

let one = [11, 12],
    two = [21, 22];

let result = one.concat(two);
console.log(result, result.length);
// [ 11, 12, 21, 22 ] 4

two[Symbol.isConcatSpreadable] = false;
result = one.concat(two);
console.log(result, result.length);
// [ 11, 12, [ 21, 22, [Symbol(Symbol.isConcatSpreadable)]: false ] ] 3

two[Symbol.isConcatSpreadable] = true;
result = one.concat(two);
console.log(result, result.length);
// [ 11, 12, 21, 22 ] 4
