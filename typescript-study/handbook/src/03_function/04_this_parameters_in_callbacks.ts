/*
    interface UIElement {
        addClickListener(onclick: (this: void, e: Event) => void): void;
    }

    class Handler {
        info: string;
        onClickBad(this: Handler, e: Event) {
            // 이런, `this`가 여기서 쓰이는군요. 이 콜백을 쓰면 런타임에서 충돌을 일으키겠군요
            this.info = e.message;
        }
    }
    let h = new Handler();
    uiElement.addClickListener(h.onClickBad); // 오류!
*/

/*
    class Handler {
        info: string;
        onClickGood(this: void, e: Event) {
            // void 타입이기 때문에 this는 이곳에서 쓸 수 없습니다!
            console.log('clicked!');
        }
    }
    let h = new Handler();
    uiElement.addClickListener(h.onClickGood);
*/

/*
    class Handler {
        info: string;
        onClickGood(this: void, e: Event) {
            // void 타입이기 때문에 this는 이곳에서 쓸 수 없습니다!
            console.log('clicked!');
        }
    }
    let h = new Handler();
    uiElement.addClickListener(h.onClickGood);
*/

/*
    class Handler {
        info: string;
        onClickGood = (e: Event) => {
            this.info = e.message;
        }
    }
*/
