# Babel
Index
- [1. Config Babel](./config-babel.md)
- [2. Config Webpack](./config-webpack.md)
- [3. Config Webpack Sass](./config-webpack-sass.md)
- [4. Config Webpack Sass Extract](./config-webpack-sass-extract.md)

## Install
```
$ npm init -y
$ npm install --save-dev @babel/core @babel/cli
$ npm install --save-dev @babel/preset-env
$ npm install --save-dev @babel/plugin-proposal-class-properties
```

[Project Root]/[package.json](./package.json)
```
{
  "name": "learn-babel-webpack",
  "version": "1.0.0",
  "scripts": {
    "build": "babel src/js -w -d dist/js"
  },
  "devDependencies": {
    "@babel/cli": "^7.12.10",
    "@babel/core": "^7.12.10",
    "@babel/plugin-proposal-class-properties": "^7.12.1",
    "@babel/preset-env": "^7.12.11"
  }
}
```

-w: 타깃 폴더에 있는 모든 파일들의 변경을 감지하여 자동으로 트랜스파일한다. (--watch 옵션의 축약형)<br>
-d: 트랜스파일링된 결과물이 저장될 폴더를 지정한다. (--out-dir 옵션의 축약형)<br>
<br>

## create .babelrc
[Project Root]/[.babelrc](./.babelrc)
```
{
  "presets": ["@babel/preset-env"],
  "plugins": ["@babel/plugin-proposal-class-properties"]
}
```

## run
```
$ npm run build (package.json scripts)

> learn-babel-webpack@1.0.0 build
> babel src/js -w -d dist/js

Successfully compiled 2 files with Babel (469ms).
```

```
$ node dist/js/main.js 
3.141592653589793
36.4621596072079
{ a: 1, b: 2, x: { c: 3, d: 4 } }
10
```