"use strict";
debugger;

let sports = {
    event: "축구",
    player: 11
};
let dup = Object.assign({}, sports);
console.log(dup.player); // 11

dup.player = 33;
console.log(sports.player); // 11

sports.event = "수영";
console.log(dup.event); // 축구


let dummy;
