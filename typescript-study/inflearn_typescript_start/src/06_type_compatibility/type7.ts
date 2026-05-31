export {};

interface Person {
    name: string;
    age: number;
    gender: string;
}

interface Product {
    name: string;
    age: number | string;
}

const person: Person = {
    name: 'mike',
    age: 23,
    gender: 'male'
}

const product: Product = person; //할당 가능 Product에게 필요한 모든 값을 Person이 가지고 있기 때문에 할당 가능