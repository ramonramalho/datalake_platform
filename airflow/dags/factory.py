

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator
from dags.airflow_utils import Utils
from airflow.utils.task_group import TaskGroup
from operator_factory import OperatorFactory

for yml in Utils.load_yml('.'):
# Definindo o DAG
    with DAG(
        dag_id=yml.get('dag_id'),
        start_date=days_ago(1),
        schedule_interval=yml.get('schedule'),
        catchup=False,
        is_paused_upon_creation=True,
        # retries=int(yml.get("retries"))
    ) as dag:

        start = DummyOperator(task_id='start', dag=dag)
        end = DummyOperator(task_id='end', dag=dag)
        
        tgs = []
        for task in yml.get('tasks'):
            with TaskGroup(group_id=f"tg_{task.get('task_id')}") as tg:
                operator_type = task.get("operator")
                strategy = OperatorFactory.get_strategy(operator_type)
                task = strategy.create_operator(task, dag)
            tgs.append(tg)

        start >> tgs >> end
