"use strict";
debugger;

let target = "123가나다";

console.log(target.endsWith("가나다")); // true
console.log(target.endsWith("가나")); // false
console.log(target.endsWith("가나", 5)); // true
