export {};

// this type 정의

function getParam(this: string, index: number): string {
    const params = this.split(',');
    if (index < 0 || params.length <= index) {
        return '';
    }
    return this.split(',')[index];
}

interface String {
    getParam(this: string, index: number): string;
}

// @ts-ignore
String.prototype.getParam = getParam;

// @ts-ignore
console.log('adfa, 123, ok'.getParam(1));