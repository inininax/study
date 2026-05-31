export {};

// never는 type을 제거함
type T1 = number | string | never;

// Typescript 내장 타입
// type Exclude<T, U> = T extends U ? never : T;
type T2 = Exclude<1 | 3 | 5 | 7, 1 | 5 | 9>; // 3 | 7
type T3 = Exclude<string | number | (() => void), Function>; // string | number

// Typescript 내장 타입
// type Exract<T, U> = T extends U ? T : never;
type T4 = Extract<1 | 3 | 5 | 7, 1 | 5 | 9>; // 1 | 5