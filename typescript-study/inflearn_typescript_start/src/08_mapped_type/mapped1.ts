export {};

// mapped type : optional, readonly 등으로 변경해 주는 역할
/*
    Partial
    Readonly
    Pick
    Record
*/

interface Person {
    name: string;
    age: number;
}

interface PersonOptional {
    name?: string;
    age?: number;
}

interface PersonReadOnly {
    readonly name: string;
    readonly age: number;
}