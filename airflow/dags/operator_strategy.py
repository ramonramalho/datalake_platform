from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.operators.emr import EmrServerlessCreateApplicationOperator, EmrServerlessStartJobOperator, EmrServerlessDeleteApplicationOperator

class OperatorStrategy:
    """Classe base para todas as estratégias de operadores."""
    
    def create_operator(self, task_config, dag):
        raise NotImplementedError("Deve ser implementado nas subclasses.")

class BashOperatorStrategy(OperatorStrategy):
    """Estratégia para criar um BashOperator."""
    
    def create_operator(self, task_config, dag):
        return BashOperator(
            task_id=task_config.get('task_id'),
            bash_command=task_config['bash_command'],
            dag=dag
        )

class EMRServerlessOperator(OperatorStrategy):
    def create_operator(self, task_config, dag):
        create_app = EmrServerlessCreateApplicationOperator(
            task_id=f"{task_config.get('task_id')}_create_spark_app",
            job_type="SPARK",
            release_label="emr-6.6.0",
            config={
                "name": f"{task_config.get('task_id')}",
                "runtime-configuration" : [task_config.get("runtime_configuration")]},
        )

        application_id = create_app.output
        
        start_app = EmrServerlessStartJobOperator(
            task_id=f"emr_{task_config.get('task_id')}",
            application_id=application_id,
            execution_role_arn=task_config.get('execution_role_arn'),
            job_driver={
                'sparkSubmit': {
                    'entryPoint': task_config.get('entrypoint'),
                    'entryPointArguments': task_config.get('args'),
                    "sparkSubmitParameters": "--conf spark.submit.pyFiles=s3://prod-datalake-artifacts/jobs/delta.py  --conf spark.executor.cores=1 --conf spark.executor.memory=4g --conf spark.driver.cores=1 --conf spark.driver.memory=4g --conf spark.executor.instances=1 --conf spark.dynamicAllocation.maxExecutors=1",
                }
            },
            configuration_overrides={
                'monitoringConfiguration': {
                    's3MonitoringConfiguration': {}
                }
            }
        )

        delete_app = EmrServerlessDeleteApplicationOperator(
            task_id=f"{task_config.get('task_id')}_delete_spark_app",
            application_id=application_id,
            trigger_rule="all_done",
        ) 

        return [create_app >>  start_app >> delete_app]
    