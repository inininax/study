# Webpack
Index
- [1. Config Babel](./config-babel.md)
- [2. Config Webpack](./config-webpack.md)
- [3. Config Webpack Sass](./config-webpack-sass.md)
- [4. Config Webpack Sass Extract](./config-webpack-sass-extract.md)

## Install
```
$ npm install --save-dev mini-css-extract-plugin
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
    "css-loader": "^5.0.1",
    "mini-css-extract-plugin": "^1.3.3",
    "node-sass": "^5.0.0",
    "sass-loader": "^10.1.0",
    "style-loader": "^2.0.0",
    "webpack": "^5.11.1",
    "webpack-cli": "^4.3.1"
  },
  "dependencies": {
    "@babel/polyfill": "^7.12.1"
  }
}
```

## create webpack.config.js
[Project Root]/[webpack.config.js](./webpack.config.js)
```
const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  // entry files
  entry: ['@babel/polyfill', './src/js/main.js', './src/sass/main.scss'],
  // 컴파일 + 번들링된 js 파일이 저장될 경로와 이름 지정
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'js/bundle.js'
  },
  plugins: [
    // 컴파일 + 번들링 CSS 파일이 저장될 경로와 이름 지정
    new MiniCssExtractPlugin({ filename: 'css/style.css' })
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        include: [
          path.resolve(__dirname, 'src/js')
        ],
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
            plugins: ['@babel/plugin-proposal-class-properties']
          }
        },
        exclude: /node_modules/
      },
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader'
        ],
        exclude: /node_modules/
      }
    ]
  },
  devtool: 'source-map',
  // https://webpack.js.org/concepts/mode/#mode-development
  mode: 'development'
};
```

## run
```
$ npm run build

> learn-babel-webpack@1.0.0 build
> webpack -w

asset bundle.js 419 KiB [emitted] (name: main) 1 related asset
runtime modules 931 bytes 4 modules
modules by path ./node_modules/core-js/modules/*.js 190 KiB 273 modules
modules by path ./node_modules/core-js/library/ 6.43 KiB 18 modules
modules by path ./node_modules/core-js/fn/ 1.29 KiB 11 modules
modules by path ./src/ 5.67 KiB
  modules by path ./src/js/*.js 4.21 KiB 2 modules
  modules by path ./src/sass/*.scss 1.47 KiB 2 modules
modules by path ./node_modules/@babel/polyfill/lib/*.js 1.22 KiB
  ./node_modules/@babel/polyfill/lib/index.js 686 bytes [built] [code generated]
  ./node_modules/@babel/polyfill/lib/noConflict.js 567 bytes [built] [code generated]
modules by path ./node_modules/css-loader/dist/runtime/*.js 3.78 KiB
  ./node_modules/css-loader/dist/runtime/cssWithMappingToString.js 2.21 KiB [built] [code generated]
  ./node_modules/css-loader/dist/runtime/api.js 1.57 KiB [built] [code generated]
4 modules
webpack 5.11.1 compiled successfully in 1861 ms
```