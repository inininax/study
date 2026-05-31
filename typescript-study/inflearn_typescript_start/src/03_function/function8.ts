export {};

interface Object {
    getShortKeys(this: object): string[];
}

// @ts-ignore
Object.prototype.getShortKeys = function () {
    return Object.keys(this).filter(key => key.length <= 3);
};

const obj = {
    a: 1,
    bb: 2,
    ccc: 3,
    dddd: 4
};
// @ts-ignore
console.log(obj.getShortKeys());