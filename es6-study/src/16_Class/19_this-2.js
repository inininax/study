"use strict";
debugger;

// class Sports{
//   constructor(){
//     console.log(Sports.getGround());
//     console.log(this.constructor.getGround());
//   }
//   static getGround(){
//     return "상암구장";
//   }
// };
// let obj = new Sports();

class Sports {
  constructor() {
    console.log( Sports.getGround() );
    console.log( this.constructor.getGround() );
    // console.log( this.getGround() );
  }
  static getGround() {
    return "잠실";
  }
}

let sports = new Sports();
