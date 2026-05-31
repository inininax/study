export {};

class Person {
    name: string;
    age: number;

    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }
}

class Product {
    name: string;
    price: number;

    constructor(name: string, price: number) {
        this.name = name;
        this.price = price;
    }
}

function print(value: Person | Product) {
    console.log(value.name);
    if (value instanceof Person) {
        console.log(value.age);
        return;
    }
    console.log(value.price);
}