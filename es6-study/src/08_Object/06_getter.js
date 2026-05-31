"use strict";
debugger;

let obj = {
    value: 123,
    get getValue() {
        return this.value;
    },
    get getValue2() {
        return `${this.value} 2`;
    }
};
console.log(obj.getValue); // 123
console.log(obj.getValue2); // 123 2

try {
    console.log(obj.getValue2());
} catch (e) {
    console.log(e); // TypeError: obj.getValue2 is not a function
}

let dummy;
