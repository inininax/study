'use strict';

/**
 * Spring 프로젝트 중 Context에서 RequestMapping list를 뽑을 수 없거나
 * db, file 누락으로 정상적인 구동이 어려울 경우가 있을 때
 * 
 * Controller Java file을 읽어 RequestMapping을 텍스트로 비교하는
 * 그다지 섬세하지 못한 노가다
 */

// require
const fs = require('fs');
const path = require('path');
const util = require('util');
const glob = require('glob');


// ex : 현재경로/test
// let currentPath = path.join(__dirname, '/test');
// console.log('currentPath : %s', currentPath);


// start log
console.log('Start : %o', new Date());


// result data
let output = '';


// read controller
glob("C:/xxxxx/src/main/java/**/*Controller.java", function (er, filepaths) {

	for (let i in filepaths) {
		let filepath = filepaths[i];
		let controllerName = filepath.substring(filepath.lastIndexOf('/') + 1, filepath.lastIndexOf('.'));
		let filedata = fs.readFileSync(filepath, 'utf-8');
		let lines = filedata.split('\r\n');

		let parentPath;

		for (let j in lines) {
			let line = lines[j].trim();

			if (line.indexOf('@RequestMapping') == -1)
				continue;

			let nextLine = lines[parseInt(j) + 1].trim();

			if (nextLine.indexOf('public class') > -1) {
				parentPath = line.substring(line.indexOf('"') + 1, line.lastIndexOf('"')).replace('*', '');
				continue;
			}

			let subPath;

			if (line == '@RequestMapping') {
				subPath = nextLine.split(' ')[2];
				subPath = subPath.substring(0, subPath.indexOf('('));
			} else {
				subPath = line.substring(line.indexOf('"') + 1, line.lastIndexOf('"'));
			}

			// console.log('%s\t%s', controllerName, parentPath + subPath);
			output += util.format('%s\t%s\n', controllerName, parentPath + subPath);
		}
	}

	// write file
	try {
		fs.mkdirSync(path.join(__dirname, './output'));
	} catch (e) {
		console.log('message : %s', e.message);
	}
	fs.writeFileSync(path.join(__dirname, './output/find_requestmapping.txt'), output, 'utf-8');

	// end log
	console.log('End : %o', new Date());
	console.log('Output : %s', output);
});