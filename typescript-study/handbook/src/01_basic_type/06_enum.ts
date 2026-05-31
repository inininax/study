enum Color {Red, Blue, Green}

let c: Color = Color.Blue;
console.log(c);

enum Color2 {Red = 1, Blue, Green}

let c2: Color2 = Color2.Blue;
console.log(c2);

enum Color3 {Red = 1, Blue = 4, Green = 100}

let c3: Color3 = Color3.Blue;
let colorName3: string = Color3[100];
console.log(c3);
console.log(colorName3);