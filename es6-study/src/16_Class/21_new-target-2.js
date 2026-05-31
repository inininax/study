"use strict";
debugger;

// class Sports {
//   constructor(){
//     console.log("Sports:", new.target.name);
//   }
// };
// class Soccer extends Sports {
//   constructor(){
//     super();
//       console.log("Soccer:", new.target.name);
//   }
// };
// let sportsObj = new Sports();
// let soccerObj = new Soccer();

class Sports {
  constructor() {
    console.log('sports', new.target.name);
  }
}

class Soccer extends Sports {
  constructor() {
    super();
    console.log('soccer', new.target.name);
  }
}

let sports = new Sports();
console.log('-------------------');
let soccer = new Soccer();