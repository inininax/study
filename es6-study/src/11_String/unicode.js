"use strict";
debugger;

// 16진수 이스케이프 시퀀스
console.log("1:", "\x31\x32\x33");

// 유니코드 이스케이프 시퀀스
console.log("2:", "\u0031\u0032\u0033");

// 유니코드 코드포인트 이스케이프
console.log("3:", "\u{34}\u{35}\u{36}");

// U+FFFF보다 큰 코드 포인트: 코끼리
//http://unicode-table.com/en/1F418/
console.log("4:", "\u{1f418}");

//서로게이트 페어(Surrogate pair)
console.log("5:", "\uD83D\uDC18");

// 1: 123
// 2: 123
// 3: 456
// 4: 🐘
// 5: 🐘

let dummy;
