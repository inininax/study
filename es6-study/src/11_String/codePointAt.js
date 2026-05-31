"use strict";
debugger;

console.log("가".codePointAt(0)); // 44032
console.log("나".codePointAt(0)); // 45208
console.log("가나".codePointAt(0)); // 44032
console.log("가나".codePointAt(1)); // 45208

let values = "ABC";
for (var value of values) {
    console.log(value, value.codePointAt(0));
}
// A 65
// B 66
// C 67
