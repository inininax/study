export {};

interface Person {
    name: string;
    age: number;
}

interface Product {
    name: string;
    price: number;
}

// interface는 컴파일 시 제거되기 때문에 오류 발생
/*
function print(value: Person | Product) {
    console.log(value.name);
    if (value instanceof Person) {
        console.log(value.age);
        return;
    }
    console.log(value.price);
}
*/