"use strict";
debugger;

class ExtendArray extends Array {
  constructor() {
    super();
  }
  getTotal() {
    let total = 0;
    for (let value of this) {
      total += value;
    }
    return total;
  }
}

let arr = new ExtendArray();
arr.push(10, 20, 30, 40);

console.log(arr.getTotal());