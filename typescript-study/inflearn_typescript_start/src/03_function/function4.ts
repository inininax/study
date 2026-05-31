export {};

function getText(name: string, age: number, language = 'korean'): string {
    const nameText = name.substring(0, 10);
    const ageText = age >= 35 ? 'senior' : 'junior';
    const languageText = language.substring(0, 10);
    return `name: ${nameText}, age: ${ageText}, language: ${languageText}`;
}

const v1: string = getText('mike', 123);
const v2: string = getText('mike', 123, '123');
// error - const v2: string = getText('mike', '123');
// error - const v3: number = getText('mike', '123');