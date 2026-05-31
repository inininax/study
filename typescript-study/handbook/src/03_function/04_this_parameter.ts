interface Card_param {
    suit: string;
    card: number;
}

interface Deck_param {
    suits: string[];
    cards: number[];

    createCardPicker(this: Deck_param): () => Card_param;
}

let deck_param: Deck_param = {
    suits: ["hearts", "spades", "clubs", "diamonds"],
    cards: Array(52),
    // NOTE: 아래 함수는 이제 callee가 반드시 Deck 타입이어야 함을 명시적으로 지정합니다.
    createCardPicker: function (this: Deck_param) {
        return () => {
            let pickedCard = Math.floor(Math.random() * 52);
            let pickedSuit = Math.floor(pickedCard / 13);

            return {suit: this.suits[pickedSuit], card: pickedCard % 13};
        }
    }
}

let cardPicker_param = deck_param.createCardPicker();
let pickedCard_param = cardPicker_param();

alert("card: " + pickedCard_param.card + " of " + pickedCard_param.suit);