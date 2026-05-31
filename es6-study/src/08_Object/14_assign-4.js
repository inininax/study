"use strict";
debugger;

let sports = {
    event: "축구",
    player: 11
}
let dup = sports;

sports.player = 55;
console.log(dup.player); // 55

dup.event = "농구";
console.log(sports.event); // 농구


let dummy;
