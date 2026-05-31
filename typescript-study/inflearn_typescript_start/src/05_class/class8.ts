export {};

class Person {
    //parameter에 public 사용 시 자동으로 맴버 변수로 할당 및 값 바인딩 처리 코드 생략 가능
    constructor(public name: string, public age: number) {
    }
}

const person = new Person('홍길동', 99);
console.log(person.name, person.age); // 홍길동, 99