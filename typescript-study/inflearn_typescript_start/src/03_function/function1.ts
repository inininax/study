export {};

function getText(name: string, age: number): string {
    const nameText = name.substring(0, 10);
    const ageText = age >= 35 ? 'senior' : 'junior';
    return `name: ${nameText}, age: ${ageText}`;
}

const v1: string = getText('mike', 123);
// error - const v2: string = getText('mike', '123');
// error - const v3: number = getText('mike', '123');