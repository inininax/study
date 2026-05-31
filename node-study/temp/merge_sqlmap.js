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


// input
const inputSqlMapResXMLPath = 'C:/xxxxx/src/main/resources/';
const inputSqlMapConfigXMLPath = 'C:/xxxxx/src/main/resources/sqlmap-config.xml';


// start log
console.log('Start : %o', new Date());

// sql map config file 내용, 주석 제거
let sqlMapConfigData = fs.readFileSync(inputSqlMapConfigXMLPath, 'utf-8');
sqlMapConfigData = removeComment(sqlMapConfigData);


// sql map config file 내용의 sqlmap 경로 array
let lines = sqlMapConfigData.split('\n');
let output = '';

for (let i in lines) {
    let line = lines[i].trim();

    if (line.indexOf('<sqlMap resource="') == -1)
        continue;

    line = line.substring(line.indexOf('"') + 1);
    line = line.substring(0, line.indexOf('"'));
    line = inputSqlMapResXMLPath + line;

    let filedata = fs.readFileSync(line, 'utf-8');
    filedata = filedata.replace('<?xml version="1.0" encoding="UTF-8"?>', '');
    filedata = filedata.replace('<!DOCTYPE sqlMap PUBLIC "-//ibatis.apache.org//DTD SQL Map 2.0//EN" "http://ibatis.apache.org/dtd/sql-map-2.dtd">', '');
    filedata = filedata.replace("<!DOCTYPE sqlMap PUBLIC '-//ibatis.apache.org//DTD Sql Map 2.0//EN' 'http://ibatis.apache.org/dtd/sql-map-2.dtd'>", '');
    filedata = removeComment(filedata);

    output += filedata + '\n';
}

output = '<?xml version="1.0" encoding="UTF-8"?><root>' + output + '</root>';


// write file
try {
    fs.mkdirSync(path.join(__dirname, './output'));
} catch (e) {
    console.log('message : %s', e.message);
}
fs.writeFileSync(path.join(__dirname, './output/merge_sqlmap.xml'), output, 'utf-8');


// end log
console.log('End : %o', new Date());