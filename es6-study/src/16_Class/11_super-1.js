"use strict";
debugger;

class Sports {
  constructor(){
    console.log('Sports constructor'); // 1
  }
  setGround(ground){
    console.log('Sports.setGround', ground); // 3, 123
    this.ground = ground;
  }
};

class Soccer extends Sports {
  // constructor(){
  //   console.log('Soccer constructor');
  // }
  setGround(ground){
    console.log('Soccer.setGround', ground); // 2
    super.setGround(123);
    this.ground = ground;
  }
  getGround(){
    return this.ground;
  }
};

let soccer = new Soccer(11);
soccer.setGround("상암구장");
console.log('soccer.ground', soccer.ground);
console.log('soccer.getGround()', soccer.getGround());


let dummy;
