
# End-to-End ETL with Apache Airflow

> IMPORTANT INFORMATION:
- [Docker Set up Instructions](./assets/setup.md)
- [Instructions to Build Dag and Tasks](./assets/Build_Instructions_DAG_Tasks.md)


**Goal:** Build and operate a daily ETL pipeline that extracts a CSV from S3, validates availability, transforms it with pandas, conditionally branches on success/failure, creates a target table in Postgres, loads transformed rows, and posts a final notification.


**Components Used:**  
TaskFlow API, Sensors, Branching, XCom, SQL operators, Hooks (S3, Postgres), dependency management, idempotent loads.

---

## 1) Prerequisites (install & providers)

Follow the instructions to setup Airflow in Docker: [Docker set up instructions](./assets/setup.md)

The Docker compose file contains all services and volumes needed to setup the servers required for Airflow, metadata DB (postgres), and user data DB (postgres).

Requirements:

- Airflow 3.1+
- A Postgres instance you can write to
- An S3 bucket with a file named **`walmart_sales.csv`** is already set up. Find the access and secret keys on D2L.

Expected CSV columns:

`Store,Date,Temperature,Fuel_Price,MarkDown1,MarkDown2,MarkDown3,MarkDown4,MarkDown5,IsHoliday,CPI,Unemployment`

---

## 2) Airflow Connections to Configure

### **AWS Connection**

- **Conn Id:** `ensf-aws`
- **Conn Type:** Amazon Web Services
- **Login:** AWS Access Key ID (see D2L)
- **Password:** AWS Secret Access Key (see D2L)


### **Postgres Connection information**

- **Conn Id:** `user_postgres`
- **Conn Type:** Postgres
- **Host:** `userdb`
- **Login:** `userdb`
- **Password:** `userdb`
- **Port:** 5432 (default)
- **Database** `user_data`

---

## 3) Local Data Folder Setup

The DAG writes data to:

```
/opt/airflow/data/extracted
```

Ensure this folder exists and is writable.


### Docker Compose example:
This volumne has been added to the docker compose file, to map your folder to a directory in the docker container. You do not need to do anything else.
```yaml
volumes:
  - ./data:/opt/airflow/data
```

---

## 4) S3 File Setup

The AWS S3 bucket has been setup and contains a file (`walmart_sales.csv`). The path to the file is:

```
s3://ensf612bucket/walmart_sales.csv
```

---

## 5) DAG Setup Instructions

1. Create a file in your Airflow `dags/` directory named:

```
etl_pipeline_dag.py
```

2. Write your implementation of the ETL DAG inside it. [Click here for detailed instructions on building out your DAG and Tasks.](./assets/Build_Instructions_DAG_Tasks.md)

3. Ensure you reference the proper AWS and Postgres connection IDs matching your Airflow configuration.

---

## 6) Running the Pipeline

1. Start Airflow (webserver + scheduler). [Refer to the Docker setup instructions for commands.](./assets/setup.md)
2. Open the Airflow UI.
3. Locate the DAG **`A4_etl_pipeline_dag`**.
4. **Unpause** the DAG.
5. Trigger a DAG run.
6. Monitor execution:

   - Extraction from S3  
   - File availability check  
   - Branching decision  
   - Transformation of data  
   - Table creation in Postgres  
   - Loading transformed rows  
   - Final notification  

### Validate in Postgres:

```sql
SELECT COUNT(*) FROM public.walmart_sales_transformed;
SELECT * FROM public.walmart_sales_transformed LIMIT 10;
```

---





