from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

dag_list = ["Magellan", "Magellan_logis", "Aljex", "Aljex_Fox", "Aljex_HD", "Amil", "Circle",
            "Landstar", "Loads", "Mystic", "Parade", "BayAndBay", "Trucker_Tools"]

def create_dag(source_name):
    dag_id = f"{source_name}_parser_daily"

    default_args = {
        "start_date": datetime(2025, 4, 20),
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    }

    dag = DAG(
        dag_id=dag_id,
        schedule_interval="@daily",
        default_args=default_args,
        catchup=False,
        tags=["parser"]
    )

    with dag:
        run_parser = BashOperator(
            task_id=f"run_{source_name.lower()}",
            bash_command=f"cd /opt/acploads && PYTHONPATH=/opt/acploads python manage.py run_{source_name}",
        )

    dag.doc_md = f"DAG for running {source_name} parser."
    return dag

for source in dag_list:
    dag_id = f"{source}_parser_daily"
    globals()[dag_id] = create_dag(source)
