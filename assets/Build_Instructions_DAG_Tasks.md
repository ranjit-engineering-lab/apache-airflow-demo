
# Airflow ETL Pipeline — DAG & Task Build Instructions

These instructions describe only the steps required to construct the DAG and tasks for your ETL pipeline in Apache Airflow.

![dag image](./A4_etl_pipeline_dag-graph.png)

---

## 1. Create the DAG File

Create a new file inside your Airflow `dags/` directory:

```
etl_pipeline_dag.py
```

Define a DAG with the following properties:

- **dag_id:** `A4_etl_pipeline_dag`
- **schedule:** `@daily`
- **start_date:** January 1, 2024  
- **catchup:** `False`
- **tags:** include `"etl"`

---

## 2. Define Required Constants

At the top of your DAG file, define constants for:

```
AWS_CONN_ID = 'ensf-aws'
BUCKET_NAME = 'ensf612bucket'
POSTGRES_CONN_ID = 'user_postgres'
TABLE_NAME = 'public.walmart_sales_transformed'
LOCAL_DATA_DIR = '/opt/airflow/data/extracted'
```

---

## 3. Task: ExtractFromS3

Create a **TaskFlow** task that:

1. Ensures the local extraction directory exists  
2. Reads `walmart_sales.csv` from your S3 bucket using `S3Hook`  
3. Writes the file locally to:

```
/opt/airflow/data/extracted/walmart_sales.csv
```

4. Returns the **local file path**

---

## 4. Sensor Task: FileAvailabilitySensor

Create a **TaskFlow sensor** that:

1. Reads the CSV produced by the Extract task  
2. Checks if the file contains at least **one record**  
3. Returns a `PokeReturnValue` with:
   - `is_done=True` if records exist  
   - `xcom_value=<file_path>`

Sensor configuration:

- `poke_interval=30`  
- `timeout=3600`  
- `mode="poke"`

---

## 5. Branching Task: BranchingTask

Create a `BranchPythonOperator` that:

1. Receives the file path returned by the sensor  
2. Reads the CSV  
3. Returns one of the downstream tasks id:
   - `"TransformData"` if the file has rows  
   - `"ErrorReport"` if the file is empty

---

## 6. Task: TransformData

Create a TaskFlow task that:

1. Reads the locally extracted CSV  
2. Drops rows containing null values  
3. Converts the `Date` column to datetime  
4. Computes:

```
promo_intensity = MarkDown1 + MarkDown2 + MarkDown3 + MarkDown4 + MarkDown5
```

5. Converts column names to lowercase with underscores  
6. Groups by `store` and `date` using the following aggregations:

- temperature → mean  
- fuel_price → mean  
- promo_intensity → sum  
- isholiday → max  
- cpi → mean  
- unemployment → mean  

7. Writes the cleaned file to:

```
/opt/airflow/data/extracted/walmart_sales_transformed.csv
```
Code:
```
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
```

8. Returns the transformed file path

---

## 7. Task: ErrorReport

Create a TaskFlow task that returns:

```
{
  "message": "Errors detected in the ETL process.",
  "status_code": 0
}
```

This path is executed when BranchingTask detects an issue.

---

## 8. SQL Task: CreateTable

Use `SQLExecuteQueryOperator` to ensure the target table exists in Postgres.

Columns must be:

```
store INT
date DATE
temperature FLOAT
fuel_price FLOAT
promo_intensity INT
isholiday INT
cpi FLOAT
unemployment FLOAT
```

---

## 9. Task: LoadData

Create a TaskFlow task that:

1. Reads the transformed CSV  
2. Uses `PostgresHook` to obtain a SQLAlchemy engine  
3. Writes rows to the target table using `df.to_sql()` with:
   - `if_exists="append"`  
   - `index=False`

4. Returns:

```
{
  "message": "Data loaded successfully into Postgres.",
  "status_code": 1
}
```

---

## 10. Task: Notification

Create a TaskFlow task that:

1. Pulls XComs from:
   - `LoadData`
   - `ErrorReport`
2. Prints either the success or error message  
3. Returns whichever report is available

Use trigger rule:

```
none_failed_min_one_success
```

---

## 11. Define Task Dependencies

Your DAG must follow this structure:

```
![dag image](./A4_etl_pipeline_dag-graph.png)
```

