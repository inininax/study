"use strict";
debugger;

let getTotal = ([one, two] = [10, 20]) => one + two;
console.log(getTotal()); // 30

let getValue = ({two: value} = {two: 20}) => value;
console.log(getValue()); // 20


let dummy;
