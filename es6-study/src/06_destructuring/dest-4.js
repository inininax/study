"use strict";
debugger;

let five, six;
({one: five, two: six} = {one: 10, two: 20});
console.log(five, six); // 10, 20

let {nine, plus: {ten}} = {nine: 9, plus: {ten: 10}};
console.log(nine, ten); // 9, 10

let dummy;
