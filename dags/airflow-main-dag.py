from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.contrib.hooks.ssh_hook import SSHHook
from airflow.contrib.operators.ssh_operator import SSHOperator
from datetime import datetime, timedelta
import pendulum

from airflow.hooks.base_hook import BaseHook
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator

def slack_failure_alert(context):
    
    slack_msg = """
            :red_circle: Task Failed. 
            *Task*: {task}  
            *Dag*: {dag} 
            *Execution Time*: {exec_date}  
            *Log Url*: {log_url} 
            """.format(
            task=context.get('task_instance').task_id,
            dag=context.get('task_instance').dag_id,
            ti=context.get('task_instance'),
            exec_date=pendulum.parse(context.get('ts')).in_tz('Africa/Cairo').to_iso8601_string(),
            log_url=context.get('task_instance').log_url,
        )
    failed_alert = SlackWebhookOperator(
        task_id='slack_alert',
        slack_webhook_conn_id = 'slack',
        message=slack_msg,
        username='airflow')
    return failed_alert.execute(context=context)

default_args={
        "depends_on_past": False,
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        'on_failure_callback': slack_failure_alert, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'on_skipped_callback': another_function, #or list of functions
        # 'trigger_rule': 'all_success'
    }

sshHook = SSHHook(ssh_conn_id="python-remote")
with DAG(
    dag_id="etl-logistics",
    # start_date=pendulum.datetime(2017, 1, 1, tz="UTC"),
    start_date=datetime(2025, 1, 31),
    catchup=False,
    schedule="0 0 * * *",
    default_args=default_args
):
    # 1. Generate data for the day
    generate_data = SSHOperator(
        task_id= "generate_fake_data",
        ssh_hook = sshHook,
        cmd_timeout = 60 * 15,
        command= "pythonn /usr/app/src/generate_fake_data.py medium"
    )

    # 2. load data to mysql
    prepare_load_data = SSHOperator(
        task_id= "prepare_and_load",
        ssh_hook = sshHook,
        command= "pythonn /usr/app/src/prepare_load.py"
    )

    # 3. Perform transformation 

    generate_data >> prepare_load_data
    
