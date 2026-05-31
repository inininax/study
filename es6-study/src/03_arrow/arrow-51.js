"use strict";
debugger;

let Sports = function () {
	this.count = 20;
};
Sports.prototype = {
	plus: function () {
		this.count += 1;
	},
	get: function () {
		setTimeout(function () {
			console.log(this === window); // true
			console.log(this.plus); // undefined
		}, 1000);
	}
};
let newSports = new Sports();
newSports.get();


let dummy;
