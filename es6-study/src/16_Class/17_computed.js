"use strict";
debugger;

let type = "Type";
class Sports {
  static ["get" + type](kind) {
    return kind ? "Sports" : "Music";
  }
}

console.log( Sports.getType() );