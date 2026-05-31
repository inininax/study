export {};

interface Param {
    name: string;
    age?: number;
    language?: string;
}

function getText({name, age = 15, language,}: Param): string {
    return '';
}