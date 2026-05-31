"use strict";
debugger;

let count = {
    current: 1,
    get getCount() {
        return ++this.current;
    }
};

let mergeObj = {};
Object.assign(mergeObj, count);
console.log(mergeObj); // { current: 1, getCount: 2 }

let dummy;
