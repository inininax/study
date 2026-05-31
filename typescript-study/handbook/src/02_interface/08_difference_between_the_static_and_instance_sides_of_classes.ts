interface DiffClockInterface {
    tick(): void;
}

interface DiffClockConstructor {
    new(hour: number, minute: number): DiffClockInterface;
}

const createClock = (clock: DiffClockConstructor, hour: number, minute: number): DiffClockInterface => {
    return new clock(hour, minute)
};

class DigitalClock implements DiffClockInterface {
    constructor(h: number, m: number) {
    }

    tick() {
        console.log('digital clock');
    }
}

class AnalogClock implements DiffClockInterface {
    constructor(h: number, m: number) {
    }

    tick() {
        console.log('analog clock');
    }
}

let digitalClock: DiffClockInterface = createClock(DigitalClock, 12, 17);
let analogClock: DiffClockInterface = createClock(AnalogClock, 7, 50);

// ---

/*
interface ClockConstructor {
  new (hour: number, minute: number);
}

interface ClockInterface {
  tick();
}

const Clock: ClockConstructor = class Clock implements ClockInterface {
  constructor(h: number, m: number) {}
  tick() {
      console.log("beep beep");
  }
}
*/