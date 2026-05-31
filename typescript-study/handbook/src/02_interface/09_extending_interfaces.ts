interface Shape {
    color: string;
}

interface Square extends Shape {
    sideLength: number;
}

let square = {} as Square;
square.color = 'blue';
square.sideLength = 10;

// ---

interface PenStroke {
    penWidth: number;
}

interface PenSquare extends Shape, PenStroke {
    sideLength: number;
}

let penSquare = {} as PenSquare;
penSquare.color = 'blue';
penSquare.sideLength = 10;
penSquare.penWidth = 5.0;
