"use strict";
debugger;

let get = (...rest) => {
    console.log(rest); // [1, 2, 3]
    console.log(Array.isArray(rest)); // true
}

get(...[1, 2, 3]);

let dummy;