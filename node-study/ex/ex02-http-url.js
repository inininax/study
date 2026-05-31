// custom module
var myfirstmodule = require('./module/myfirstmodule.js');

// node module
var http = require('http');
var url = require('url');

console.log('create server..');

http.createServer(function(req, res) {

	// console.log('request server : %o', req);
	// console.log('response server : %o', res);

	res.writeHead(200, {
		'Content-Type' : 'text/html'
	});

	var dt = myfirstmodule.myDateTime();
	var query = url.parse(req.url, true).query;
	var txt = query.year + ' ' + query.month;

	res.end(txt);

}).listen(8888);
