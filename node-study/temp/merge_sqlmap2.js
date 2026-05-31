'use strict';

/**
 * ERD 등이 제대로 없으면서
 * 테이블이 200 ~ 900개 가량이라 시스템 전체를 파악하고 있는 사람이 없을 때
 * 
 * 어쩔 수 없이 테이블 목록을 sql로 구한 후 소스에서 직접 테이블이 사용되는지 찾는 용도로 사용
 */

// require
const fs = require('fs');
const path = require('path');
const util = require('util');
const glob = require('glob');

// ex : 현재경로/test
// let currentPath = path.join(__dirname, '/test');
// console.log('currentPath : %s', currentPath);

const removeComment = function (value) {
	value = value.replace(/\r\n/g, '__rn__');
	value = value.replace(/<!--[^>](.*?)-->/g, '');
	value = value.replace(/__rn__/g, '\r\n');
	return value;
};

// start log
console.log('Start : %o', new Date());

// result data
const inputXMLPathPattern = 'C:/xxxxx/src/main/**/*Mapper.xml';
let output = '';

// read controller
glob(inputXMLPathPattern, function (er, filepaths) {
	console.log(filepaths);

	for (let i in filepaths) {
		let filedata = fs.readFileSync(filepaths[i], 'utf-8');
		filedata = filedata.replace('<?xml version="1.0" encoding="UTF-8"?>', '');
		filedata = filedata.replace('<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">', '');

		// filedata = filedata.replace('<?xml version="1.0" encoding="UTF-8"?>', '');
		// filedata = filedata.replace('<!DOCTYPE sqlMap PUBLIC "-//ibatis.apache.org//DTD SQL Map 2.0//EN" "http://ibatis.apache.org/dtd/sql-map-2.dtd">', '');
		// filedata = filedata.replace("<!DOCTYPE sqlMap PUBLIC '-//ibatis.apache.org//DTD Sql Map 2.0//EN' 'http://ibatis.apache.org/dtd/sql-map-2.dtd'>", '');

		filedata = removeComment(filedata);

		output += filedata + '\n';
	}

	output = '<?xml version="1.0" encoding="UTF-8"?>\n<root>\n' + output + '\n</root>';

	// write file
	try {
		fs.mkdirSync(path.join(__dirname, './output'));
	} catch (e) {
		console.log('message : %s', e.message);
	}
	fs.writeFileSync(path.join(__dirname, './output/merge_sqlmap2.xml'), output, 'utf-8');

	// end log
	console.log('End : %o', new Date());
	console.log('Output : %s', output);
});