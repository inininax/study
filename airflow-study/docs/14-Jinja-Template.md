# 14. Jinja Template 기초

Airflow는 **Jinja2** 템플릿 엔진을 내장하여, Operator의 일부 인자에 `{{ ... }}` 표현식을 쓰면 Task가 실제로 실행되는 시점에 값으로 치환합니다.

## 왜 필요한가?

```python
# ❌ 잘못된 예 — 파싱 시점의 값이 고정되어 매일 같은 날짜
from datetime import date
BashOperator(
    task_id="t",
    bash_command=f"aws s3 cp s3://b/{date.today()}/ ./",
)

# ✅ 옳은 예 — Task 실행 시점의 logical_date가 들어감
BashOperator(
    task_id="t",
    bash_command="aws s3 cp s3://b/{{ ds }}/ ./",
)
```

## 기본 문법

```jinja
{{ ds }}                          # 변수
{{ ds | upper }}                  # 필터 (문자열 메서드)
{% if x > 0 %}A{% else %}B{% endif %}    # 조건문
{% for item in items %}{{ item }}{% endfor %}  # 반복
```

## template_fields

**모든 Operator 인자가 Jinja 템플릿이 되는 것은 아닙니다.** 각 Operator 클래스의 `template_fields` 속성에 명시된 인자만 템플릿됩니다.

대표적인 Operator의 template_fields:

| Operator | template_fields |
|----------|----------------|
| `BashOperator` | `('bash_command', 'env', 'cwd')` |
| `PythonOperator` | `('templates_dict', 'op_args', 'op_kwargs')` |
| `PostgresOperator` / `MySqlOperator` | `('sql',)` |
| `EmailOperator` | `('to', 'subject', 'html_content', 'files')` |
| `S3KeySensor` | `('bucket_key', 'bucket_name')` |

> 즉 `BashOperator`의 `task_id`에 `{{ ds }}`를 써도 **치환되지 않습니다.**

## PythonOperator에서 Jinja 쓰기

`python_callable`은 함수 객체라 직접 Jinja를 쓸 수 없습니다. 대신:

### 방법 1: **context로 받기**

```python
def my_func(**context):
    ds = context["ds"]
    print(f"오늘은 {ds}")

PythonOperator(task_id="t", python_callable=my_func)
```

### 방법 2: `op_kwargs`에 Jinja

```python
def my_func(today: str):
    print(f"오늘은 {today}")

PythonOperator(
    task_id="t",
    python_callable=my_func,
    op_kwargs={"today": "{{ ds }}"},   # ← op_kwargs는 template_fields라 치환됨
)
```

### 방법 3: `templates_dict`

```python
def my_func(**context):
    ds = context["templates_dict"]["my_date"]
    print(ds)

PythonOperator(
    task_id="t",
    python_callable=my_func,
    templates_dict={"my_date": "{{ ds }}"},
)
```

## TaskFlow API에서 Jinja

`@task` 데코레이터의 인자도 Jinja가 적용됩니다.

```python
@task
def process(today: str = "{{ ds }}"):
    print(today)
```

또는 `context`를 직접 받기:

```python
from airflow.decorators import task

@task
def process():
    from airflow.operators.python import get_current_context
    ctx = get_current_context()
    print(ctx["ds"])
```

## template_searchpath — 외부 SQL/HTML 파일

`.sql`이나 `.html` 파일을 별도로 두고 템플릿할 수 있습니다.

```
project/
  dags/
    my_dag.py
    sql/
      query.sql
```

```python
with DAG(
    ...,
    template_searchpath="/opt/airflow/dags/sql",
) as dag:
    PostgresOperator(
        task_id="t",
        sql="query.sql",   # 파일명만 적으면 자동으로 찾아서 Jinja 렌더링
    )
```

```sql
-- sql/query.sql
SELECT * FROM events
WHERE event_date = '{{ ds }}'
  AND region    = '{{ params.region }}';
```

## 자주 쓰는 패턴

### 날짜 필터 SQL

```jinja
WHERE event_date = '{{ ds }}'
WHERE ts >= '{{ data_interval_start }}'
  AND ts <  '{{ data_interval_end }}'
WHERE event_date = '{{ macros.ds_add(ds, -1) }}'   -- 어제
```

### 파일 경로

```jinja
s3://bucket/raw/{{ ds_nodash }}/data.parquet
/data/snapshots/dt={{ ds }}/region={{ params.region }}/
```

### 조건부 명령

```jinja
{% if dag_run.conf.get('dry_run') %}
  echo "DRY RUN — no changes"
{% else %}
  python /opt/airflow/scripts/load.py --date {{ ds }}
{% endif %}
```

### XCom pull

```jinja
{{ ti.xcom_pull(task_ids='extract', key='row_count') }}
```

## 디버깅: Rendered Template 탭

UI에서 Task 셀 클릭 → 우측 패널 → **Rendered Template** 탭.
Jinja가 실제 어떤 값으로 치환됐는지 확인할 수 있습니다. **Jinja가 의심스러울 땐 항상 여기를 먼저** 보세요.

📷 캡처 권장: `docs/images/14-01-rendered-template.png`

## CLI로 Jinja 결과 미리 보기

```bash
docker compose exec airflow-scheduler \
  airflow tasks render 02_template_variables print_via_bash 2026-01-03
```

→ 해당 Task의 모든 template_fields가 어떻게 렌더링되는지 출력.

## 다음으로

→ [15. 예약어 전체 레퍼런스 ★](15-예약어-전체레퍼런스.md)
