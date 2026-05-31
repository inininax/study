export {};

type IsString<T> = T extends string ? 'yes' : 'no';
type T1 = IsString<string | number>;
type T2 = IsString<number | IsString<number>>;

type Array2<T> = Array<T>;
type T3 = Array2<string | number>;
// sring[] | number[]