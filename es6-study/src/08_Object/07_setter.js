"use strict";
debugger;

let obj = {
    set setValue(value) {
        this.value = value;
    },
    set setValue2(value) {
        this.value2 = value;
    }
};

obj.setValue = 123;
console.log(obj.value); // 123
console.log(obj.value2); // undefined

obj.setValue2 = 456;
console.log(obj.value2); // 456

let dummy;
