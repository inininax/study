"use strict";
debugger;

function get(one, two, three) {
    console.log(one + two + three);
}

const values = [10, 20, 30];
get(...values); // 60

let dummy;
