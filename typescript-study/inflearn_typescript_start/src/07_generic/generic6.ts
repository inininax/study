export {};

interface Person {
    name: string;
    age: number;
}

interface Korean extends Person {
    liveInSeoul: boolean;
}

interface Product {
    name: string;
    price: number;
}

function swapProperty<T extends Person, K extends keyof Person>(p1: T, p2: T, key: K): void {
    const temp = p1[key];
    p1[key] = p2[key];
    p2[key] = temp;
}

const p1: Korean = {
    name: '1 name',
    age: 1,
    liveInSeoul: false
}

const p2: Korean = {
    name: '2 name',
    age: 2,
    liveInSeoul: true
}

swapProperty(p1, p2, 'name');
swapProperty(p1, p2, 'age');

console.log(p1, p2);

const pd1: Product = {
    name: '아파트',
    price: 99999999999
}

const pd2: Product = {
    name: '아파트2',
    price: 9999999999999
}

// 타입 정의에 맞지 않기 때문에 에러 발생
// swapProperty(pd1, pd2, 'name'); // error

