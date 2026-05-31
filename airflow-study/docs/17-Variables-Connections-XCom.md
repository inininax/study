# 17. Variables / Connections / XCom

DAG에서 **외부 정보 / 비밀 / Task 간 값 전달**을 다루는 3가지 메커니즘.

## Variable — 단순 키-값 저장소

UI: **Admin → Variables**

```
┌──────────────────────────────────────────────┐
│ Variables                                    │
│ [+ Add Variable]                             │
│ ─────────────────────────────────────────── │
│  Key             Value                       │
│  region          kr                          │
│  email_to        ops@example.com             │
│  api_config      {"host":"a.com","port":443} │
└──────────────────────────────────────────────┘
```

📷 캡처 권장: `docs/images/17-01-variables.png`

### DAG에서 사용

#### Python에서

```python
from airflow.models import Variable

region = Variable.get("region", default_var="kr")
config = Variable.get("api_config", default_var={}, deserialize_json=True)
```

#### Jinja에서

```jinja
{{ var.value.region }}                          → "kr"
{{ var.value.get('region', 'kr') }}             → "kr"
{{ var.json.api_config.host }}                  → "a.com"
```

### CLI

```bash
airflow variables set region kr
airflow variables get region
airflow variables list
airflow variables delete region
```

> **주의**: Variable.get을 DAG 파일 **최상위**에서 호출하면 매 파싱마다 DB를 친다 → Scheduler 부하. 반드시 **Task 함수 안**에서 사용.

## Connection — 외부 시스템 접속 정보

UI: **Admin → Connections**

| 필드 | 의미 | 예 |
|------|------|----|
| Connection Id | DAG에서 참조하는 ID | `my_postgres` |
| Connection Type | DB/HTTP/AWS/SSH 등 | `Postgres` |
| Host | 호스트 | `db.internal` |
| Schema (Database) | DB 이름 | `analytics` |
| Login | 사용자 | `airflow` |
| Password | 비밀번호 | `***` |
| Port | 포트 | `5432` |
| Extra | JSON 추가 옵션 | `{"sslmode":"require"}` |

📷 캡처 권장: `docs/images/17-02-connections.png`

### DAG에서 사용

```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

PostgresOperator(
    task_id="t",
    postgres_conn_id="my_postgres",
    sql="SELECT count(*) FROM events WHERE dt='{{ ds }}'",
)
```

```jinja
{{ conn.my_postgres.host }}
{{ conn.my_postgres.password }}
{{ conn.my_postgres.extra_dejson.sslmode }}
```

> **운영 환경**에서는 Variables/Connections를 메타DB에 평문 저장하지 말고 [Secrets Backend](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/) (Vault, AWS Secrets Manager 등)를 사용하세요.

### CLI

```bash
airflow connections add my_postgres \
  --conn-type postgres \
  --conn-host db.internal \
  --conn-port 5432 \
  --conn-login airflow \
  --conn-password 'secret' \
  --conn-schema analytics
```

## XCom — Task 간 값 전달

XCom = "**X**-Communication". Task가 작은 값(JSON-serializable)을 다른 Task에 넘기는 메커니즘.

### Push (값 저장)

#### 방법 1: 함수 반환값 (가장 흔함)

```python
def extract(**context):
    return 42

def transform(**context):
    value = context["ti"].xcom_pull(task_ids="extract")
    print(value)
```

PythonOperator의 함수 return값은 **자동으로 XCom push** (key=`return_value`).

#### 방법 2: 명시적 push

```python
def extract(**context):
    context["ti"].xcom_push(key="row_count", value=100)
    context["ti"].xcom_push(key="last_id", value="A123")
```

#### 방법 3: TaskFlow API

```python
@task
def extract():
    return {"rows": 100}

@task
def transform(data: dict):
    return data["rows"] * 2

transform(extract())   # 자동으로 XCom 연결
```

### Pull (값 꺼내기)

```python
# 같은 DAGRun의 다른 Task에서
ti.xcom_pull(task_ids="extract")                       # return_value
ti.xcom_pull(task_ids="extract", key="row_count")      # 특정 key
ti.xcom_pull(task_ids=["extract", "extract2"])         # 여러 Task → list
ti.xcom_pull(task_ids="extract", include_prior_dates=True)  # 과거 logical_date도
```

### Jinja에서

```jinja
{{ ti.xcom_pull(task_ids='extract') }}
{{ ti.xcom_pull(task_ids='extract', key='row_count') }}
```

### XCom 크기 제한

XCom은 메타DB에 저장되므로 큰 데이터를 담으면 안 됩니다.
- **권장**: 수 KB 이내의 메타정보만 (count, file path, ID 등)
- **금지**: DataFrame, 큰 JSON
- 큰 데이터는 S3/GCS에 저장하고 **경로**만 XCom으로 전달

### XCom 보기

UI: **Admin → XComs** 또는 Task 셀 클릭 → **XCom** 탭.

📷 캡처 권장: `docs/images/17-03-xcom.png`

## 정리

| 용도 | 사용 |
|------|------|
| 환경 설정 / 운영 파라미터 | **Variable** |
| 외부 시스템 접속 정보 / 비밀 | **Connection** (+ Secrets Backend in prod) |
| Task 간 작은 값 전달 | **XCom** |
| 트리거 시 일회성 입력 | **dag_run.conf** |
| DAG 정의 시 정적 입력 | **params** |

## 다음으로

→ [18. 실전 시나리오](18-실전시나리오.md)
