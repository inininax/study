"""
04_backfill_demo.py

백필 학습 전용 DAG. catchup=True로 두면 start_date 이후의 모든 logical_date에 대한
DAGRun이 자동으로 채워진다. (단, max_active_runs로 동시 실행을 1개로 제한)

⚠ 주의 (학습자에게 중요)
- 본 DAG의 토글을 ON 하는 순간 start_date(2026-04-01) ~ 현재 사이의 모든 일자
  DAGRun이 자동 큐잉된다. 며칠치만 체험하고 싶다면 토글을 ON 하지 말고
  CLI `airflow dags backfill` 로 명시적 범위로만 실행하는 것을 권장.
- 의도치 않게 큐잉된 DAGRun을 정리하려면:
    docker compose exec airflow-scheduler \\
      airflow tasks clear 04_backfill_demo -s 2026-04-01 -e 2026-12-31 -y

학습 포인트:
- start_date를 과거로 두고 catchup=True
- max_active_runs=1로 순차 실행
- {{ data_interval_start }}, {{ data_interval_end }} 의미
- Web UI Backfill 버튼 vs CLI airflow dags backfill
"""
from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="04_backfill_demo",
    description="백필 시연용 DAG (catchup=True)",
    start_date=datetime(2026, 4, 1),
    end_date=None,
    schedule="@daily",
    catchup=True,                # ★ 과거 미실행 구간 자동 채움
    max_active_runs=1,           # ★ 동시 실행 제한 (백필 시 순차)
    default_args={
        "retries": 1,
    },
    tags=["learning", "backfill"],
) as dag:

    show_interval = BashOperator(
        task_id="show_interval",
        bash_command=r"""
echo "처리할 데이터 구간"
echo "  data_interval_start = {{ data_interval_start }}"
echo "  data_interval_end   = {{ data_interval_end }}"
echo "  ds                  = {{ ds }}"
echo "→ '{{ ds }}' 일자 데이터를 처리한다고 가정"
""",
    )

    fake_extract = BashOperator(
        task_id="fake_extract",
        bash_command="echo 'SELECT * FROM source WHERE event_date = \"{{ ds }}\"'",
    )

    fake_load = BashOperator(
        task_id="fake_load",
        bash_command="echo 'INSERT INTO mart_daily PARTITION (dt=\"{{ ds }}\") ...'",
    )

    show_interval >> fake_extract >> fake_load
