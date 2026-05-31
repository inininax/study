"use strict";
debugger;

var obj = {};
Object.defineProperty(obj, "book", {
    get: function () {
        return "책";
    }
});

console.log(obj.book); // 책

let dummy;
