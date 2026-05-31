"use strict";
debugger;

try {
  let result = Member;
} catch (e) {
  console.log('호이스팅 불가', e);
}

class Member {
  static getMember() {
    return "member";
  }
}

console.log( Member.getMember() );
