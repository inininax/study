// angle-bracket
let someValue: any = 'angle bracket';
let strLength: number = (<string>someValue).length;
console.log(someValue, strLength);

// as
let someValue2: any = 'as';
let strLength2: number = (someValue2 as string).length;
console.log(someValue2, strLength2);