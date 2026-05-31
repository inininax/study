# react study

## react
- create project
```shell
npx create-react-app my-app
npx create-react-app my-app --template typescript
# or
npm init react-app my-app
# or
yarn create react-app my-app
yarn create react-app my-app --template typescript
```

- create redux
```shell
npx create-react-app my-app --template redux-typescript
# or
yarn create react-app my-app --template redux-typescript
```

- run
```shell
npx serve -s build
```

- test
```shell
/__tests__/*
App.spec.js
App.test.js
```

## ESLint + Prettier 설정
```shell
yarn add eslint --dev
yarn add prettier --dev
yarn add eslint-config-prettier --dev
yarn add eslint-plugin-prettier --dev

yarn run eslint --init
```

```shell
npm i eslint -D
npm i prettier -D
npm i eslint-config-prettier -D
npm i exlint-plugin-prettier -D

npx eslint --init

# prettier를 사용한 개별 수정
#npx prettier src/app.js --write
```

```shell
.eslintrc.js 파일에 하단 설정 추가
{
  "extends": [
    "eslint:recommended",
    "plugin:prettier/recommended"
  ]
}

package.json 파일의 scripts 부분 수정
{
  "scripts": {
    "build": "webpack --progress",
    "lint": "eslint src --fix"
  }
}
```

```shell
npm run lint
```

## ESLint + Prettier 자동화
```shell
npm i -D husky
npm i -D lint-staged

yarn add husky --dev
yarn add lint-staged --dev
```

```shell
package.json 
{
  "husky": {
    "hooks": {
      "pre-commit": "eslint app.js --fix"
    }
  },
  "lint-staged": {
    "*.js": "eslint --fix"
  }
}
```

## ESLint + Prettier 에디터에서 검사
```shell
... 생략
```


---



## ESLint
- install
```shell
npm install eslint --save-dev
# or
yarn add eslint --dev
```

- init
```shell
npx eslint --init
# or
./node_modules/.bin/eslint --init
# or
yarn run eslint --init
```

- .eslintrc.{js,yml,json} - 사이트 내 recommended option이 존재함
```shell
{
    "extends": "eslint:recommended"
}
```

- package.json 적용
```shell
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "lint": "eslint src --fix"
  },
```

- run
```shell
eslint ./src --fix
```

## Prettier
- install
```shell
npm i prettier -D 
npm install prettier --save-dev
# or
yarn add --dev --exact prettier
```

- .prettierrc.json
```shell
{
  ...
}
```

- .prettierignore
```shell
# Ignore artifacts:
build
coverage

# Ignore all HTML files:
*.html
```

- 사용
```shell
npx prettier --write .
# or
yarn prettier --write .
```

## ESLint + Prettier 함께 사용할 경우
```shell
npm i eslint-config-prettier -D
npm install eslint-config-prettier --save-dev
# or
yarn add eslint-config-prettier --dev

# .eslintrc.js 파일에 하단 내용 수정
{
  extends: [
    "eslint:recommended",
    "eslint-config-prettier"
  ]
}
```

- eslint + prettier 동시에 돌릴 경우
```shell
yarn add eslint-plugin-prettier --dev
```

- .eslintrc.js
```shell
{
  plugins: ["prettier"],
  rules: {
    "prettier/prettier": "error"
  }
}
```
