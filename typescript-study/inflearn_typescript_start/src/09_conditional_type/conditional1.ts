export {};

// T extends U ? X : Y

type IsStringType<T> = T extends string ? 'yes' : 'no';
type T1 = IsStringType<string>;
type T2 = IsStringType<number>;

const v1: T1 = 'yes';
const v2: T2 = 'no';