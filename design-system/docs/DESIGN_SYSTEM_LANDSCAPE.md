# Design System Landscape — 2025-2026 참고 자료

전 세계에서 가장 많이 사용되는 오픈소스 디자인 시스템/CSS 프레임워크 조사 결과.
이 프로젝트의 아키텍처 및 로드맵 결정 시 참고 자료로 활용.

## TOP 5 Rankings (by npm weekly downloads)

| 순위 | 이름 | npm 주간 다운로드 | GitHub Stars | 카테고리 |
|:---:|---|---:|---:|---|
| 1 | **Tailwind CSS** | 76,900,000 | 94,200 | Utility-first CSS |
| 2 | **MUI (Material UI)** | 8,290,000 | 94,000 | React Component Library |
| 3 | **Bootstrap** | 6,150,000 | 174,100 | Component CSS Framework |
| 4 | **Ant Design** | 2,730,000 | 97,800 | React Enterprise UI |
| 5 | **Mantine** | 1,420,000 | 28,000 | React Component Library |

### Special Mention

| 이름 | GitHub Stars | 비고 |
|---|---:|---|
| **shadcn/ui** | 106,500 | CLI copy-paste 모델 (npm 다운로드 측정 불가). UI 프로젝트 중 역대 최고 성장 속도 |
| **Chakra UI** | 38,800 | v3 rewrite 이후 성장 둔화, Mantine에 추월당함 |
| **daisyUI** | 40,600 | Tailwind 위에 컴포넌트 클래스 제공. 35+ 테마 |
| **Radix UI** | 18,500 | 헤드리스 프리미티브. shadcn/ui의 기반 |

## 상세 분석

### 1. Tailwind CSS (v4)

- **아키텍처**: `@theme {}` CSS 블록에서 토큰 정의 → 유틸리티 클래스 자동 생성
- **v4 변경점**: JS config 파일 제거, CSS-native `@import "tailwindcss"`, `@layer` 사용
- **강점**: 빌드 시 사용하지 않는 CSS 제거 (JIT), 모든 프레임워크 호환
- **약점**: 컴포넌트 없음 (유틸리티만), 마크업이 길어짐
- **참고**: 신규 React/Next.js 프로젝트의 사실상 표준. 개발자 37% 사용 (State of CSS 2025)

### 2. MUI (Material UI, v7)

- **아키텍처**: React 컴포넌트 + `sx` prop 인라인 스타일링 + Theme Provider
- **강점**: 40+ 프로덕션 컴포넌트, DataGrid/DatePicker 등 고급 컴포넌트, 강력한 TypeScript
- **약점**: React 전용, 번들 크기 큼, CSS-in-JS 런타임 비용
- **참고**: 엔터프라이즈 React 팀의 기본 선택. 유료 MUI X 티어 존재

### 3. Bootstrap (v5.3+)

- **아키텍처**: SCSS 변수 + 12-column Grid + pre-built 컴포넌트 + CSS Custom Properties
- **강점**: 전 세계 웹사이트 20% 사용, 학습 비용 최저, 모든 백엔드 스택 호환
- **약점**: 디자인 자유도 낮음, 커스터마이징 번거로움
- **참고**: jQuery 제거 완료 (v5). CSS variable 테마 지원. v6 기획 중

### 4. Ant Design (v5)

- **아키텍처**: React 컴포넌트 + CSS-in-JS (`@ant-design/cssinjs`) + ConfigProvider 테마
- **강점**: 데이터 중심 UI 최강 (Table, Form, Tree), 중국/아시아 생태계 지배
- **약점**: 번들 크기 매우 큼, 중국어 중심 문서, 서양 디자인 언어와 차이
- **참고**: 알리바바 제작. B2B SaaS/어드민 대시보드에 최적

### 5. Mantine (v7+)

- **아키텍처**: React 컴포넌트 + CSS Modules (런타임 CSS-in-JS 없음) + createTheme()
- **강점**: 120+ 컴포넌트, 70+ hooks, SSR/RSC 완벽 호환, DX 최고
- **약점**: React 전용, 생태계 규모 MUI/Bootstrap 대비 작음
- **참고**: v7에서 Emotion → CSS Modules로 전환. 2025 가장 빠르게 성장 중

### shadcn/ui (버전 없음)

- **아키텍처**: Radix UI 프리미티브 + Tailwind CSS + CLI로 소스 코드 복사
- **토큰**: OKLCH 기반 CSS 변수 (`--background`, `--foreground`, `--primary` 등)
- **강점**: 의존성 없음 (코드 소유), 완전 커스터마이징, Next.js 기본 선택
- **약점**: 컴포넌트 업데이트 시 수동 반영 필요
- **참고**: GitHub Stars 106k+로 UI 프로젝트 역대 최고 성장. Registry 모델로 팀별 비공개 컴포넌트 배포 가능

## 우리 프로젝트와의 비교

| 항목 | Tailwind | Bootstrap | daisyUI | 우리 시스템 |
|---|---|---|---|---|
| **토큰** | @theme CSS | SCSS vars | OKLCH CSS vars | 2-tier JSON → 7 formats |
| **컴포넌트** | 없음 | ~50 | ~70 | **20** |
| **유틸리티** | ~수천 (JIT) | ~200 | Tailwind 의존 | **~180** |
| **레이아웃** | Grid/Flex utils | 12-col Grid | Tailwind 의존 | **12-col Grid + Stack** |
| **프레임워크** | 없음 | 없음 | 없음 | **없음 (순수 CSS)** |
| **테마** | @theme 커스텀 | SCSS override | data-theme 35개 | **light/dark (data-theme)** |
| **DTCG** | 없음 | 없음 | 없음 | **지원** |
| **번들 크기** | JIT (사용분만) | ~250KB | ~40KB | **134KB (all.css)** |

## 향후 발전 방향 (참고)

1. **다중 테마 지원** — daisyUI처럼 `[data-theme="brand-a"]` 커스텀 테마 여러 개 지원
2. **Tailwind 호환 레이어** — 토큰을 Tailwind v4 `@theme` 블록으로 출력하여 Tailwind 프로젝트에서도 사용 가능하게
3. **프레임워크 바인딩** — React/Vue/Svelte 래퍼 컴포넌트 패키지 별도 제공
4. **OKLCH 컬러** — 현재 hex 기반 → OKLCH로 전환 시 다크모드 전환이 더 자연스러움
5. **컴포넌트 확장** — DatePicker, Combobox, Command Palette 등 고급 컴포넌트

## 데이터 출처

- [npm trends](https://npmtrends.com/bootstrap-vs-material-ui-vs-tailwindcss) — 다운로드 비교
- [State of CSS 2025](https://stateofcss.com/) — 개발자 사용 통계
- [GitHub](https://github.com) — Stars, contribution 활동
- [W3Techs](https://w3techs.com/) — 웹사이트 사용 통계

> 조사 시점: 2026-03-28
