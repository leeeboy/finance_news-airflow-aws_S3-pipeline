from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import os
import logging

def upload_to_s3(file_details):

    s3_hook = S3Hook(aws_conn_id = "aws_default")
    # file_details =  [filepath, filename]
    bucket_name = os.environ['bucket_name']
    s3_hook.load_file(filename=file_details[0], key = f"temp/{file_details[1]}",bucket_name=bucket_name, replace=True)
    logging.info(f"s3 key for the file is {file_details[1]}")

