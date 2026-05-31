export {};

interface Person {
    name: string;
    age: number;
}

interface Product {
    name: string;
    age: number;
}

const person: Person = {name: 'mike', age: 23}
const product: Product = person; //할당 가능 Person <= Product 이기 때문에 할당 가능