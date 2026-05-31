export {};

interface Person {
    name: string;
    age: number;
}

interface Korean extends Person {
    liveInSeoul: boolean;
}

interface Japanese extends Person {
    liveInTokyo: boolean;
}

const p1: Person = {name: 'a', age: 1}
const p2: Korean = {name: 'a', age: 1, liveInSeoul: false}
const p3: Japanese = {name: 'a', age: 1, liveInTokyo: false}
const arr1 = [p1, p2, p3]; // Person[]
const arr2 = [p2, p3]; // Array<Korean | Japanese>