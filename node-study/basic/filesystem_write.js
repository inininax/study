"use strict";

// require
const fs = require('fs');
const path = require('path');

// variable
let targetPath = path.join(__dirname, '../output/');
let fileData = 'File Data';

// file path
console.log('__filename : %s', __filename);
console.log('__dirname : %s', __dirname);

// 폴더 생성
try {
	fs.mkdirSync(targetPath);
	console.log('mkdirSync : %s', targetPath);
} catch (e) {
	// if (e.code != 'EEXIST')
	console.log('mkdirSync e : %s', e.message);
}

// async 비동기식 파일 쓰기
fs.writeFile(targetPath + 'writeFile.txt', fileData, 'utf-8', function(e) {
	if (e) {
		console.log('writeFile e : %o', e);
	} else {
		console.log('Write Async');
	}
});

// sync 동기식 파일 쓰기
try {
	fs.writeFileSync(targetPath + 'writeFileSync.txt', fileData, 'utf-8');
	console.log('Write Sync');
} catch (e) {
	console.log('writeFileSync e : %o', e);
}