"use strict";
debugger;

class Member{
  setName(name) {
    this.name = name;
  }
  getName() {
    return this.name;
  }
};

let member = new Member();
try {
  console.log(member.getTitle());
} catch (e) {
  console.error(e);
}

Member.prototype.getTitle = function(){
  return 'title';
};
console.log(member.getTitle());

console.log(typeof Member);
let dummy;
