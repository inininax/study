"""
02_template_variables.py

Airflow의 Jinja Template 예약어를 한 번에 모두 출력해보는 DAG.

학습 포인트:
- {{ ds }}, {{ ts }}, {{ data_interval_start }} 등 빠짐없이 출력
- BashOperator의 bash_command는 자동으로 Jinja 렌더링됨
- PythonOperator는 **context로 같은 값을 받음
"""
from __future__ import annotations

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def print_all_context(**context):
    """PythonOperator에서는 context dict로 동일한 값을 받을 수 있다."""
    keys_of_interest = [
        "ds", "ds_nodash",
        "ts", "ts_nodash", "ts_nodash_with_tz",
        "logical_date", "data_interval_start", "data_interval_end",
        "prev_data_interval_start_success", "prev_data_interval_end_success",
        "next_ds", "next_ds_nodash",
        "prev_ds", "prev_ds_nodash",
        "run_id", "dag_run", "task_instance_key_str",
        "dag", "task",
    ]
    print("===== Airflow Context Variables =====")
    for k in keys_of_interest:
        v = context.get(k, "<missing>")
        print(f"{k:40s} = {v!r}")
    print("=====================================")


with DAG(
    dag_id="02_template_variables",
    description="Jinja 예약어 전체를 한 번에 보기",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    tags=["learning", "templates"],
) as dag:

    # BashOperator: bash_command가 Jinja로 자동 렌더됨
    print_via_bash = BashOperator(
        task_id="print_via_bash",
        bash_command=r"""
echo "===== Bash에서 본 Jinja 예약어 ====="
echo "ds                       = {{ ds }}"
echo "ds_nodash                = {{ ds_nodash }}"
echo "ts                       = {{ ts }}"
echo "ts_nodash                = {{ ts_nodash }}"
echo "ts_nodash_with_tz        = {{ ts_nodash_with_tz }}"
echo "logical_date             = {{ logical_date }}"
echo "data_interval_start      = {{ data_interval_start }}"
echo "data_interval_end        = {{ data_interval_end }}"
echo "next_ds                  = {{ next_ds }}"
echo "next_ds_nodash           = {{ next_ds_nodash }}"
echo "prev_ds                  = {{ prev_ds }}"
echo "prev_ds_nodash           = {{ prev_ds_nodash }}"
echo "run_id                   = {{ run_id }}"
echo "task_instance_key_str    = {{ task_instance_key_str }}"
echo "dag.dag_id               = {{ dag.dag_id }}"
echo "task.task_id             = {{ task.task_id }}"
echo "===== 매크로 함수 사용 예시 ====="
echo "어제 날짜               = {{ macros.ds_add(ds, -1) }}"
echo "내일 날짜               = {{ macros.ds_add(ds, 1) }}"
echo "ds 포맷 변경 (YYYYMMDD) = {{ macros.ds_format(ds, '%Y-%m-%d', '%Y%m%d') }}"
echo "===================================="
""",
    )

    print_via_python = PythonOperator(
        task_id="print_via_python",
        python_callable=print_all_context,
    )

    print_via_bash >> print_via_python
