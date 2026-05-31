export {};

// enum string 할당 시 단방향 매핑

// const enum 사용 시 파일 생성 안됨

const enum Language {
    Koran = 'ko',
    English = 'en',
    Japanese = 'jp'
}

console.log(Language.Koran);
console.log(Language.Japanese);
console.log(Language.English);