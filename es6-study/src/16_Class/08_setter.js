"use strict";
debugger;

class Member {
  set setName(name) {
    this.name = name;
  }
  get getName() {
    return this.name;
  }

  set setName2(name) {
    this.name2 = name;
  }
  get getName2() {
    return this.name2;
  }
};

let member = new Member();

member.setName = "이름123";
console.log(member.getName);

member.setName2 = 'all name';
console.log(member.getName2);
