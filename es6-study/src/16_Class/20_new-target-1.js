"use strict";
debugger;

let sports = function(){
  console.log(new.target);
}
sports(); // undefined
new sports(); // [Function: sports]


let dummy;
