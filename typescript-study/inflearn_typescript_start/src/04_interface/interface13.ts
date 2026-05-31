export {};


interface Person {
    name: string;
    age: number;
}

interface Product {
    name: string;
    price: number;
}

type PP = Person & Product;

const pp: PP = {
    name: 'a',
    age: 23,
    price: 1000,
};