# Sencha Ext JS study
- extjs 학습을 위한 예제들입니다.

## Ext JS 라이브러리 직접 설치 필요
- Ext JS는 상용/GPL 라이선스이므로 이 저장소에 포함하지 않습니다.
- 예제 실행 전 아래 버전을 직접 내려받아 `src/libs/` 아래에 배치하세요.
  - `src/libs/ext-5.1.4/`
  - `src/libs/ext-6.2.0-gpl/`

## 설치 체크리스트 (HTML이 실제 참조하는 경로 기준)

아래 파일들이 존재하면 대부분의 예제가 동작합니다. 경로는 `src/*.html` 기준 상대경로입니다.

**ext-5.1.4** (SDK 압축을 풀어 `src/libs/ext-5.1.4/`로 배치):

- [ ] `src/libs/ext-5.1.4/ext-all-debug.js` — 핵심 라이브러리 (대부분의 예제가 참조; `build/ext-all.js`가 아니라 폴더 루트의 `ext-all-debug.js`임에 주의)
- [ ] `src/libs/ext-5.1.4/packages/ext-theme-crisp/build/resources/ext-theme-crisp-all.css` — crisp 테마 (다수 예제)
- [ ] `src/libs/ext-5.1.4/packages/sencha-charts/build/sencha-charts.js` — 차트 예제
- [ ] (일부 예제만) 각 테마 리소스:
  - `src/libs/ext-5.1.4/packages/ext-theme-classic/build/resources/ext-theme-classic-all.css`
  - `src/libs/ext-5.1.4/packages/ext-theme-aria/build/resources/ext-theme-aria-all.css`
  - `src/libs/ext-5.1.4/packages/ext-theme-neptune-touch/build/resources/ext-theme-neptune-touch-all.css`

**ext-6.2.0-gpl** (GPL SDK를 `src/libs/ext-6.2.0-gpl/`로 배치):

- [ ] `src/libs/ext-6.2.0-gpl/ext-all-debug.js` — 핵심 라이브러리
- [ ] `src/libs/ext-6.2.0-gpl/classic/theme-triton/theme-triton-debug.js` — triton 테마 JS
- [ ] `src/libs/ext-6.2.0-gpl/classic/theme-triton/resources/theme-triton-all.css` — triton 테마 CSS
- [ ] `src/libs/ext-6.2.0-gpl/packages/ux/classic/ux-debug.js` — UX 패키지
- [ ] `src/libs/ext-6.2.0-gpl/packages/ux/classic/triton/resources/ux-all.css` — UX 패키지 CSS
- [ ] `src/libs/ext-6.2.0-gpl/classic/locale/locale-ko-debug.js` — 한국어 로케일

**기타** (소수 jQuery 예제):

- [ ] `src/libs/jquery/1.11.2/jquery.min.js`
- [ ] `src/libs/jquery/3.3.1/jquery.min.js`
- [ ] `src/libs/jquery/jquery-3.3.1.min.js`

> 참고: `src/extjs5/chapter19/` 의 두 예제(`sliding_paging`, `progressbar_paging`)는 작성자의 로컬 플러그인 파일(`plugin/SlidingPager.js`, `plugin/ProgressBarPager.js`)을 참조했으나 유실되어 HTML에서 주석 처리했습니다.

## ext-6.2.0-gpl download
- Sencha GPL Licensing : Sencha Ext JS, Sencha GXT, and Sencha Touch
- https://www.sencha.com/legal/GPL/

## extjs5 원문은 아래와 같습니다. 원문 링크를 확인해 주세요.
- https://www.inflearn.com/course/sencha-extjs-6-%EA%B8%B0%EC%B4%88/
- https://github.com/mongoworld/extjs_world
- http://mongodev.tistory.com
- https://www.youtube.com/channel/UCmIEd8PTq5PXJyXlboXKOpQ
