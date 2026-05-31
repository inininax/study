"use strict";
debugger;

class Member {
  constructor(name){
    this.name = name;
  }
  getName() {
    return this.name;
  }
}

class Leader {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
  getName() {
    return this.name;
  }
  getAge() {
    return this.age;
  }
}

let member = new Member("스포츠");
console.log(member.getName());

let leader = new Leader('leader', 100);
console.log(`name: ${leader.getName()}, age: ${leader.getAge()}`);
