export {};

// naver는 property를 제거
type StringPropertyNames<T> = {
    [K in keyof T]: T[K] extends string ? K : never; // mapped type
}[keyof T]; // 값의 type을 뽑아냄

interface Person {
    name: string;
    age: number;
    nation: string;
}

type T1 = StringPropertyNames<Person>; // "nation" | "name"

// interface Person2 {
//     name: 'name';
//     age: never;
//     nation: 'nation';
// }

type StringProperties<T> = Pick<T, StringPropertyNames<T>>;
type T2 = StringProperties<Person>; // {name: string, nation: string}

