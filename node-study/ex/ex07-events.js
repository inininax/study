let fs = require('fs');
let events = require('events');
let rs = fs.createReadStream('./ex/ex07-events.js');

rs.on('open', function() {
	console.log('file is open');
});

let eventEmitter = new events.EventEmitter();

// Create an event handler:
let myEventHandler = function() {
	console.log('I hear a scream!');
};

// Assign the event handler to an event:
eventEmitter.on('scream', myEventHandler);

// Fire the 'scream' event:
eventEmitter.emit('scream');

const TVALUE = '';


let sendMessage = param => {
	console.log(param);
};

console.log(sendMessage);
console.dir(sendMessage);
