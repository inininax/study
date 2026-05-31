// require (모듈 참조)

var myfirstmodule = require('./module/myfirstmodule.js');
var http = require('http');

console.log('create server..');

http.createServer(function(req, res) {

	// console.log('request server : %o', req);
	// console.log('response server : %o', res);

	res.writeHead(200, {
		'Content-Type' : 'text/html'
	});

	var dt = myfirstmodule.myDateTime();

	res.write('My First Module. Currently : ' + dt.toString());
	res.end();

}).listen(8888);
