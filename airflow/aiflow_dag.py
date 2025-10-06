from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.providers.microsoft.azure.operators.data_factory import AzureDataFactoryRunPipelineOperator

'''O uso do Airflow como orquestrador da pipeline não está disponível para as contas free do Azure,
portanto, segue apenas um exemplo de como seria a construção da DAG, fornecido no link:
https://learn.microsoft.com/pt-br/fabric/data-factory/apache-airflow-jobs-run-azure-data-factory-pipeline'''

with DAG(
    dag_id="run_open_brewery_adf_pipeline",
    start_date=datetime(2025, 10, 4),
    schedule_interval="@daily",
    catchup=False,  #Por padrão roda qualquer intervalo que não foi executado. False evita estas execuções.
    default_args={
        "retries": 1, #1 nova tentativa de execução se falha
        "retry_delay": timedelta(minutes=3), #Tempo de espera de 3 min entre as tentativas
        "azure_data_factory_conn_id": "azure_data_factory_conn_id", #Conexão criada no Airflow
    },
    default_view="graph",
) as dag:

    run_adf_pipeline = AzureDataFactoryRunPipelineOperator(
        task_id="run_adf_pipeline",
        pipeline_name="OpenBreweryPipeline",
    )

    run_adf_pipeline