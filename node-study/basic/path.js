"use strict";

console.log('Ref : %s', 'https://nodejs.org/docs/latest/api/path.html');

// require
const path = require('path');

// variable
let targetPath = path.join(__dirname, '../package.json');

// file path
console.log('현재 파일 경로 : %s', __filename);
console.log('현재 폴더 경로 : %s', __dirname);
console.log('targetPath : %s', targetPath);
