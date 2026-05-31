export {};

function func1(a = 'abc', b = 10) {
    return `${a} ${b}`;
}

// func1(3, 5); // error
// const v1: number = func1('a', 1); // error

function func2(value: number) {
    if (value < 10) {
        return value;
    }
    return `${value} is too big`;
}

const v2: string | number = func2(20);

