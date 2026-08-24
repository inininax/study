# Node gulp webpack

## 원문
- 원문 강좌를 봐주세요. 강좌 gulp, webpack 학습을 위해 올린 자료입니다.
- https://velopert.com/1344
- https://velopert.com/1456

## 실행 요구사항

- **Node.js ≤ 10** 필수입니다. (gulp 3 / Babel 6 시대의 히스토리컬 학습 자료로, 모던 Node에서는 동작하지 않습니다.)
- nvm 사용 예:
  ```shell
  nvm install 10
  nvm use
  ```
- **모던 Node(12+)에서 `npm install`이 실패하는 것은 코드 버그가 아니라 환경 문제입니다.** node-gyp 기반 구버전 의존성 빌드 실패 등은 Node ≤ 10 환경에서 재시도하세요.

## Install
```shell
npm install -g gulp
npm install -g graceful-fs lodash
npm install (or npm install package.json)
```

## Run
```text
gulp
```