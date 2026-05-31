"use strict";
debugger;

class Leader {
  getName() {
    return "leader";
  }
}

let Member = class {
  getName() {
    return "이름";
  }
};

let leader = new Leader();
console.log(leader.getName());

let member = new Member();
console.log(member.getName());
