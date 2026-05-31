interface Counter {
    (start: number): string;
    interval: number;
    reset(): void;
}

const getCounter = (): Counter => {
    let counter = (function (start: number) {}) as Counter;
    counter.interval = 123;
    counter.reset = () => {};
    return counter;
};

let counter = getCounter();
counter(10);
counter.reset();
counter.interval = 5.0;

console.log(counter);