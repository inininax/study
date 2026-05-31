export {};

function getText(name: string, ...rest: number[]): string {
    console.log(name);
    console.log(rest);
    return '';
}

console.log(getText('mike', 1, 2, 3, 4, 5))