/* (js)

function Counter() {
    this.value = 0;
    this.add = amount => {
        this.value += amount;
        console.log(this === global);
    }
}


const counter = new Counter();
console.log(counter.value);
counter.add(5);
console.log(counter.value);
const add = counter.add;
add(5);
console.log(counter.value);

console.log('-------------------------');

function Counter2() {
    this.value = 0;
    this.add = function (amount) {
        this.value += amount;
        console.log(this === global);
    }
}


const counter2 = new Counter2();
console.log(counter2.value);
counter2.add(5);
console.log(counter2.value);
const add2 = counter2.add;
add2(5);
console.log(counter2.value); //5


console.log('-------------------------');



const counter3 = {
    value: 0,
    //add: function (amount) {
    add: (amount) => {
        this.value += amount;
    }
};
console.log(counter3.value);
counter3.add(5);
console.log(counter3.value);
const add3 = counter3.add;
add3(5);
console.log(counter3.value);
*/