export {};

// discriminated union : 식별 가능

interface Person {
    type: 'a';
    name: string;
    age: number;
}

interface Product {
    type: 'b';
    name: string;
    price: number;
}

interface Product2 {
    type: 'c';
    name: string;
    price: number;
}

function print(value: Person | Product | Product2) {
    switch (value.type) {
        case 'a':
            console.log(value.age);
            break;
        case 'b':
            console.log(value.price);
            break;
        case 'c':
            console.log(value.price);
            break;
    }
}