"use strict";
debugger;

let item = "tennis";
let sports = {
    [item]: 1,
    [item + "Game"]: "윔블던",
    [item + "Method"]() {
        return this[item];
    }
};
console.log(sports.tennis); // 1
console.log(sports.tennisGame); // 윔블던
console.log(sports.tennisMethod()); // 1

let dummy;
