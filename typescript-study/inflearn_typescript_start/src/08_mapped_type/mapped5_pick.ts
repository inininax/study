export {};

// Typescript 내장 타입
// type Pick<T, K extends keyof T> = { [P in K]: T[P] };

interface Person {
    name: string;
    age: number;
    language: string;
}

type T1 = Pick<Person, 'name' | 'age'>;

const v1: T1 = {
    name: '',
    //language: '',
    age: 0
};