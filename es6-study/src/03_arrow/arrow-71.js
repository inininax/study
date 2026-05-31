"use strict";
debugger;

let Sports = function () {
	this.count = 20;
};
Sports.prototype = {
	add: () => {
		this.count += 1;
	}
};
let newSports = new Sports();

newSports.add();

console.log(newSports.count); // 20
console.log(window.count); // NaN array function의 경우 this가 instance를 참조하지 못함

let dummy;
