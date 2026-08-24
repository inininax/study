# node-study

Node.js 기초 학습 예제 모음입니다. (모듈, HTTP 서버, 파일시스템, 이벤트 등)

## 디렉터리 구성

| 경로 | 내용 |
|------|------|
| `basic/` | 코어 모듈 기초 예제 — `filesystem_read.js`(파일 읽기), `filesystem_write.js`(파일 쓰기), `path.js`(path 모듈) |
| `ex/` | 단계별 연습 예제 — 아래 표 참고 |
| `temp/` | 임시 유틸 스크립트 — `find_requestmapping.js`, `merge_sqlmap*.js` (SQL 맵 파일 탐색/병합) |

## ex/ 연습 예제

| 파일 | 주제 |
|------|------|
| `ex01-server.js` | 커스텀 모듈 require + http 서버 기본 |
| `ex02-http-url.js` | url 모듈로 요청 라우팅 |
| `ex03-filesystem.js/.html` | 파일시스템으로 HTML 파일 서빙 |
| `ex04-filesystem.js` | 파일 읽기/쓰기 심화 |
| `ex05-url.js` | URL 파싱 |
| `ex06-uppercase.js` | upper-case 외부 패키지 사용 |
| `ex07-events.js` | EventEmitter 이벤트 처리 |

## 실행 방법

```bash
node basic/path.js
node ex/ex01-server.js
```

외부 패키지(`upper-case`, `glob`, `walk`)가 필요한 예제는 먼저 설치:

```bash
npm install
```

> 참고: 일부 예제는 `./module/myfirstmodule.js` 같은 로컬 모듈을 참조합니다.
