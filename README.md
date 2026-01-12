[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/0H9LWW_0)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=21800210&assignment_repo_type=AssignmentRepo)

# Assignment: End-to-End ETL with Apache Airflow

> IMPORTANT INFORMATION:
- [Docker Set up Instructions](./assets/setup.md)
- [Instructions to Build Dag and Tasks](./assets/Build_Instructions_DAG_Tasks.md)
- [Video Demo Instructions](./assets/SUBMISSION.md)



This assignment aims to provide hands-on experience with **Apache Airflow** for orchestrating data pipelines. Students will learn to design, implement, and monitor workflows that automate ETL (Extract, Transform, Load) tasks.

**Goal:** Build and operate a daily ETL pipeline that extracts a CSV from S3, validates availability, transforms it with pandas, conditionally branches on success/failure, creates a target table in Postgres, loads transformed rows, and posts a final notification.

**What you’ll practice:**  
TaskFlow API, Sensors, Branching, XCom, SQL operators, Hooks (S3, Postgres), dependency management, idempotent loads.

**Learning Outcomes**

By the end of this assignment, students should be able to:

* Understand the architecture and core components of Apache Airflow (DAGs, Operators, Tasks, Scheduler, Web UI).
* Design and implement Directed Acyclic Graphs (DAGs) to automate workflows.
* Integrate Airflow with data sources.
* Use hooks, sensors, custom operators, and XCom for data passing between tasks.
* Schedule, monitor, and debug Airflow jobs.

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

## 6) Running the Assignment

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

