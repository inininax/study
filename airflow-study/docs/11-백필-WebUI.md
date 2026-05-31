# 11. Web UI에서 백필 (Backfill) ★

**백필(Backfill)** = 과거 시점의 logical_date에 해당하는 DAGRun을 **여러 개 만들어서** 한꺼번에 채우는 작업.

## 언제 쓰나?

- 새 DAG를 작성한 뒤 **과거 데이터까지 처음부터 채워야 할** 때
- 며칠간 DAG가 깨져 있어서 누락된 날짜들을 한꺼번에 다시 돌려야 할 때
- 비즈니스 로직이 바뀌어 **과거 일자도 새 로직으로** 다시 계산해야 할 때

## 단일 실행 vs 백필 vs catchup

```mermaid
graph TB
    A[과거 데이터를 처리하고 싶다] --> B{몇 일치?}
    B -->|1일 (특정 날짜 1개)| C[단일 실행<br/>Trigger w/ Logical Date]
    B -->|여러 일치| D[백필 사용]
    D --> E{언제?}
    E -->|DAG 처음 만들 때 자동| F[catchup=True<br/>스케줄러가 자동 채움]
    E -->|이미 운영 중인 DAG에서| G[Web UI Backfill 모달<br/>또는 CLI airflow dags backfill]
```

| 방식 | 트리거 | 용도 |
|------|--------|------|
| 단일 실행 | ▶ Trigger DAG | 1개 DAGRun |
| catchup=True | DAG 켜면 자동 | 새 DAG 최초 1회 자동 채움 |
| Web UI Backfill | ⟳ Backfill 버튼 | 운영 중 DAG의 과거 다시 채움 |
| CLI backfill | `airflow dags backfill` | 동일 (스크립트화 가능) |

> ⚠️ **본 학습 환경(Airflow 2.9.3)에는 Web UI Backfill 모달이 없습니다.** 모달은 **2.10+** 부터 도입되었으므로 아래 "Web UI Backfill 모달" 절은 2.10 이상 환경 사용자를 위한 참고 자료입니다.
> **2.9.3 사용자는 [CLI 방식](#cli-방식-모든-버전-가능) 절로 바로 넘어가세요.**

## Web UI Backfill 모달 (Airflow 2.10+ 전용 — 2.9에는 없음)

DAG 상세 화면 우측 상단의 ⟳ **Backfill** 버튼 클릭.

```
┌────────────────────────────────────────────────────────────┐
│ Backfill: 04_backfill_demo                                 │
├────────────────────────────────────────────────────────────┤
│  From       [ 2026-04-01 00:00:00  ]                       │
│  To         [ 2026-04-15 00:00:00  ]                       │
│                                                             │
│  Run Backwards    [ ]   ← 최신부터 거꾸로 돌리기           │
│  Reprocess Behavior:                                        │
│   ( ) None             기존 DAGRun이 있으면 건너뜀         │
│   (•) Failed           실패한 DAGRun만 재실행              │
│   ( ) Completed        성공한 것까지 다시 실행 (위험)      │
│                                                             │
│  Max Active Runs   [ 1 ]   ← 동시에 몇 개?                 │
│                                                             │
│  [ Dry Run ] [ Cancel ] [ Backfill ]                        │
└────────────────────────────────────────────────────────────┘
```

📷 캡처 권장: `docs/images/11-01-backfill-modal.png`

### 옵션 의미

| 항목 | 의미 |
|------|------|
| **From / To** | 백필 대상 logical_date 범위 |
| **Run Backwards** | 최신 → 과거 순으로 실행 (장애 복구 시 최신부터 빨리 보고 싶을 때) |
| **Reprocess Behavior** | 이미 존재하는 DAGRun을 어떻게 다룰지 |
| **Max Active Runs** | 한 번에 동시 실행할 DAGRun 개수 (DB 부하 제어) |
| **Dry Run** | 실제 실행하지 않고 어떤 DAGRun이 만들어질지만 보여줌 |

## CLI 방식 (모든 버전 가능)

```bash
docker compose exec airflow-scheduler \
  airflow dags backfill \
  --start-date 2026-04-01 \
  --end-date   2026-04-15 \
  04_backfill_demo
```

자세한 옵션은 [12. CLI 백필](12-백필-CLI.md) 참고.

## 백필이 진행되는 동안 UI에서 보이는 모습

Grid View에 새 컬럼들이 한꺼번에 생기며, 위에서부터 순차적으로 녹색이 됩니다.

```
Grid View (시간축 ↓)

logical_date         start  ext   load
2026-04-01           ✓      ✓     ✓     ← 완료
2026-04-02           ✓      ✓     ✓
2026-04-03           ✓      ✓     ▶     ← 실행 중
2026-04-04           ◇      ◇     ◇     ← 대기 (queued)
2026-04-05           ◇      ◇     ◇
...
2026-04-15           ◇      ◇     ◇
```

📷 캡처 권장: `docs/images/11-02-backfill-progress.png`

`run_id`는 `backfill__2026-04-03T00:00:00+00:00` 형태로 만들어집니다.

## "Reprocess Behavior" 자세히

이미 같은 logical_date의 DAGRun이 **존재할 때** 어떻게 할지:

| 옵션 | 동작 |
|------|------|
| **None** | 기존 DAGRun이 있으면 건너뜀 (가장 안전) |
| **Failed** | 기존 DAGRun이 failed면 다시 만들어 실행, success면 건너뜀 |
| **Completed** | 기존 DAGRun이 success여도 다시 실행 (**데이터 중복 위험**) |

> **권장 패턴**: 데이터 처리 Task는 **idempotent** (같은 logical_date로 여러 번 실행해도 결과가 같도록) 작성하고, 보통 **Failed**를 선택. SQL이라면 `DELETE WHERE dt='{{ ds }}'; INSERT ...` 또는 `INSERT OVERWRITE` 패턴.

## Max Active Runs

`max_active_runs=1`이면 한 번에 1개만 실행 → **순차 백필** (안전, 느림).
`max_active_runs=8`이면 8개 동시 실행 → **병렬 백필** (빠름, 데이터 충돌 주의).

DAG 정의에서 설정한 값이 기본값입니다.

```python
with DAG(..., max_active_runs=1):  # ← 백필 시 동시성 상한
    ...
```

## 백필 진행 도중 멈추기

UI에서 백필 중인 DAGRun들의 상태를 한 번에 변경:

1. Grid View에서 백필 컬럼들을 Shift-Click으로 다중 선택
2. 우측 패널 "Mark as ..." → **failed** 또는 직접 Pause
3. 또는 DAG 토글을 OFF로 → Scheduler가 새 Task를 큐잉하지 않음

CLI로 강제 종료:

```bash
docker compose exec airflow-scheduler \
  airflow dags state 04_backfill_demo 2026-04-05T00:00:00+00:00
# 상태 조회 후 필요시
docker compose exec airflow-scheduler \
  airflow tasks clear 04_backfill_demo --start-date 2026-04-05 --end-date 2026-04-15 -y
```

## 자주 묻는 것

### Q1. catchup=True인데 백필 모달은 또 왜 필요한가요?

`catchup=True`는 DAG **최초 켜질 때** 한 번 자동 채우기 위한 옵션. 이미 운영 중인 DAG에서 과거를 다시 돌리려면 백필 모달/CLI를 사용합니다.

### Q2. logical_date 과거 1개로 ▶ Trigger w/ config 하면 안 되나요?

1일치는 됩니다. 단,
- 그 사이의 다른 날짜는 안 채워짐
- run_type이 `manual`이라서 백필 통계에 안 잡힘
- run_id 형식이 다르므로 추후 식별 어려움

여러 날짜라면 항상 **백필 기능을 쓰세요.**

### Q3. 백필 중에 DAG를 수정하면?

Scheduler가 다음 사이클에 새 코드로 다시 파싱합니다. **이미 실행 중인 TaskInstance는 영향 없고**, 다음 TaskInstance부터 새 코드가 적용됩니다. 큰 변경이라면 백필 일시 중지 → 코드 변경 → 재개를 권장.

### Q4. 백필 도중 일부만 실패했을 때 다시 돌리려면?

방법 1) 같은 백필 명령을 다시 돌리고 Reprocess Behavior = **Failed** 선택.
방법 2) Grid View에서 실패한 셀들을 선택 → **Clear** → Scheduler가 자동 재시도.

자세한 시나리오는 [18. 실전 시나리오](18-실전시나리오.md) 참고.

## 실습

```bash
# 1) 04_backfill_demo DAG 토글 OFF 상태로 두고 catchup이 안 일어나도록
# 2) start_date를 2026-04-01로 두면 그 사이가 비어있다
# 3) CLI로 백필 시작
docker compose exec airflow-scheduler \
  airflow dags backfill \
  --start-date 2026-04-01 \
  --end-date   2026-04-07 \
  --reset-dagruns -y \
  04_backfill_demo

# 4) UI Grid View에서 7개 DAGRun이 만들어지는지 확인
# 5) 각 DAGRun의 "show_interval" task 로그에서 ds 값이 4/1, 4/2, ..., 4/7로 다른 것을 확인
```

## 다음으로

→ [12. CLI 백필 명령어 전체](12-백필-CLI.md)
