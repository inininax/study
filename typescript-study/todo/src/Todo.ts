import {Priority, PRIORITY_NAME_MAP} from "./type";
import chalk from "chalk";

export default class Todo {
    static nextId: number = 1;

    //private title: string; - 생성자에서 private을 받기 때문에 생략 가능
    constructor(
        private title: string,
        private priority: Priority,
        public id: number = Todo.nextId,
    ) {
        Todo.nextId++;
    }

    toString() {
        return chalk`{blue.bold ${this.id})} 제목: {bold ${this.title}} (우선순위: {${PRIORITY_STYLE_MAP[this.priority]} ${PRIORITY_NAME_MAP[this.priority]}(${this.priority})})`;
    }
}

const PRIORITY_STYLE_MAP: { [K in Priority]: string } = {
    [Priority.High]: 'red.bold',
    [Priority.Medium]: 'grey.bold',
    [Priority.Low]: 'yellow.bold',
};