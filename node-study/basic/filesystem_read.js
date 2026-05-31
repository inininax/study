"use strict";

// require
const fs = require('fs');
const path = require('path');

// variable
let targetPath = path.join(__dirname, '../package.json');
let fileData = null;

// file path
console.log('__filename : %s', __filename);
console.log('__dirname : %s', __dirname);
console.log('Target Path : %s', targetPath);

// async 비동기식 파일 읽기
fs.readFile(targetPath, 'utf-8', function(error, data) {
	console.log('Read Async : %s', data);
});

// sync 동기식 파일 읽기
fileData = fs.readFileSync(targetPath, 'utf-8');
console.log('Read Sync : %s', fileData);