// node module
var fs = require('fs');

fs.appendFile('ex04-filesystem.txt', 'Hello content!', function(err) {

	if (err) {
		throw err;
	}

	console.log('saved!');

});