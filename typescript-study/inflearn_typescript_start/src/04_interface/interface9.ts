export {};

interface GetText {
    (name: string, age: number): string;

    totalCall?: number;
}

const getText: GetText = function (name, age) {
    if (getText.totalCall !== undefined) {
        getText.totalCall += 1;
        console.log(`getText.totalCall: ${getText.totalCall}`);
    }
    return '';
}

getText.totalCall = 0;
getText('', 0);
getText('', 0);