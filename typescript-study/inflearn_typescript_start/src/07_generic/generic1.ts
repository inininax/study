export {};

function makeNumberArray(defaultValue: number, size: number): number[] {
    const arr: number[] = [];
    for (let i = 0; i < size; i++) {
        arr.push(defaultValue);
    }
    return arr;
}

function makeStringArray(defaultValue: string, size: number): string[] {
    const arr: string[] = [];
    for (let i = 0; i < size; i++) {
        arr.push(defaultValue);
    }
    return arr;
}