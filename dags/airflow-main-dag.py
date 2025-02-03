from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.contrib.hooks.ssh_hook import SSHHook
from airflow.contrib.operators.ssh_operator import SSHOperator
from datetime import datetime, timedelta

# save
default_args={
        "depends_on_past": False,
        "email": ["belaghoury1@gmail.com"],
        "email_on_failure": True,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'on_skipped_callback': another_function, #or list of functions
        # 'trigger_rule': 'all_success'
    }

sshHook = SSHHook(ssh_conn_id="python-remote")
with DAG(
    dag_id="etl-logistics",
    start_date=datetime(2025, 1, 31),
    catchup=False,
    schedule="0 0 * * *",
):
    test_connection = SSHOperator(
        task_id= "test_connection",
        ssh_hook = sshHook,
        command= "python /usr/src/app/test_connection.py"
    )
    
