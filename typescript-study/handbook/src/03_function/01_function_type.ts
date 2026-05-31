// Typing the function
function add(x: number, y: number): number {
    return x + y;
}

let myAdd = function (x: number, y: number): number {
    return x + y;
};

// Writing the function type
let myAdd2: (x: number, y: number) => number =
    function (x: number, y: number): number {
        return x + y;
    };

let myAdd3: (baseValue: number, increment: number) => number =
    function (x: number, y: number): number {
        return x + y;
    };

// Inferring the types
let myAdd4 = (x: number, y: number): number => {
    return x + y;
};

let myAdd5: (baseValue: number, increment: number) => number =
    function (x, y) {
        return x + y;
    };
