"use strict";
debugger;

class Sports {
  constructor(member){
    console.log('Sports constructor');
    this.member = member;
  }
  getMember(){
    return this.member;
  }
};

class Soccer extends Sports {
  // constructor(member){
  //   console.log(member);
  // }
  setGround(ground){
    this.ground = ground;
  }
  getGround(){
    return this.ground;
  }
};

let obj = new Soccer(11);
console.log(obj.getMember());

obj.setGround('grass');
console.log(obj.getGround());
