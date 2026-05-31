"use strict";
debugger;

let oneObj = {};
Object.assign(oneObj, "ABC", undefined, null);
console.log(oneObj); // { '0': 'A', '1': 'B', '2': 'C' }

let twoObj = {};
Object.assign(twoObj, {key1: undefined, key2: null});
console.log(twoObj); // { key1: undefined, key2: null }

let dummy;
