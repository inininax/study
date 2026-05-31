// custom module
var myfirstmodule = require('./module/myfirstmodule.js');

// node module
var http = require('http');
var url = require('url');
var fs = require('fs');

console.log('create server..');

http.createServer(function(req, res) {

	// console.log('request server : %o', req);
	// console.log('response server : %o', res);

	// sync 동기방식 파일 읽기
	// var data = fs.readFileSync('home.js', 'utf-8');
	// console.log('02 readSync: %s',data);
	
	// async 비동기방식 파일 읽기
	fs.readFile('./ex03-filesystem.html', function(err, data) {
		res.writeHead(200, {
			'Content-Type' : 'text/html'
		});

		var dt = myfirstmodule.myDateTime();
		var query = url.parse(req.url, true).query;

		console.log(data);
		
		// data = data.replace(/${year}/gi, query.year);
		// data = data.replace(/${month}/gi, query.month);

		res.end(data);
	});

}).listen(8888);
