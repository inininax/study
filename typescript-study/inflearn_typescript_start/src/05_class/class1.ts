export {}

class Person {
    name: string;
    age: number = 0;

    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }

    sayHello() {
        console.log('Say Hello!');
    }
}

class Programmer extends Person {
    fixBug() {
        console.log('버그 수정 완료!');
    }
}

const person = new Person('lks', 36);
person.sayHello();

const programmer = new Programmer('lks', 36);
programmer.sayHello();
programmer.fixBug();

