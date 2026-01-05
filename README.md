# Finance News ETL Pipeline (API → Excel → S3)
## 1. Project Overview

This project implements an Airflow ETL pipeline that fetches finance news data from the Alpha Vantage API, transforms it, stores it in an Excel file, and uploads it to an AWS S3 bucket. The pipeline is designed to be modular, production-ready, and scalable, making it suitable for recurring data ingestion and downstream analytics.
### DAG Architecture
<img width="1246" height="872" alt="finance-news_API_EXCEL_S3-graph" src="https://github.com/user-attachments/assets/cb0be3ce-0f54-4bd7-97ee-f00cd9718364" />

### Airflow DAG schedule
<img width="1920" height="1032" alt="image" src="https://github.com/user-attachments/assets/ed7dc4a0-1df1-48f3-b375-938603039ea8" />


### Key Features:

    Automated hourly data ingestion from an external API

    Data transformation to nested structured format

    Excel file creation and validation

    Upload to AWS S3 with file existence validation

    Task-level logging and failure alerts

    Designed with Airflow TaskFlow API for readability and maintainability

## 2. Architecture

The pipeline consists of the following components:

[Alpha Vantage API] → [Airflow DAG] → [Transform Data] → [Create Excel File] → [Upload to S3] → [Confirm Upload]


### Tasks and Flow

    get_api_data – Fetches JSON data from the Alpha Vantage API.

    transform_api_data – Converts the JSON into a nested list for easier Excel formatting.

    load_excel – Generates an Excel file from the transformed data.

    upload_to_s3 – Uploads the Excel file to the S3 temp/ folder and returns the S3 key.

    wait_for_file (S3KeySensor) – Confirms the file is uploaded successfully in S3 before downstream processes.

### Deployment:

DAGs are designed to run locally in Docker or on production Airflow environments (Astronomer, MWAA).

S3 access is managed via Airflow connections with AWS IAM credentials.

TaskFlow API ensures automatic dependency management, while deferrable sensors reduce worker load.

## 3. Future Scope

    Event-driven ingestion: Trigger DAG via S3 events instead of polling

    Data validation: Add schema checks for API responses before Excel generation

    Data warehousing: Extend DAG to load Excel data into Redshift, Snowflake, or BigQuery

    File promotion: Automatically move processed files from temp/ → processed/

    Monitoring dashboards: Integrate Slack or Grafana dashboards for metrics and alerts

    Scalable parallel processing: Support multiple API endpoints or tickers in parallel

## 4. How to Replicate This DAG
### Prerequisites

    Python 3.10+

    Docker & Docker Compose (for local Airflow)

    AWS Account with S3 bucket access

    Airflow 2.5+ with TaskFlow API

#### Step 1: Clone the Repository
git clone https://github.com/leeeboy/finance_news-airflow-aws_S3-pipeline.git

cd finance-news-etl

#### Step 2: Set Airflow Variables

Use Airflow UI or CLI to set bucket name:

airflow variables set FINANCE_NEWS_BUCKET "finance-news-stg-bucket"

Set AWS credentials via Airflow Connections:

    Conn ID: aws_default

    Conn Type: AWS

    Access Key / Secret Key / Region

#### Step 3: Run Airflow Locally
docker-compose up

#### Step 4: Deploy DAG

Place DAG file in dags/ folder

Ensure dags/python_scripts/ contains all helper scripts (get_data.py, transform_data.py, create_file.py, load_file_to_s3.py)

#### Step 5: Trigger DAG

Via Airflow UI or CLI:

airflow dags trigger finance_news_api_excel_s3

#### Step 6: Verify

Check logs for each task

Confirm Excel file appears in S3 temp/ folder
