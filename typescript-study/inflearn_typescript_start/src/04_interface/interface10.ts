export {};

interface Person {
    name: string;
    age: number;
}

interface Korean extends Person {
    isYoungerThan(age: number): boolean;
}

class SomePerson implements Korean {
    name: string;
    age: number;

    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }

    isYoungerThan(age: number): boolean {
        return this.age < age;
    }
}