"use strict";
debugger;

var obj = {};
Object.defineProperty(obj, "item", {
    set: function (param) {
        this.sports = `SET ${param}`;
    },
    get: function () {
        return `GET ${this.sports}`;
    }
});

obj.item = "야구";
console.log(obj.sports); // SET 야구
console.log(obj.item); // GET SET 야구
let dummy;
