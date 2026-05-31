export {};

function func1(a: number, b: number | string) {
    const v1: number | string = a;
    // @ts-ignore
    const v2: number = b; // error
}

function func2(a: 1 | 2) {
    // @ts-ignore
    const v1: 1 | 3 = a; // error
    const v2: 1 | 2 | 3 = a;
}