interface SearchFunc {
    (source: string, subString: string): boolean;
}

const mySearch: SearchFunc = (src: string, sub: string) => {
    let result = src.search(sub);
    return result > -1;
};