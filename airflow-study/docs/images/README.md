# 이미지 / 스크린샷 가이드

본 학습 문서에서는 다이어그램은 Mermaid로, 화면 묘사는 ASCII로 임베드해 두었습니다.
하지만 **실제 Web UI 화면을 직접 캡처해서 이 폴더에 넣어 두면** 본인의 학습 노트로서 가장 효과적입니다.

## 캡처 도구

| OS | 단축키 |
|----|--------|
| macOS | `Cmd + Shift + 4` (영역) / `Cmd + Shift + 5` (도구창) |
| Windows | `Win + Shift + S` |
| Linux | `gnome-screenshot -a` 등 |

## 캡처 권장 목록

각 문서에서 📷 마크가 붙은 위치에 권장 파일명을 적어 두었습니다. 이 폴더에 같은 이름으로 저장하면 본 가이드의 권장 동선과 그대로 매칭됩니다.

| 파일명 | 어디서 캡처? |
|--------|------------|
| `04-01-dag-list.png` | 로그인 직후 DAGs 목록 |
| `05-01-grid-success.png` | `01_hello_airflow` 성공한 Grid View |
| `05-02-task-logs.png` | `say_hello` Task의 Logs 탭 |
| `06-01-overview.png` | UI 전체 레이아웃 (상단 네비 + 메인) |
| `06-02-status-legend.png` | 상태 색상 범례 (Grid 우측) |
| `07-01-dag-list.png` | DAGs 목록 + 필터 / 검색 영역 |
| `07-02-recent-runs-tooltip.png` | Recent 점에 마우스 올렸을 때 툴팁 |
| `08-01-dag-detail.png` | DAG 상세 진입 직후 (Grid + 우측 패널) |
| `08-02-grid-clear-modal.png` | TI Clear 옵션 모달 |
| `08-03-graph-view.png` | Graph View |
| `08-04-calendar.png` | Calendar View |
| `08-05-task-duration.png` | Task Duration 차트 |
| `08-06-gantt.png` | Gantt 뷰 |
| `08-07-rendered-template.png` | Rendered Template 탭 (★ 매우 중요) |
| `08-08-dagrun-actions.png` | DAGRun 행 헤더 우측 액션들 |
| `10-01-trigger-button.png` | DAG 헤더의 ▶ Trigger 버튼 위치 |
| `10-02-trigger-config-modal.png` | Trigger DAG w/ config 모달 |
| `11-01-backfill-modal.png` | Web UI Backfill 모달 (Airflow 2.10+) |
| `11-02-backfill-progress.png` | 백필 진행 중 Grid View |
| `14-01-rendered-template.png` | Rendered Template으로 Jinja 디버깅 |
| `17-01-variables.png` | Admin → Variables 화면 |
| `17-02-connections.png` | Admin → Connections 화면 |
| `17-03-xcom.png` | Task XCom 탭 |
| `18-01-clear-modal.png` | Past/Future/Up/Downstream 옵션 |

## 캡처 팁

1. **브라우저 줌은 100%로 통일** — 해상도 일관성
2. **테마 통일** — 라이트/다크 둘 중 하나로
3. **개인정보 마스킹** — 사내 connection 호스트, 이메일 등
4. **단계별 화면**은 같은 DAG로 통일하면 비교 학습에 좋음 (`04_backfill_demo` 추천)

## 다이어그램 렌더링

본 문서들의 다이어그램은 **Mermaid** 포맷입니다.

- GitHub: 자동 렌더
- VS Code: [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) 확장
- Cursor / IntelliJ: 내장 지원

렌더링이 안 되는 환경이라면 [mermaid.live](https://mermaid.live/)에 코드를 붙여 그림으로 변환 가능합니다.
