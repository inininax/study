export {};

class Person {
    private _name: string = '';

    get name(): string {
        return '';
    }

    set name(newName: string) {
        if (newName.length > 10) {
            throw new Error(`최대 길이 10`);
        }
        this._name = newName;
    }
}

const person = new Person();
console.log(person.name);
person.name = 'Abc';
console.log(person.name);