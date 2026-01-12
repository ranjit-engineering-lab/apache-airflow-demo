from datetime import datetime, timedelta
from io import StringIO
import os

from airflow.sdk import dag, task, chain, get_current_context
from airflow.sdk.bases.sensor import PokeReturnValue
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.standard.operators.python import BranchPythonOperator


import pandas as pd

AWS_CONN_ID = 'ensf-aws'
BUCKET_NAME = 'ensf612bucket'

POSTGRES_CONN_ID = "user_postgres"
TABLE_NAME = "public.walmart_sales_transformed"

LOCAL_DATA_DIR = "/opt/airflow/data/extracted"


@dag(
3...
)
def etl_pipeline_dag():

    @task(task_id="TransformData")
    def transform():
        file_path = LOCAL_DATA_DIR + "/walmart_sales.csv"
        df = pd.read_csv(file_path)
        df = df.dropna()
        df['Date'] = pd.to_datetime(df['Date'])
        markdown_cols = ["MarkDown1","MarkDown2","MarkDown3","MarkDown4","MarkDown5"]
        df['promo_intensity'] = df[markdown_cols].sum(axis=1)

        df.columns = [col.lower().replace(' ', '_') for col in df.columns]

        df_transformed = df.groupby(['store','date']).agg({
            'temperature': 'mean',
            'fuel_price': 'mean',
            'promo_intensity': 'sum',
            'isholiday': 'max',
            'cpi': 'mean',
            'unemployment': 'mean'
        }).reset_index()

        cleaned_path = LOCAL_DATA_DIR + "/walmart_sales_transformed.csv"
        df_transformed.to_csv(cleaned_path, index=False)
        return cleaned_path
    
   
