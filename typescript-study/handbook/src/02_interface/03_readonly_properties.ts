interface Point {
    readonly x: number;
    readonly y: number;
}

let p1: Point = {x: 10, y: 20};
console.log(p1);
// p1.x = 200; (X)

// ---

let a: number[] = [1, 2, 3, 4];
let ro: ReadonlyArray<number> = a;
console.log(a, ro);
// ro[0] = 12; (X)
// ro.push(5); (X)
// ro.length = 100; (X)
// a = ro; (X)

// ---

a = ro as number[];
console.log(a, ro);