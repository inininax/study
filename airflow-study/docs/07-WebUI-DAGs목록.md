# 07. DAG 목록 페이지

http://localhost:8080 로그인 직후 진입하는 화면입니다.

## 화면 구성

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ DAGs                                                                         │
│ [● All 4] [Active 1] [Paused 3] [Running 0] [Failed 0]   🔍 search   ⚙      │
├──────────────────────────────────────────────────────────────────────────────┤
│  ON  dag_id              tags    schedule  last run  recent  next   actions │
│  ●●  01_hello_airflow    intro   @daily    -         ····    -      ▶  ⋮   │
│  ○○  02_template_*       templ   @daily    -         ····    -      ▶  ⋮   │
│  ○○  03_branching_*      branch  None      -         ····    -      ▶  ⋮   │
│  ○○  04_backfill_demo    backf   @daily    -         ····    -      ▶  ⋮   │
└──────────────────────────────────────────────────────────────────────────────┘
```

📷 캡처 권장: `docs/images/07-01-dag-list.png`

## 컬럼별 의미

| 컬럼 | 의미 |
|------|------|
| **ON 토글** | DAG 활성/비활성. 끄면 자동 스케줄링이 일어나지 않음 |
| **dag_id** | DAG 이름 (클릭하면 상세 페이지) |
| **tags** | DAG 정의의 `tags=[]` 값. 클릭하면 필터 |
| **schedule** | cron 또는 preset (`@daily`, `None`, `Dataset` 등) |
| **last run** | 가장 최근 DAGRun의 logical_date와 상태 |
| **recent** | 최근 N개 DAGRun을 작은 점으로 시각화 (마우스 오버 시 detail) |
| **next** | 다음에 만들어질 DAGRun의 logical_date |
| **actions** | ▶ Trigger / ⋮ More 버튼 |

## 토글 ON/OFF

DAG 좌측의 동그란 토글:

| 상태 | 색 | 동작 |
|------|----|------|
| ○○ OFF (paused) | 회색 | 스케줄러가 새 DAGRun을 만들지 않음 |
| ●● ON (active) | 파랑/녹색 | 스케줄러가 schedule에 따라 자동 실행 |

> ⚠️ DAG 토글이 OFF여도 `airflow dags trigger` 또는 ▶ 버튼으로 **수동 실행은 가능**합니다. 하지만 일부 옵션(SLA 등)은 동작하지 않을 수 있어 학습 중에는 ON을 권장.

## 필터 / 검색

상단 필터 칩:

- **All / Active / Paused** — 토글 상태 필터
- **Running / Failed** — 최근 DAGRun 상태 필터

🔍 검색은 `dag_id`와 `tags` 모두 매칭. 부분 문자열 OK.

⚙ 버튼:

- **Show Paused DAGs**: paused DAG 숨기기/보이기
- **Auto Refresh**: 30초 자동 새로고침
- **Owner / Tag 필터**

## ▶ 버튼 (Actions)

DAG 행 우측의 ▶ 클릭 시:

- **Trigger DAG** — 즉시 실행 (기본 conf)
- **Trigger DAG w/ config** — conf JSON / Logical Date 지정 (자세한 내용은 [10번 문서](10-단일실행-Trigger.md))

## ⋮ 버튼 (More)

- **Pause / Unpause** — 토글과 동일
- **Delete DAG** — 메타DB에서 DAG의 모든 이력 제거 (코드 파일은 그대로)
- **Documentation** — DAG의 `doc_md` 표시

## "Recent" 점 시각화

각 DAG 행에 가장 최근 N개 DAGRun이 작은 점으로 보입니다. 색은 [상태 색상](06-WebUI-개요.md#색상-코드-전-화면-공통)과 동일.

마우스 오버 → 해당 DAGRun의 logical_date / state / duration 툴팁.
클릭 → 해당 DAGRun으로 직접 이동.

📷 캡처 권장: `docs/images/07-02-recent-runs-tooltip.png`

## "Next Run" 의미

다음에 자동 스케줄링될 DAGRun의 logical_date를 보여줍니다.

> ⚠️ `next` 컬럼은 **다음 logical_date**를 보여줍니다. 실제로 그 DAGRun이 시작되는 시각은 `data_interval_end` 시점이라는 점 기억!
> 예: schedule=`@daily`, next=`2026-01-03 00:00`이면 → 실제 실행 시작은 `2026-01-04 00:00`.

## 다음으로

→ [08. DAG 상세 화면](08-WebUI-DAG상세화면.md)
