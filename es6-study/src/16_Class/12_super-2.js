"use strict";
debugger;

class Sports {
  constructor(member){
    this.member = member;
    console.log(this.member); // 1
  }
};

class Soccer extends Sports {
  constructor(member){
    super(member);
    this.member = 456;
    console.log(this.member); // 2
  }
};

class BasketBall extends Sports {
}

class SuperBowl extends Sports {
  constructor() {
    super('super bowl');
  }
}

let obj = new Soccer(123); // 123, 456
let basketBall = new BasketBall(); // undefined
let superBowl = new SuperBowl(); // super bowl
