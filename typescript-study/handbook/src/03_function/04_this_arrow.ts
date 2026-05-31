let deck_arrow = {
    suits: ["hearts", "spades", "clubs", "diamonds"],
    cards: Array(52),
    createCardPicker: function () {
        // NOTE: 아랫줄은 화살표 함수로써, 'this'를 이곳에서 캡처할 수 있도록 합니다
        return () => {
            let pickedCard = Math.floor(Math.random() * 52);
            let pickedSuit = Math.floor(pickedCard / 13);

            return {suit: this.suits[pickedSuit], card: pickedCard % 13};
        };
    }
};

let cardPicker_arrow = deck_arrow.createCardPicker();
let pickedCard_arrow = cardPicker_arrow();

alert("card: " + pickedCard_arrow.card + " of " + pickedCard_arrow.suit);