export {};

/*
    Partial<T>
    Readonly<T>
    Record<K,T>
    Pick<T,K>
    Omit<T,K>
    Exclude<T,U>
    Extract<T,U>
    NonNullable<T>
    Parameters<T>
    ConstructorParameters<T>
    ReturnType<T>
    InstanceType<T>
    Required<T>
    ThisParameterType
    OmitThisParameter
    ThisType<T>
*/

// 샘플
interface Person {
    name: string;
    age: number;
    language: string;
}

// optional로 속성 변경
type Partial<T> = { [P in keyof T]?: T[P]; }
type PartialSample = Partial<Person>; // {name?: string, age?: number, language?: string}

// readonly로 속성 변경
type Readonly<T> = { readonly [P in keyof T]: T[P]; }
type ReadonlySample = Readonly<Person>; // {readonly name: string, readonly age: number, readonly language: string}

// T의 일부 property만 가져옴
type Pick<T, K extends keyof T> = { [P in K]: T[P]; }
type PickSample = Pick<Person, 'name' | 'age'>; // {name: string; age: number;}

// 입력 받은 property name에 T를 할당하여 새로운 타입을 생성
type Record<K extends keyof any, T> = { [P in K]: T; }
type RecordSample1 = Record<'p1' | 'p2', Person>;
type RecordSample2 = Record<'p1' | 'p2', number>;
const record: RecordSample1 = {
    p1: {name: '', age: 0, language: ''},
    p2: {name: '', age: 0, language: ''}
}

// Exclude<T, U> -- U에 할당할 수 있는 타입은 T에서 제외. - 차집합
// type Exclude<T, U> = T extends U ? never : T;
type ExcludeSample1 = Exclude<1 | 3 | 5 | 7, 1 | 5 | 9>; // 3 | 7
type ExcludeSample2 = Exclude<string | number | (() => void), Function>; // string | number

// Extract<T, U> -- U에 할당할 수 있는 타입을 T에서 추출 - 교집합
// type Exract<T, U> = T extends U ? T : never;
type ExtractSample = Extract<1 | 3 | 5 | 7, 1 | 5 | 9>; // 1 | 5

// ReturnType<T> -- 함수 타입의 반환 타입을 얻기.
// type ReturnType<T> = T extends (...args: any[]) => infer R ? R : any;
type ReturnTypeSample = ReturnType<() => string>; // string

// Unpacked

// Omit -- type Omit<T, U extends keyof T> = Pick<T, Exclude<keyof T, U>>;
type OmitExample = Omit<Person, 'nation' | 'age'>; // {name: string, language: string}, Person에서 nation, age를 제거한다는 뜻

// Overwrite
type Overwrite<T, U> = { [P in Exclude<keyof T, keyof U>]: T[P] } & U;
