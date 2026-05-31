export {};


class Stack<D> {
    private items: D[] = [];

    push(item: D) {
        this.items.push(item);
    }

    pop() {
        return this.items.pop();
    }
}

const numberStack = new Stack<number>();
numberStack.push(10);
const v1 = numberStack.pop();

const stringStack = new Stack<string>();
stringStack.push('10');
const v2 = stringStack.pop();

let myStack = new Stack<number>();
myStack = numberStack;
// myStack = stringStack; // error
