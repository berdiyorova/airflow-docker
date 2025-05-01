from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

dag_list = [
    "Magellan", "Magellan_logis", "Aljex", "Aljex_Fox", "Aljex_HD", "Amil",
    "Circle", "Landstar", "Loads", "Mystic", "Parade", "BayAndBay", "Trucker_Tools",
]

VENV = "/opt/acploads/venv"

def create_dag(src):
    dag = DAG(
        dag_id=f"{src}_parser_hourly",
        schedule_interval="@hourly",
        default_args={
            "start_date": datetime(2025, 4, 20),
            "retries": 1,
            "retry_delay": timedelta(minutes=5),
        },
        catchup=False,
        tags=["parser"],
    )

    cmd = rf"""
        if [ ! -d {VENV} ]; then
            python -m venv {VENV} &&
            {VENV}/bin/pip install --no-cache-dir -r /opt/acploads/requirements.txt
        fi
        cd /opt/acploads &&
        PYTHONPATH=/opt/acploads {VENV}/bin/python manage.py run_{src}
    """

    with dag:
        BashOperator(
            task_id=f"run_{src.lower()}",
            bash_command=cmd,
        )

    return dag

for s in dag_list:
    globals()[f"{s}_parser_hourly"] = create_dag(s)
