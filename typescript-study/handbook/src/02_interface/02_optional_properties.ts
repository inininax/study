interface SquareConfig {
    color?: string;
    width?: number;
}

const createSquare = (config: SquareConfig): { color: string; area: number } => {
    let square = {color: 'white', area: 100};
    if (config.color) square.color = config.color;
    if (config.width) square.area = config.width ** 2; // Math.pow(config.width, 2)
    return square;
};

let mySquare = createSquare({color: 'black'});
console.log(mySquare);