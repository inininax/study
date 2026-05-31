# Airflow 학습 가이드

Apache Airflow를 처음 접하는 분들을 위한 한국어 학습 자료입니다.
**Web UI에서 단일 실행 / 백필 / Jinja 예약어** 사용법에 특히 초점을 맞췄습니다.

## 목차

### 0부. 빠른 체험 (★ 처음이라면 여기부터)

| # | 문서 | 핵심 내용 |
|---|------|----------|
| 00 | [30분 퀵스타트](docs/00-30분-퀵스타트.md) | 30분 안에 환경 띄우고 백필까지 한 번 체험 |

### 1부. Airflow 기초 개념

| # | 문서 | 핵심 내용 |
|---|------|----------|
| 01 | [Airflow 소개](docs/01-airflow-소개.md) | Airflow가 무엇인지, 왜 쓰는지 |
| 02 | [핵심 개념 (DAG / Task / Operator)](docs/02-핵심개념.md) | DAG, Task, Operator, TaskInstance |
| 03 | [Airflow 아키텍처](docs/03-아키텍처.md) | Scheduler, Executor, Webserver, Worker |

### 2부. 로컬 환경 구축 및 첫 DAG

| # | 문서 | 핵심 내용 |
|---|------|----------|
| 04 | [로컬 환경 구축](docs/04-로컬환경구축.md) | Docker Compose로 Airflow 띄우기 |
| 05 | [첫 번째 DAG 작성](docs/05-첫번째-DAG.md) | Hello World DAG |

### 3부. Web UI 가이드

| # | 문서 | 핵심 내용 |
|---|------|----------|
| 06 | [Web UI 개요](docs/06-WebUI-개요.md) | 메뉴 구성과 페이지 종류 |
| 07 | [DAG 목록 페이지](docs/07-WebUI-DAGs목록.md) | DAG 토글, 필터, 마지막 실행 보기 |
| 08 | [DAG 상세 화면](docs/08-WebUI-DAG상세화면.md) | Grid / Graph / Code / Logs / XCom |

### 4부. 단일 실행과 백필 (★ 핵심)

| # | 문서 | 핵심 내용 |
|---|------|----------|
| 09 | [DAG 실행 메커니즘](docs/09-DAG-실행메커니즘.md) | logical_date, data_interval, run_id |
| 10 | [Web UI에서 단일 실행 (Trigger)](docs/10-단일실행-Trigger.md) | ▶ 버튼, conf 전달, 파라미터 설정 |
| 11 | [Web UI에서 백필 (Backfill)](docs/11-백필-WebUI.md) | Backfill 모달, dry-run, 정렬 |
| 12 | [CLI 백필 명령어](docs/12-백필-CLI.md) | `airflow dags backfill` 옵션 전체 |
| 13 | [Catchup과 Schedule 동작](docs/13-Catchup과-Schedule.md) | catchup=True/False, max_active_runs |

### 5부. Template 예약어 / 매크로 (★ 핵심)

| # | 문서 | 핵심 내용 |
|---|------|----------|
| 14 | [Jinja Template 기초](docs/14-Jinja-Template.md) | `{{ }}` 문법, template_fields |
| 15 | [예약어 전체 레퍼런스](docs/15-예약어-전체레퍼런스.md) | **`ds`, `ts`, `data_interval_*`, `logical_date` 등 빠짐 없이 정리** |
| 16 | [매크로 함수](docs/16-매크로함수.md) | `macros.ds_add`, `macros.datetime` 등 |

### 6부. 실전 활용

| # | 문서 | 핵심 내용 |
|---|------|----------|
| 17 | [Variables / Connections / XCom](docs/17-Variables-Connections-XCom.md) | 외부 시스템 연동, 값 공유 |
| 18 | [실전 시나리오](docs/18-실전시나리오.md) | 실패한 Task 재실행, 과거 데이터 채우기 |

### 7부. 손에 자주 두는 레퍼런스

| # | 문서 | 핵심 내용 |
|---|------|----------|
| 19 | [용어집 (Glossary)](docs/19-용어집.md) | DAG / Task / Operator / Sensor / Pool 등 모든 용어 |
| 20 | [치트시트](docs/20-치트시트.md) | 예약어 / 매크로 / CLI / SQL 패턴 한 장 요약 |
| 21 | [트러블슈팅 FAQ](docs/21-트러블슈팅-FAQ.md) | 증상 → 원인 → 해결 패턴별 진단 가이드 |

## 빠른 시작

```bash
# 0. .env 준비 (최초 1회, Linux는 AIRFLOW_UID 수정)
cp .env.example .env

# 1. Airflow 초기화 (최초 1회)
docker compose up airflow-init

# 2. Airflow 기동
docker compose up -d

# 3. Web UI 접속
open http://localhost:8080
# 기본 계정: airflow / airflow
```

상세 절차는 [04-로컬환경구축.md](docs/04-로컬환경구축.md)를 참고하세요.

## 학습 순서 추천

```
[처음이면]      00 (30분 퀵스타트)
                  ↓
[기초 개념]     01 → 02 → 03
                  ↓
[환경 + 첫 DAG] 04 → 05
                  ↓
[Web UI]        06 → 07 → 08
                  ↓
[실행 메커니즘] 09 → 10 → 11 → 12 → 13
                  ↓
[예약어 마스터] 14 → 15 → 16
                  ↓
[실전]          17 → 18

[항상 옆에 둘 것]
  19 (용어집)    — 모르는 용어 만났을 때
  20 (치트시트)  — 명령어 / 예약어 까먹었을 때
  21 (FAQ)       — 안 돌아갈 때
```

## 예제 DAG 파일

`dags/` 디렉토리에 학습용 DAG가 들어 있습니다.

- `01_hello_airflow.py` — 가장 단순한 DAG
- `02_template_variables.py` — `ds`, `ts`, `data_interval_*` 등 모든 예약어 출력
- `03_branching_example.py` — BranchPythonOperator로 분기
- `04_backfill_demo.py` — 백필 실습용 (catchup=True)

## 이미지 / 스크린샷

`docs/images/` 폴더에 학습 중 캡처해야 할 스크린샷 가이드가 있습니다.
대부분의 다이어그램은 **Mermaid** 포맷으로 작성되어 GitHub, VS Code 등에서 자동 렌더링됩니다.

## 참고 자료

- 공식 문서: https://airflow.apache.org/docs/
- Templates Reference: https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html
- 본 가이드 작성 기준 버전: **Airflow 2.9.x** (Airflow 3.x 차이점은 별도 표기)
