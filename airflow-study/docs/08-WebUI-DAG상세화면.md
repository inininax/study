# 08. DAG 상세 화면

DAG 이름을 클릭하면 진입. 좌측에 **Grid View**, 우측에 선택한 DAGRun/Task의 상세 패널이 보입니다.

## 화면 레이아웃

```
┌──────────────────────────────────────────────────────────────────────┐
│ 04_backfill_demo                                                     │
│ Schedule: @daily   Owner: airflow              ▶ ⟳ ⋮  [Pause toggle] │
│ ─────────────────────────────────────────────────────────────────── │
│ [Grid] [Graph] [Calendar] [Task Duration] [Gantt] [Code] [Audit Log] │
├──────────────────────────────────────────────────────────────────────┤
│ ┌──── Grid (좌측) ────┐  ┌──────── Detail Panel (우측) ─────────┐ │
│ │ logical_date       │  │  Tabs: Details / Logs / XCom / Code   │ │
│ │   ↓                │  │                                       │ │
│ │ 04-01  ✓ ✓ ✓       │  │  Task: fake_load                       │ │
│ │ 04-02  ✓ ✓ ✓       │  │  State: success                        │ │
│ │ 04-03  ✓ ✓ ▶       │  │  Try: 1                                │ │
│ │ 04-04  ◇ ◇ ◇       │  │  Logs: ...                             │ │
│ │ ...                │  │                                       │ │
│ └────────────────────┘  └──────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

📷 캡처 권장: `docs/images/08-01-dag-detail.png`

## Grid View

가장 많이 보는 뷰. 행은 **시간(logical_date)**, 열은 **Task**.

```
        [Tasks →]
        start  ext   load
04-01    ✓     ✓     ✓     ← 3개 Task 모두 success
04-02    ✓     ✓     ✓
04-03    ✓     ▶     ◇     ← ext 실행 중, load 대기
04-04    ◇     ◇     ◇
```

### 셀 클릭 동작

| 클릭 위치 | 결과 |
|----------|------|
| **헤더(Task 이름)** | 우측에 해당 Task의 종합 정보 |
| **행 헤더(날짜)** | 우측에 해당 DAGRun의 종합 정보 |
| **셀(개별 TaskInstance)** | 우측에 해당 TI의 상세 |

### 셀 우클릭(또는 셀 클릭 후 우측 패널 액션)

- **Clear** — TI 상태를 None으로 초기화 → Scheduler가 자동 재실행
- **Mark as success** — 성공으로 강제 마킹 (실행 안 함)
- **Mark as failed** — 실패로 강제 마킹

> Clear / Mark는 다음 옵션과 함께 사용:
> - Past — 이 시점 **이전** TI도 함께
> - Future — 이 시점 **이후** TI도 함께
> - Upstream — 이 Task의 upstream도 함께
> - Downstream — downstream도 함께
> - Recursive — 하위 SubDag까지

📷 캡처 권장: `docs/images/08-02-grid-clear-modal.png`

## Graph View

DAG의 그래프 시각화. 한 DAGRun을 골라서 그 시점의 상태로 색칠해서 보여줍니다.

```mermaid
graph LR
    start --> hello --> end
```

상단의 드롭다운으로 어떤 DAGRun을 표시할지 선택 가능.

📷 캡처 권장: `docs/images/08-03-graph-view.png`

## Calendar View

월/일 단위로 DAGRun 성공/실패를 캘린더 히트맵으로 표시.

📷 캡처 권장: `docs/images/08-04-calendar.png`

## Task Duration

Task별로 실행 시간이 시간순으로 어떻게 변하는지 추세선.
**갑자기 시간이 튀는 Task**를 발견할 때 유용.

📷 캡처 권장: `docs/images/08-05-task-duration.png`

## Gantt

특정 한 DAGRun의 Task별 시작/종료를 간트차트로 표시. **병렬도 / 직렬 병목** 식별에 좋음.

📷 캡처 권장: `docs/images/08-06-gantt.png`

## Code

DAG 파일 소스 코드를 그대로 보여줌. **운영 환경에서 코드 배포본을 확인하는 용도**로 사용.

> ⚠️ 여기 보이는 코드는 **Webserver가 마지막에 파싱한 시점의 코드**입니다. 방금 수정했는데 여기 안 반영됐다면 → Scheduler가 아직 재파싱하지 않았거나 파싱 에러가 있을 수 있음. `airflow dags list-import-errors`로 확인.

## Audit Log

이 DAG에 대해 누가 언제 무엇을 했는지(트리거, clear, pause 등)의 기록.

## 우측 Detail Panel — TI 선택 시

특정 셀을 클릭하면 우측에 다음 탭이 나타납니다.

| 탭 | 내용 |
|----|------|
| **Details** | TI의 메타정보 (state, try_number, queue, pool, executor_config, hostname...) |
| **Logs** | 시도별 로그. 시도(try) 번호 탭으로 분리 |
| **XCom** | 이 TI가 push한 XCom 값들 |
| **Code** | 이 Task의 코드(렌더링된 Jinja 결과 포함) |
| **Rendered Template** | Jinja 템플릿이 **실제 어떤 값으로 치환됐는지** 확인 (★ 디버깅 핵심) |

### "Rendered Template" — 매우 중요

`{{ ds }}`, `{{ data_interval_end }}` 등 예약어가 **실제 어떤 값**으로 들어갔는지 확인할 수 있습니다.

예를 들어 BashOperator의 bash_command가 다음과 같다면:

```python
bash_command="aws s3 cp s3://bucket/raw/{{ ds }}/ s3://bucket/cur/{{ ds_nodash }}/"
```

Rendered Template 탭에는:

```
bash_command:
  aws s3 cp s3://bucket/raw/2026-01-03/ s3://bucket/cur/20260103/
```

→ Jinja 표현식이 헷갈릴 때 **여기서 항상 정답을 확인**하세요.

📷 캡처 권장: `docs/images/08-07-rendered-template.png`

## DAGRun 단위 액션 (행 헤더 클릭)

행 헤더(날짜)를 클릭하면 우측에 DAGRun 종합 정보가 나옵니다.

| 액션 | 효과 |
|------|------|
| **Clear** | 이 DAGRun의 모든 TI 초기화 → 처음부터 다시 |
| **Mark Success** | 이 DAGRun을 success로 강제 |
| **Mark Failed** | 이 DAGRun을 failed로 강제 |
| **Re-run** | 동일 logical_date로 새 DAGRun 생성 (옵션에 따라 다름) |
| **Delete DAG Run** | 이 DAGRun 자체를 삭제 (이력에서 제거) |

📷 캡처 권장: `docs/images/08-08-dagrun-actions.png`

## 빈번한 운영 패턴

### 단일 Task 실패 → 재시도

1. 빨간 셀 클릭
2. 우측 패널에서 **Clear** → state none → Scheduler가 다시 큐잉

### DAGRun 전체 재실행

1. 행 헤더 클릭
2. **Clear (with downstream)** → 모든 Task 초기화

### Task 코드 수정 후 효과 확인

1. 코드 수정 → 30초 대기 (Scheduler 재파싱)
2. **Code** 탭에서 새 코드 확인
3. 재실행 (위 두 패턴 중 하나)
4. **Rendered Template** 탭에서 Jinja 결과 확인

## 다음으로

→ [09. DAG 실행 메커니즘](09-DAG-실행메커니즘.md)
