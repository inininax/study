"use strict";
debugger;

let Sports = function () {
};

Sports.prototype.getCount = function () {
    return 123;
};

let fnObj = Object.setPrototypeOf({}, Sports);

console.log(fnObj.getCount); // undefined
console.log(fnObj.prototype.getCount.call(Sports)); // 123

let dummy;
