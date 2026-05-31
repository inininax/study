export {};

// type Exclude<T,U>            - Exclude from T those types that are assignable to U
// => T extends U ? never : T

// Exclude<keyof T, U> -> T의 키들 중 U에 속한 것을 제거

// type Pick<T,K>               - From T, pick a set of properties whose keys are in the union K
// => {[P in K]: T[P]}

type Omit<T, U extends keyof T> = Pick<T, Exclude<keyof T, U>>;

interface Person {
    name: string;
    age: number;
    nation: string;
}

// Person에서 nation, age를 제거
type T1 = Omit<Person, 'nation' | 'age'>;