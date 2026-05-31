export {};

// Typescript 내장 타입

// infer 키워드를 통해 함수의 반환 타입을 R에 담음
// type ReturnType<T> = T extends (...args: any[]) => infer R ? R : any;
type T1 = ReturnType<() => string>;

function f1(s: string): number {
    return s.length;
}

type T2 = ReturnType<typeof f1>;