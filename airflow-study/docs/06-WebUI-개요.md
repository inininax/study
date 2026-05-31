# 06. Web UI 개요

http://localhost:8080 으로 접속한 직후 보이는 화면 구성을 정리합니다.

## 전체 레이아웃

```
┌────────────────────────────────────────────────────────────────────────┐
│ [≡] Airflow   DAGs  Datasets  Security  Browse  Admin  Docs           │ ← 상단 네비게이션
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│ DAGs (메인 영역)                                                       │
│ [● All] [Active] [Paused] [Running] [Failed]    🔍 Search   ⚙ filter   │
│ ─────────────────────────────────────────────────────────────────────  │
│  [●] dag_id              schedule     last run   recent  next   ...   │
│  ...                                                                   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

📷 캡처 권장: `docs/images/06-01-overview.png`

## 상단 네비게이션 메뉴

| 메뉴 | 용도 |
|------|------|
| **DAGs** | DAG 목록 (메인) |
| **Datasets** | Dataset 기반 트리거 그래프 (2.4+) |
| **Security** | Users / Roles / Permissions |
| **Browse** | DAG Runs / Task Instances / Logs / Audit logs / Jobs / SLA Misses |
| **Admin** | Variables / Connections / XComs / Pools / Configurations / Plugins |
| **Docs** | 공식 문서, REST API, 버전 정보 |

## "Browse" 하위 메뉴 — 운영 시 가장 많이 보는 화면들

| 화면 | 무엇을 보나? |
|------|-------------|
| **DAG Runs** | 모든 DAG의 실행 이력 한 번에 (필터·검색 가능) |
| **Task Instances** | 모든 Task의 실행 이력. **상태별 한 번에 일괄 처리 가능** |
| **Task Logs** | Task별 로그 (영구 저장 위치) |
| **Audit Logs** | 누가 언제 무엇을 했는지 (트리거, clear, 백필 등) |
| **Jobs** | Scheduler / Triggerer / Worker 잡 상태 |
| **SLA Misses** | SLA 위반 |

## "Admin" 하위 메뉴 — 설정 화면들

| 화면 | 용도 |
|------|------|
| **Variables** | 키-값 저장소. DAG에서 `Variable.get('key')` 또는 `{{ var.value.key }}`로 접근 |
| **Connections** | 외부 시스템 접속 정보 (DB, S3, Slack 등). DAG에서 `conn_id`로 참조 |
| **XComs** | Task 간 작은 데이터 전달 이력 |
| **Pools** | Task 동시 실행 수를 제한하는 슬롯 |
| **Configurations** | airflow.cfg 내용 |
| **Plugins** | 로드된 플러그인 |

자세한 사용법은 [17. Variables/Connections/XCom](17-Variables-Connections-XCom.md).

## 우측 상단 아이콘들

```
... [🕒 Time zone] [👤 사용자] [Help]
```

- **🕒 Time zone**: UTC / Local / DAG Time zone 토글. **시각 표기에만** 영향 (예: `2026-01-03 00:00 UTC`를 `2026-01-03 09:00 KST`로 보여줌). 토글을 바꿔도 메타DB에 저장된 `logical_date` 값은 **항상 UTC 그대로**이며, DAG의 schedule 동작도 변하지 않습니다.
- **사용자 메뉴**: 비밀번호 변경 / 로그아웃.

## DAGs 목록 페이지

가장 많이 보는 화면입니다. 별도 문서에서 자세히 다룹니다.

→ [07. DAG 목록 페이지](07-WebUI-DAGs목록.md)

## DAG 상세 페이지

DAG 이름을 클릭하면 진입. 여러 탭으로 구성.

| 탭 | 보여주는 것 |
|----|-----------|
| **Grid** | 시간축으로 DAGRun과 Task 상태를 격자로 (★ 가장 많이 봄) |
| **Graph** | DAG 그래프 시각화 |
| **Calendar** | 월/일 단위 성공/실패 캘린더 |
| **Task Duration** | Task별 실행 시간 추이 |
| **Task Tries** | 재시도 횟수 추이 |
| **Landing Times** | logical_date 대비 실제 시작 시각 지연 |
| **Gantt** | 한 DAGRun의 Task별 시간축 (병렬도 파악) |
| **Code** | DAG 소스 코드 |
| **Audit Log** | 이 DAG에 대한 액션 이력 |

→ [08. DAG 상세 화면](08-WebUI-DAG상세화면.md)

## 색상 코드 (전 화면 공통)

| 색 | 상태 |
|----|------|
| ⚪ 회색 | none / queued / no_status |
| 🔵 라이트 블루 | scheduled |
| 🟢 라이트 그린 | running |
| 🟢 다크 그린 | success |
| 🔴 빨강 | failed |
| 🟠 오렌지 | up_for_retry |
| 🟡 노랑 | up_for_reschedule (Sensor) |
| 🟣 보라 | upstream_failed |
| 🟤 갈색 | shutdown |
| ⚫ 검정 | removed |
| 🌑 진회색 | skipped |

각 화면 우측에 범례(Legend)가 있으니 헷갈릴 때 확인.

📷 캡처 권장: `docs/images/06-02-status-legend.png`

## 다음으로

→ [07. DAG 목록 페이지](07-WebUI-DAGs목록.md)
