# learn babel + webpack
https://ko.wikipedia.org/wiki/ECMA%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8<br>
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_Resources<br>
https://kangax.github.io/compat-table/es6/<br>
<br>

## [Versions](https://en.wikipedia.org/wiki/ECMAScript) (2021/01)
| Name | Date published |
|-|-|
| ES1 | 1997/06 |
| ES2 | 1998/06 |
| ES3 | 1999/12 |
| ES4 | Abandoned (버려짐) |
| ES5 | 2009/12 |
| ES2015 (ES6) | 2015/06 |
| ES2016 (ES7) | 2016/06 |
| ES2017 (ES8) | 2017/06 |
| ES.Next | Next version |
<br>

## 실행 요구사항

- **Node.js 14.x** 필수입니다. (`node-sass@5`는 Node 14까지만 호환되며, 모던 Node에서는 설치/빌드가 실패합니다.)
- nvm 사용 예:
  ```shell
  nvm install 14
  nvm use
  ```
- **모던 Node에서 `npm install`이 실패하는 것은 코드 버그가 아니라 환경 문제입니다.** Node 14 환경에서 재시도하세요.

## Babel + Webpack
Index
- [1. Config Babel](./config-babel.md)
- [2. Config Webpack](./config-webpack.md)
- [3. Config Webpack Sass](./config-webpack-sass.md)
- [4. Config Webpack Sass Extract](./config-webpack-sass-extract.md)

References
- https://poiemaweb.com/es6-babel-webpack-1<br>
- https://poiemaweb.com/es6-babel-webpack-2<br>

```
$ npm install
$ npm run build
```
