# es6, webpack, babel example
- install
```shell
npm init -y
npm install webpack webpack-cli --save-dev
npm install --save lodash
npm install --save-dev style-loader css-loader
npm install --save-dev csv-loader xml-loader
npm install toml yamljs json5 --save-dev
```

- run
```shell
# npx webpack --config webpack.config.js
npm run build
```

- path
```text
tree -I node_modules
.
├── README.md
├── dist
│   ├── 106d9ce17b481ed61205.png
│   ├── bundle.js
│   ├── bundle.js.LICENSE.txt
│   ├── ce150814b32364bc9e09.woff
│   ├── ce150814b32364bc9e09.woff2
│   └── index.html
├── package-lock.json
├── package.json
├── src
│   ├── data.csv
│   ├── data.json5
│   ├── data.toml
│   ├── data.xml
│   ├── data.yaml
│   ├── icon.png
│   ├── index.js
│   ├── my-font.woff
│   ├── my-font.woff2
│   └── style.css
└── webpack.config.js
```

- Reference
    - https://webpack.js.org/guides/getting-started
    - https://webpack.js.org/guides/asset-management
