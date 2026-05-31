"use strict";
debugger;

var sports = "축구";
let music = "재즈";

function get(){
  var sports = "농구";
  let music = "클래식";

  console.log("1:", sports); // 농구
  console.log("2:", this.sports); // 농구 - 2번째 호출 시 오류 발생
  console.log("3:", this.music); // undefined
};
window.get(); // function 내부에 this === window
get(); // function 내부에서 this는 window를 참조하지 않아 this.sports 호출 시 오류 발생


let dummy;
