# Next App
## Prettier
````shell
npm info "eslint-config-airbnb@latest" peerDependencies
yarn add -D eslint eslint-config-airbnb eslint-plugin-import eslint-plugin-jsx-a11y eslint-plugin-react eslint-plugin-react-hooks
yarn add -D prettier eslint-config-prettier eslint-plugin-prettier
yarn add -D babel-eslint eslint-plugin-babel 
````

- ESLint 설정하기 (.eslintrc.json 파일 설정)
```json
{
  "env": {
    "browser": true,
    "es6": true,
    "node": true
  },
  "parser": "babel-eslint",
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
    "airbnb",
    "plugin:prettier/recommended"
  ],
  "settings": {
    "react": {
      "version": "detect"
    }
  },
  "parserOptions": {
    "ecmaFeatures": {
      "jsx": true
    },
    "ecmaVersion": 2018,
    "sourceType": "module"
  },
  "plugins": [
    "react",
    "react-hooks",
    "prettier"
  ],
  "rules": {
    "react/react-in-jsx-scope": 0,
    "react/prefer-stateless-function": 0,
    "react/jsx-filename-extension": 0,
    "react/jsx-one-expression-per-line": 0,
    "no-nested-ternary": 0
  },
  "globals": {
    "React": "writable"
  }
}
```

- Prettier 설정하기 (.prettierrc 파일 설정)
```json
{
  "singleQuote": false,
  "semi": true,
  "useTabs": false,
  "tabWidth": 2,
  "trailingComma": "all",
  "printWidth": 80
}
```