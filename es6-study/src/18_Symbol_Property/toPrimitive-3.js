"use strict";
debugger;

let obj = {
  [Symbol.toPrimitive](hint){
    if (hint === "number"){
      return 30;
    };
    if (hint === "string"){
      return "문자열";
    };
    return "디폴트";
  }
};

console.log("1:", 20 + obj);
console.log("2:", 20 * obj);
// 1: 20디폴트
// 2: 600

console.log("3:", obj + 50);
console.log("4:", +obj + 50);
console.log("5:", `${obj}` + 123);
// 3: 디폴트50
// 4: 80
// 5: 문자열123
