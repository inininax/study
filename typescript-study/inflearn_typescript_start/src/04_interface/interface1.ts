export {};

interface Person {
    name: string;
    age: number;

    [key: string]: string | number; //index type - key 값이 string일 경우 허용
}

interface Person2 {
    name: string;
    age?: number;
}

interface Person3 {
    name: string;
    age: number | undefined;
}

interface Person4 {
    name: string;
    readonly age: number;
}

const p0101: Person = {
    name: '',
    age: 23,
    birth: 'a'
};
// const p2: Person = {name: '', age: '23'};

const p0201: Person2 = {name: '', age: 23};
const p0202: Person2 = {name: ''};

const p0301: Person3 = {name: '', age: 23};
// const p0302: Person3 = {name: ''};

const p0401: Person4 = {name: '', age: 23};
// p0401.age = 30;

