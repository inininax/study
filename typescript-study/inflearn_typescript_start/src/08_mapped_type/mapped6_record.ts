export {};

interface Person {
    name: string;
    age: number;
}

// Typescript 내장 타입
// type Record<K extends string, T> = { [P in K]: T };
type T1 = Record<'p1' | 'p2', Person>;
type T2 = Record<'p1' | 'p2', number>;

const v1: T1 = {
    p1: {name: '', age: 0},
    p2: {name: '', age: 0}
}