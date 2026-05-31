# Webpack
Index
- [1. Config Babel](./config-babel.md)
- [2. Config Webpack](./config-webpack.md)
- [3. Config Webpack Sass](./config-webpack-sass.md)
- [4. Config Webpack Sass Extract](./config-webpack-sass-extract.md)

## Install
```
$ npm install --save-dev webpack webpack-cli
$ npm install --save-dev babel-loader
$ npm install @babel/polyfill
```

[Project Root]/[package.json](./package.json)
```
{
  "name": "learn-babel-webpack",
  "version": "1.0.0",
  "scripts": {
    "build": "webpack -w"
  },
  "devDependencies": {
    "@babel/cli": "^7.12.10",
    "@babel/core": "^7.12.10",
    "@babel/plugin-proposal-class-properties": "^7.12.1",
    "@babel/preset-env": "^7.12.11",
    "babel-loader": "^8.2.2",
    "webpack": "^5.11.1",
    "webpack-cli": "^4.3.1"
  },
  "dependencies": {
    "@babel/polyfill": "^7.12.1"
  }
}
```

```
"babel src/js -w -d dist/js" -> "webpack -w"
```

## create webpack.config.js
[Project Root]/[webpack.config.js](./webpack.config.js)
```
const path = require('path');

module.exports = {
    // enntry file
    entry: './src/js/main.js',
    // 컴파일 + 번들링된 js 파일이 저장될 경로와 이름 지정
    output: {
        path: path.resolve(__dirname, 'dist/js'),
        filename: 'bundle.js'
    },
    module: {
        rules: [{
            test: /\.js$/,
            include: [
                path.resolve(__dirname, 'src/js')
            ],
            exclude: /node_modules/,
            use: {
                loader: 'babel-loader',
                options: {
                    presets: ['@babel/preset-env'],
                    plugins: ['@babel/plugin-proposal-class-properties']
                }
            }
        }]
    },
    devtool: 'source-map',
    // https://webpack.js.org/concepts/mode/#mode-development
    mode: 'development'
};
```

## run
```
$ npm run build (package.json scripts)

> learn-babel-webpack@1.0.0 build
> webpack -w

asset bundle.js 403 KiB [emitted] (name: main) 1 related asset
runtime modules 668 bytes 3 modules
modules by path ./node_modules/core-js/modules/*.js 190 KiB 273 modules
modules by path ./node_modules/core-js/library/ 6.43 KiB 18 modules
modules by path ./node_modules/core-js/fn/ 1.29 KiB 11 modules
modules by path ./node_modules/@babel/polyfill/lib/*.js 1.22 KiB
  ./node_modules/@babel/polyfill/lib/index.js 686 bytes [built] [code generated]
  ./node_modules/@babel/polyfill/lib/noConflict.js 567 bytes [built] [code generated]
modules by path ./src/js/*.js 4.21 KiB
  ./src/js/main.js 509 bytes [built] [code generated]
  ./src/js/lib.js 3.71 KiB [built] [code generated]
./node_modules/core-js/es6/index.js 5.78 KiB [built] [code generated]
./node_modules/core-js/web/index.js 157 bytes [built] [code generated]
./node_modules/regenerator-runtime/runtime.js 24 KiB [built] [code generated]
webpack 5.11.1 compiled successfully in 1550 ms
```