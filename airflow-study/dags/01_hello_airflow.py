"""
01_hello_airflow.py

가장 단순한 DAG. Airflow가 정상 동작하는지 확인하는 용도.

학습 포인트:
- DAG 정의 방법 (with 블록)
- BashOperator / PythonOperator 사용
- Task 의존성 표기 (>> 연산자)
"""
from __future__ import annotations

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def say_hello(**context):
    print("Hello, Airflow!")
    print(f"이 Task의 logical_date: {context['logical_date']}")
    print(f"이 Task의 task_id: {context['task'].task_id}")
    return "hello-from-python"


with DAG(
    dag_id="01_hello_airflow",
    description="가장 단순한 학습용 DAG",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    tags=["learning", "intro"],
) as dag:

    start = BashOperator(
        task_id="start",
        bash_command="echo '=== DAG 시작 ==='",
    )

    hello = PythonOperator(
        task_id="say_hello",
        python_callable=say_hello,
    )

    end = BashOperator(
        task_id="end",
        bash_command="echo '=== DAG 종료 ==='",
    )

    start >> hello >> end
