interface StringArray {
    [index: number]: string;
}

let myArray: StringArray = ['bob', 'fred'];
let myStr: string = myArray[0];

console.log(myArray, myStr);

// ---

class Animal {
    name: string;

    constructor(name: string) {
        this.name = name;
    }
}

class Dog extends Animal {
    breed: string;

    constructor(name: string, breed: string) {
        super(name);
        this.breed = breed;
    }
}

let dog: Dog = new Dog('mark', 'Deutscher Schäferhund');
console.log(dog.name, dog.breed);

let dog2: Animal = dog;
console.log(dog2.name);

// interface NotOkay {      error (X)
//     [x: number]: Animal;
//     [x: string]: Dog;
// }

interface NumberDictionary {
    [index: string]: number | string;

    length: number;
    name: string;
}

let numberDictionary: NumberDictionary = {
    length: 2,
    name: 'dummy'
};
numberDictionary.hi = 0;
numberDictionary.hello = 'hello';
console.log(numberDictionary);

// ---

interface ReadonlyStringArray {
    readonly [index: number]: string;
}

let readonlyStringArray: ReadonlyStringArray = ['Alice', 'Bob'];
console.log(readonlyStringArray);
// readonlyStringArray[2] (X)

