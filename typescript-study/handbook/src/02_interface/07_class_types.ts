// Implementing an interface
interface ClockInterface {
    currentTime: Date;

    setTime(d: Date): void;
}

class Clock implements ClockInterface {
    currentTime: Date = new Date();

    constructor(h: number, m: number) {
    }

    setTime(d: Date) {
        this.currentTime = d;
    }
}

let clock: ClockInterface = new Clock(10, 10);
console.log(clock);