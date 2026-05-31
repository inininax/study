export {};

// 가능하면 as를 사용하지 말 것

// 값의 영역에서의 typeof는 Type 내에서 사용하던 typeof와 다름!!

function print(value: number | string): void {
    if (typeof value === 'number') {
        //console.log((value as number).toFixed(2)); // as 를 통한 강제 타입 지정
        console.log(value.toFixed(2));
        return;
    }
    //console.log((value as string).trim());
    console.log(value.trim());
}