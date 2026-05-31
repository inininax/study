interface SquareConfig {
    color?: string;
    width?: number;

    [propName: string]: any;
}

const createSquare2 = (config: SquareConfig): { color: string, area: number } => {
    let square = {color: 'white', area: 100};
    if (config.color) square.color = config.color;
    if (config.width) square.area = config.width ** 2; // Math.pow(config.width, 2)
    return square;
}

let mySquare2 = createSquare2({color: 'red', width: 10});
console.log(mySquare2);

let mySquare3 = createSquare2({opacity: 0.5, width: 10} as SquareConfig);
console.log(mySquare3);