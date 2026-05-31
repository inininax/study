export {};

// void , never

function f1(): void {
}

function f2(): never {
    throw new Error('Never');
}

function f3(): never {
    while (true) {
    }
}