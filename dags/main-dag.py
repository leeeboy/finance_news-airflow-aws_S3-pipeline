from airflow import DAG
from airflow.decorators import task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.sdk import Variable
from datetime import timedelta, datetime
import os
import logging
from dags.python_scripts import get_data, transform_data, create_file, load_file_to_s3

bucket_name = os.environ['bucket_name']

default_args = {
        'owner' : 'Leela Lochan Madisetti',
        'retries' : 2,
        'retry_delay' : timedelta(minutes=1),
        'execution_timeout' : timedelta(hours=1)
      }

with DAG(
    dag_id = "finance-news_API_EXCEL_S3",
    default_args = default_args,
    start_date = datetime(2025, 1, 3),
    description = "This pipeline is intended to get finance news from Alpha Vantage API, transform the JSON to nested list, store the transformed data in .xlsx file and then load the .xlsx file into AWS S3 Bucket",
    schedule = '@hourly',
    catchup = False
)as dag:
    

    @task
    def get_api_data():
        try:
           logging.info("starting task to fetch raw json data from api")
           return get_data.get_data_frm_api()
        
        except Exception as e:
            logging.exception("get_api_data task failed")
    

    @task
    def transform_api_data(api_response):
        try:
           logging.info("starting task to tranform raw json api response to nested list")
           return transform_data.organise_data(api_response)
        
        except Exception as e:
            logging.exception("transform_api_data task failed")

    @task
    def load_excel(raw_data,ti, **kwargs):
        try:
           logging.info("strating task to create .xlsx file based on cleaned data")
           file_details = create_file.write_excel(raw_data)
           ti.xcom_push(key='file_details', value=file_details)

        except Exception as e:
            logging.exception("load_excel task failed")
    
    @task
    def upload_to_s3(ti, **kwargs):
        try:
           logging.info("starting task to upload local .xlsx file into aws s3")
           file_details = ti.xcom_pull(key='file_details', task_ids='load_excel')
           ti.xcom_push(key='file_name', value = f'temp/{file_details[1]}')
           load_file_to_s3.upload_to_s3(file_details)
        
        except Exception as e:
            logging.exception("upload_to_s3 task failed")
    
    wait_for_file = S3KeySensor(
        task_id = 'confirm_file_upload',
        aws_conn_id = 'aws_default',
        bucket_name = bucket_name,
        bucket_key = "{{ ti.xcom_pull(key='file_name', task_ids = 'upload_to_s3') }}",
        poke_interval = 60,
        timeout = 1800
    )




    api_response = get_api_data() 
    transformed_response = transform_api_data(api_response)
    load_excel(transformed_response) >> upload_to_s3() >> wait_for_file

