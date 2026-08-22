"""
03_branching_example.py

BranchPythonOperator로 조건 분기 시연.

학습 포인트:
- Trigger DAG w/ config 화면에서 conf로 분기 조건 전달
- {{ dag_run.conf }} 활용
- TriggerRule (분기 후 합류 노드의 트리거 규칙)
"""
from __future__ import annotations

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule


def choose_branch(**context):
    """conf에 mode=premium이 들어오면 process_premium, 아니면 process_basic으로."""
    conf = context["dag_run"].conf or {}
    mode = conf.get("mode", "basic")
    if mode == "premium":
        return "process_premium"
    return "process_basic"


with DAG(
    dag_id="03_branching_example",
    description="conf로 분기하는 DAG",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule=None,   # 수동 트리거 전용
    catchup=False,
    tags=["learning", "branching"],
) as dag:

    start = EmptyOperator(task_id="start")

    branch = BranchPythonOperator(
        task_id="branch",
        python_callable=choose_branch,
    )

    process_basic = BashOperator(
        task_id="process_basic",
        bash_command="echo 'basic 처리: ds={{ ds }}'",
    )

    process_premium = BashOperator(
        task_id="process_premium",
        bash_command="echo 'premium 처리: ds={{ ds }}'",
    )

    # branch에서 선택되지 않은 쪽은 skipped 상태가 되므로,
    # join은 NONE_FAILED_MIN_ONE_SUCCESS 트리거 규칙을 써야 함
    join = EmptyOperator(
        task_id="join",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    start >> branch >> [process_basic, process_premium] >> join
