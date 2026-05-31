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
		setTimeout(() => {
			this.plus(); // 상위 this 그대로 사용 가능
			console.log(this.count); // 21
		}, 1000);
	}
};
let newSports = new Sports();
newSports.get();


let dummy;
