# 12. CLI 백필 명령어

UI 모달이 없는 버전이거나, 백필을 스크립트화하고 싶을 때 사용합니다.

## 기본 형태

```bash
docker compose exec airflow-scheduler \
  airflow dags backfill \
  --start-date YYYY-MM-DD \
  --end-date   YYYY-MM-DD \
  <DAG_ID>
```

`--start-date`와 `--end-date`는 logical_date 기준입니다.

## 모든 옵션

```
airflow dags backfill [-h]
  -s, --start-date START_DATE        시작 logical_date (YYYY-MM-DD 또는 ISO 8601)
  -e, --end-date END_DATE            종료 logical_date
  -B, --run-backwards                최신부터 거꾸로 실행
  -m, --mark-success                 실제 실행하지 않고 success로 마킹
  -t, --task-regex REGEX             특정 Task만 백필 (예: --task-regex 'extract_.*')
  -i, --ignore-dependencies          Task 의존성 무시
  -I, --ignore-first-depends-on-past 첫 DAGRun의 depends_on_past 무시
  -l, --local                        로컬에서 실행 (디버깅용)
  -p, --pool POOL                    이 백필을 특정 pool로 제한
      --delay-on-limit DELAY         max_active_runs 도달 시 대기 시간(초)
      --reset-dagruns                기존 DAGRun을 지우고 새로 만듬
      --rerun-failed-tasks           실패한 Task만 다시 시도
  -c, --conf CONF                    JSON conf (수동 트리거와 동일)
      --continue-on-failures         일부 DAGRun이 실패해도 백필 계속 진행
      --disable-retry                Task 재시도 비활성화
  -y, --yes                          확인 프롬프트 자동 yes
      --treat-dag-as-regex           DAG_ID를 정규식으로 취급
  -n, --dry-run                      각 Task의 Template Fields를 렌더링만 해보고 끝 (실 실행 X)
```

## 자주 쓰는 패턴

### 1) 기본 백필

```bash
airflow dags backfill \
  --start-date 2026-04-01 \
  --end-date   2026-04-15 \
  04_backfill_demo
```

→ 4/1, 4/2, ..., 4/15 (총 15개) DAGRun 생성. 이미 존재하는 DAGRun은 건너뜀.

### 2) 기존 DAGRun을 모두 초기화하고 다시

```bash
airflow dags backfill \
  --start-date 2026-04-01 \
  --end-date   2026-04-15 \
  --reset-dagruns -y \
  04_backfill_demo
```

→ 기존에 만들어진 DAGRun을 **삭제하고** 새로 백필. **운영 데이터 주의.**

### 3) 실패한 Task만 재시도

```bash
airflow dags backfill \
  --start-date 2026-04-01 \
  --end-date   2026-04-15 \
  --rerun-failed-tasks \
  04_backfill_demo
```

→ 이미 success인 Task는 건드리지 않고, failed/upstream_failed Task만 다시 시도.

### 4) 특정 Task만 백필

```bash
airflow dags backfill \
  --start-date 2026-04-01 \
  --end-date   2026-04-15 \
  --task-regex 'fake_load' \
  04_backfill_demo
```

→ 해당 정규식에 매치되는 Task만 실행. 의존성도 함께 평가됩니다.

### 5) Dry Run (Template Fields만 렌더링)

```bash
airflow dags backfill \
  --start-date 2026-04-01 \
  --end-date   2026-04-15 \
  --dry-run \
  04_backfill_demo
```

→ Airflow 2.9의 `--dry-run`(`-n`)은 **각 Task의 Template Fields(`bash_command`, `sql` 등)를 어떻게 렌더링할지만** 출력하고 실제 실행은 건너뜁니다. Jinja 표현식 검증용.
> 백필 범위에 어떤 logical_date가 만들어질지 사전에 보려면 `airflow dags list-runs -d <DAG_ID>`로 기존 DAGRun 확인이 더 유용합니다.

### 6) 최신부터 거꾸로

```bash
airflow dags backfill \
  --start-date 2026-04-01 \
  --end-date   2026-04-15 \
  --run-backwards \
  04_backfill_demo
```

→ 4/15부터 4/1 순으로 진행. 운영 중 장애가 생긴 직후 **최신 데이터부터 빠르게 복구**할 때 유용.

### 7) Mark Success (실행 없이 성공 처리)

```bash
airflow dags backfill \
  --start-date 2026-04-01 \
  --end-date   2026-04-15 \
  --mark-success \
  04_backfill_demo
```

→ Task를 실제로 실행하지 않고 success 마킹만. **이미 다른 도구로 처리한 데이터가 있어 Airflow 메타DB만 맞추고 싶을 때.**

### 8) conf 전달 백필

```bash
airflow dags backfill \
  --start-date 2026-04-01 \
  --end-date   2026-04-07 \
  --conf '{"region":"kr"}' \
  04_backfill_demo
```

→ 모든 DAGRun에 동일한 `dag_run.conf`가 들어감.

## 그 외 유용한 CLI

### Task / DAGRun 상태 초기화 (clear)

특정 구간의 Task 상태를 모두 None으로 만들면 Scheduler가 자동 재시도.

```bash
airflow tasks clear 04_backfill_demo \
  --start-date 2026-04-03 \
  --end-date   2026-04-05 \
  -y
```

옵션:
- `--only-failed`: 실패한 것만
- `--only-running`: 실행 중인 것만
- `-t TASK_REGEX`: 특정 Task만

### DAGRun 직접 삭제

```bash
airflow dags delete 04_backfill_demo  # ⚠ DAG 자체 + 모든 이력 삭제 (위험)
```

특정 DAGRun만 지울 땐 UI Grid View에서 컬럼 우클릭 → Delete.

### DAG 토글 ON/OFF

```bash
airflow dags pause   04_backfill_demo
airflow dags unpause 04_backfill_demo
```

### 실행 가능성 미리 보기

```bash
airflow dags list-runs -d 04_backfill_demo
airflow dags state    04_backfill_demo 2026-04-03T00:00:00+00:00
airflow tasks list    04_backfill_demo --tree
```

### 단일 Task 직접 실행 (테스트)

```bash
airflow tasks test 04_backfill_demo show_interval 2026-04-03
```

→ 메타DB에 기록 안 됨. **로컬 디버깅 전용.**

## 정리

| 목적 | 명령어 |
|------|-------|
| 그냥 백필 | `airflow dags backfill -s -e DAG_ID` |
| 기존 것 다 지우고 | + `--reset-dagruns -y` |
| 실패한 것만 재시도 | + `--rerun-failed-tasks` |
| 시뮬레이션 | + `--dry-run` |
| 최신부터 | + `--run-backwards` |
| 실행 없이 마킹만 | + `--mark-success` |
| 특정 Task만 | + `--task-regex 'pattern'` |
| 단일 Task 디버그 | `airflow tasks test DAG_ID TASK_ID DATE` |

## 다음으로

→ [13. Catchup과 Schedule 동작](13-Catchup과-Schedule.md)
