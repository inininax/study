# 타입스크립트 코리아 기초 세미나(inflearn) study
## 원문
- [타입스크립트 코리아 기초 세미나(inflearn)](https://www.inflearn.com/course/%ED%83%80%EC%9E%85%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8-%EC%BD%94%EB%A6%AC%EC%95%84-1705-%EA%B8%B0%EC%B4%88-%EC%84%B8%EB%AF%B8%EB%82%98/dashboard)

## 강의 내용
### Overview
- Compiled language (or transpile)
- Static type checker
- Superset of javascript

### 개발 환경 구축 및 컴파일러 사용
- Install nvm & node
```shell
$ brew install nvm

$ nvm --version
0.38.0

$ nvm install 14.15.5

$ nvm ls
->     v14.15.5 ...

$ nvm current
v14.15.5

$ node -v
v14.15.5

$ npm -v
7.13.0
```

- Install TypeScript
```shell
$ npm install -g typescript
$ tsc -v
Version 4.2.4

$ npm init
...

$ touch dummy.ts
$ tsc dummy.ts
dummy.js 컴파일
```

- Init TypeScript
```shell
$ tsc --init
tsconfig.json 생성

$ tsc
tsconfig.json 설정값을 통해 컴파일
```

- Init tslint
```shell
$ npm i -g tslint (npm i typescript tslint)
$ tslint --init
tslint.json 파일 생성
```

### IDE 활용
- 작성 중

### Compiler Options
- 작성 중

### var, let, const
```typescript
let a: string = 'A';
let b = 'B';
const c: string = 'C';
const d = 'D';
```

### Type assertions, Type alias
- Type assertions
```typescript
let someValue = 'this is a string';
let strLength1: number = (<string>someValue).length;
let strLength2: number = (someValue as string).length;
```

- Type alias
```typescript
type MyStringType = string;
const str = 'world';
let myStr: MyStringType = 'hello';
myStr = str;
```

- Union Type
```typescript
let person: string | number = 0;
person = 'Name';
type StringOrNumber = string | number;
let another: StringOrNumber = 0;
another = 'Anna';
```

- Aliasing Tuple
```typescript
let person: [string, number] = ['Name', 36];
type PersonTuple = [string, number];
let another: PersonTuple = ['Anna', 24];
```

- Interface와의 차이점: 확장 방법의 차이: interface는 extends를 통해 확장 가능, type은 &로 확장
```typescript
// interface
interface PeopleInterface {
    name: string
    age: number
}

interface StudentInterface extends PeopleInterface {
    school: string
}
```
```typescript
// type
type PeopleType = {
    name: string
    age: number
}

type StudentType = PeopleType & {
    school: string
}
```

- Interface와의 차이점: interface는 동일 한 이름으로 추가 정의 시 자동으로 확장되지만 type은 동일한 명으로 확장 불가
```typescript
interface Window {
    title: string
}

interface Window {
    ts: TypeScriptAPI
}

// 같은 interface 명으로 Window를 다시 만든다면, 자동으로 확장이 된다.
const src = 'const a = "Hello World"'
window.ts.transpileModule(src, {})
```
```typescript
type Window = {
    title: string
}

// Error: Duplicate identifier 'Window'. type은 확장 불가
type Window = {
    ts: TypeScriptAPI
}
```

- Interface와의 차이점: interface는 객체에서만 사용 가능

- Interface와의 차이점: computed value의 사용
```typescript
type names = 'firstName' | 'lastName'
type NameTypes = {
    [key in names]: string
}

const yc: NameTypes = {firstName: 'hi', lastName: 'yc'}

interface NameInterface {
    [key in names]: string // error
}
```

- Interface와의 차이점: 선언
```typescript
type Alias = { num: number }

interface InterFace {
    num: number;
}

declare function aliased(arg: Alias);

Alias;

declare function interfaced(arg: InterFace): InterFace;
```

### Interface
- default
```typescript
interface Person {
    [index: string]: string;

    name: string;
    age: number;

    hello?(): void;
}

interface Person2 {
    [index: number]: string;

    hello(): void;
}

const person0: { name: string, age: number } = {
    name: 'Name',
    age: 10
};

const person1: Person = {
    name: 'Name2',
    age: 40
};
person1.anybody = 'Anna';
person1.anybody1 = 'Anna1';
person1.anybody2 = 'Anna2';
person1.anybody3 = 'Anna3';

const person2: Person2 = {
    hello(): void {
        return 'Heelo';
    }
};
person2[0] = 'Hi'
person2[1] = 'Hi1'
person2[2] = 'Hi2'

function hello(p: Person): void {
    console.log(`hello! ${p.name}`);
}

hello(person1);
```

- class implements interface
```typescript
interface IPerson {
    name: string;

    hello(): void;
}

class Person implements IPerson {
    name: string = null;

    constructor(name: string) {
        this.name = name;
    }

    hello(): void {
        console.log(`Hi ${this.name}!`);
    }
}

const person: IPerson = new Person('Name');
person.hello();
```

- interface extends interface
```typescript
interface Person {
    name: string;
    age: number;
}

interface Korean extends Person {
    city: string;
}

const k: Korean = {
    name: 'Name',
    city: 'Seoul'
};
```

- function interface (컴파일 시에만 에러를 체크하기 때문에 런타임과 관련 없이 동작)
```typescript
interface HelloPerson {
    (name: string, age?: number): void;
}

const helloPerson: HelloPerson = function () {
};

helloPerson('Name');
```

- Indexable Types
```typescript
interface StringArray {
    [index: number]: string;
}

const sa: StringArray = [];
sa[0] = '0';
sa[1] = '1';
sa[100] = '100';

interface StringDictionary {
    [index: string]: string;
}

const ad: StringDictionary = {};
ad.hi = 'Hi';
ad.hello = 'Hello';

interface StringArrayDictionary {
    [index: string]: string;

    [index: number]: string;
}

const sad = {};
sad[0] = '0';
sad[100] = '100';
sad.hi = 'hi';
sad.hello = 'hello';
```

### Class
- access modifier: default public
```typescript
class Person {
    name: string;
    age: number;

    constructor(name: string) {
        this.name = name;
        console.log(this.age === undefined); // true
    }
}

const person: Person = new Person('Name');
person.name = 'Name2';
console.log(person);
```
```typescript
class Person {
    private name: string = 'Name';
    protected age: number = null;

    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }

    private hello(): void {
        console.log(this.name, this.age);
    }

    helloworld = (): void => {
        this.hello();
    }
}

class Child extends Person {
    constructor(name: string) {
        super();
        // name...
        console.log(this.age);
    }
}

const person: Person = new Person('Name', 35);
console.log(person);
```
```typescript
class Person {
    // name, age 생략 가능
    constructor(protected name: string, private age: number) {
    }

    hello(): void {
        console.log(this.name, this.age);
    }
}

class Child extends Person {
}

const person: Person = new Person('Name', 36);
person.hello();

const child: Child = new Child('Name', 36);
child.hello();
```

- getter, setter
```typescript
class Person {
    private _name: string;
    private _age: number;

    constructor(name: string, age: number) {
        this._name = name;
        this._age = age;
    }

    get name() { // es6, c#
        return this._name;
    }

    set name(name: string) {
        this._name = name;
    }
}

const person: Person = new Person('Name', 36);
// person._age (X)
console.log(person.name);
person.name = 'Name2';
console.log(person.name);
```

- static properties
```typescript
class Person {
    static HEIGHT: number = 200; // default: public

    constructor(private _name: string, private _age: number) {
    }

    hello(): void {
        console.log(this._name);
    }

    getName(): string {
        return this._name;
    }

    setName(name: string): void {
        this._name = name;
    }
}

const person: Person = new Person('Name', 36);
console.log(Person.HEIGHT); // public static
```

- abstract class
```typescript
abstract class APerson {
    protected _name: string = 'Name';

    abstract setName(name: string): void;
}

class Person extends APerson {
    setName(name: string): void {
        this._name = name;
    }
}

// const person: APerson = new APerson(); (X)
const person: Person = new Person();
```

- singleton
```typescript
class Preference {
    private static instance: Performance = null;

    public static getInstance() {
        if (Performance.instance === null) {
            Performance.instance = new Performance();
        }
        return Preference.instance;
    }

    private constructor() {
    }

    hello() {
    }
}

const p: Performance = Performance.getInstance();
p.hello();
```

```typescript
interface ICar {
    hank(): void;

    accelerate(speed: number): void;

    getSpeed();
}

class Car implements ICar {
    // name: string = null; 생략 가능
    private _speed: number = 0;

    constructor(public name: string) {
    }

    hank(): void {
        console.log('hank');
    }

    accelerate(speed: number) {
        this._speed = speed;
    }

    get spped(): number {
        return this._speed;
    }

    getSpeed() {
        return this._speed;
    }
}

const car: Car = new Car('Benz');
car.hank();
car.accelerate(10);
console.log(car.name);
console.log(car.speed);
console.log(car.getSpeed());
```

### Generic
```typescript
function helloString(message: string): string {
    return message;
}

function helloNumber(message: number): number {
    return message;
}

function helloAny(message: any): any {
    return message;
}

function hello<T>(message: T): T {
    return message;
}

const str: string = hello('string');
const num: number = hello(0);
```
```typescript
function helloArray<T>(messages: T[]): T[] {
    return messages;
}

const arr1: string[] = ['a1', 'b1'];
const arr2: Array<String> = ['a2', 'b2'];
const arr = helloArray(['a3', 'b3']);
console.log(arr1, arr2, arr3)
```
```typescript
type HelloGeneric = <T>(message: T) => T;

const hello: HelloGeneric = <T>(message: T): T => {
    return message;
}

console.log(hello<string>('Hello').length);
```
```typescript
class Person<T> {
    private _name: T;

    constructor(name: T) {
        this._name = name;
    }
}

const name = new Person('name');
const age = new Person(0);
```
```typescript
class Person<T extends string | number> { // union type
    private _name: T;

    constructor(name: T) {
        this._name = name;
    }
}

const name = new Person('name');
const age = new Person(0);
// const age = new Person(false); (X)
```
```typescript
class Person<T, K> {
    private _name: T;
    private _age: K;

    constructor(name: T, age: K) {
        this._name = name;
        this._age = age;
    }
}
```
```typescript
// type lookup system
interface Person {
    name: string;
    age: number;
}

const person: Person = {
    name: 'Name',
    age: 36
};

function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

function setProperty<T, K extends keyof T>(obj: T, key: K, value: T[K]): void {
    obj[key] = value;
}

type Test = keyof Person; // Initial type: "name" | "age"

console.log(getProperty(person, 'name'));
setProperty(person, 'name', 'Anna');
console.log(getProperty(person, 'name'));
```

### Iterator
- Array, Map, Set, String, Int32Array, Uint32Array에는 내장된 구현체가 존재

- 이터레이터를 통해 이터러블한 객체의 Symbol.iterator 함수를 호출한다.
```typescript
// lib.es6.d.ts
interface IteratorResult<T> {
    done: boolean;
    value: T;
}

interface Iterator<T> {
    next(value?: any): IteratorResult<T>;

    return?(value?: any): IteratorResult<T>;

    throw?(a?: any): IteratorResult<T>;
}

interface Iterable<T> {
    [Symbol.iterator](): Iterator<T>;
}

interface IterableIterator<T> extends Iterator<T> {
    [Symbol.iterator](): IterableIterator<T>;
}
```
```typescript
class CustomIterable implements Iterable<string> {
    private _array: Array<string> = ['first', 'secode'];

    [Symbol.iterator](): Iterator<string> {
        var nextIndex = 0;
        return {
            next: () => {
                return {
                    value: this._array[nextIndex++],
                    done: nextIndex < this._array.length
                };
            }
        };
    }
}

const cIterable = new CustomIterable();
for (const item of cIterable) {
    console.log(item);
}
```

### Decorator
- class, method, property, parameter decorator

- tsconfig.json - experimentalDecorators: true
```json
{
  "compilerOptions": {
    "target": "ES5",
    "experimentalDecorators": true
  }
}
```

- class decorator
```typescript
function hello(constructorFn: Function) {
    console.log(constructorFn);
}

@hello
class Person {
}
```
```typescript
function hello(constructorFn: Function) {
    console.log(constructorFn);
}

function helloFactory(show: boolean) {
    return show ? hello : null;
}

@helloFactory(true)
class Person {
    constructor(props) {
        console.log('new Person()');
    }
}

new Person();
```
```typescript
function hello(constructorFn: Function) {
    constructorFn.prototype.hello = () => {
        console.log('Hello');
    }
}

@hello
class Person {
}

const p = new Person();
// p.hello(); (X)
(<any>p).hello(); // 
```

- method decorator
```typescript
function editable(canBeEditable: boolean) {
    return function (target: any, propName: string, description: PropertyDescriptor) {
        console.log(target); // Person {}
        console.log(propName); // hello
        console.log(description); // {value: [Function: hello], writable: true, enumerable: false, configurable: true}

        description.writable = canBeEditable;
    };
}

class Person {
    constructor() {
        console.log('new Person()');
    }

    @editable(true)
    hello() {
        console.log('hello');
    }
}

const p = new Person();
p.hello();

// true 일 경우, false 일 경우 재정의 불가
p.hello = function () {
    console.log('editable');
};
```

- property decorator
```typescript
function writable(canBeWritable: boolean) {
    return function (target: any, propName: string): any {
        console.log(target); // Person {}
        console.log(propName); // name

        return {
            writable: canBeWritable
        };
    }
}

class Person {
    @writable(true)
    name: string = 'Name';

    constructor() {
        console.log('new Person()');
    }
}

const p = new Person();
console.log(p.name);
```

- parameter decorator
```typescript
function printInfo(target: any, methodName: string, paramIndex: number) {
    console.log(target); // Person {}
    console.log(methodName); // hello
    console.log(paramIndex); // 0
}

class Person {
    private _name: string;
    private _age: number;

    constructor(name: string, @printInfo age: number) {
        this._name = name;
        this._age = age;
    }

    hello(@printInfo message: string) {
        console.log(`message ${message}`);
    }
}

const p = new Person('Name', 36);
```

### Type Inference
- 타입 추론: 기본적으로 타입을 명시적으로 쓰지 않을 때 추론하는 방법에 대한 규칙
- let은 기본적으로 우리가 아는 기본 자료형으로 추론
- const는 literal 타입으로 추론
    - 오브젝트 타입을 타입을 쓰지 않으면, 프로퍼티는 let 처럼 추촌
        - const person = {name: 'Name', age: 36}; 면
        - person => {name: string, age: number}로 추론
- structuring, destructuring
```typescript
const array1 = []; // any[] 으로 추론
const array2 = ['a', 'b', 'c']; // string[] 으로 추론
const array3 = ['a', 1, false]; // union type -> (string | number | bollean)[] 으로 추론
```
```typescript
class Animal {
    name: string;
}
class Dog extends Animal {
    dog: string;
}
class Cat extends Animal {
    cat: string;
}
const array4 = [new Dog(), new Cat()]; // union type -> (Dog | cat)[] 으로 추론
```
```typescript
function hello(message: string | number) { // literal type -> 'world' | 0
    if (message === 'world') {
        return 'world';
    } else {
        return 0;
    }
}
```

- union type, type guard
```typescript
interface Person {
    name: string;
    age: number;
}
interface Car {
    brand: string;
    wheel: number;
}
function isPerson(arg: any): arg is Person { // type guard
    return arg.name !== undefined;
}
function hello(arg: Person | Car) {
    if (isPerson(arg)) {
        console.log(arg.name);
    } else {
        console.log(arg.brand);
    }
}
```