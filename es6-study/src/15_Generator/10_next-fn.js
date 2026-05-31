"use strict";
debugger;

let getAmount = function*(qty, price){
  let amount = Math.floor(qty * price);
  let discount = yield amount;
  return amount - discount;
};
let getDiscount = function(amount){
  return amount > 1000 ? amount * 0.2 : amount * 0.1;
};
let amountObj = getAmount(10, 60);

let result = amountObj.next();
console.log(result); // 600

let dcAmount = getDiscount(result.value);
console.log(dcAmount); // 60

console.log(amountObj.next(dcAmount)); // 540


let dummy;
