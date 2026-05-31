"use strict";
debugger;

let sports = () => {
	try {
		let args = arguments; // ReferenceError: args is not defined, arrow function에서는 사용 불가
		console.log(args); // 
	} catch (error) {
		console.log("사용 불가");
	}
}
sports(1, 2);


let dummy;
