let notSure: any = 4;

console.log(notSure);
notSure.ifItExists();
notSure.toFixed();

notSure = 'string';
console.log(notSure);

notSure = false;
console.log(notSure);

let anyList: any[] = [1, true, 'free'];
anyList[1] = 100;

console.log(anyList[1]);