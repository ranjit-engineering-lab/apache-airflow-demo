
# Instructions for Creating an 8–10 Minute Video Demo

## 1. Introduction (30–60 seconds)

Briefly introduce:

- Your names
- The purpose of the ETL pipeline  
- Tools used: *Apache Airflow, S3, Postgres, Python/pandas*  
- What the viewer will see in the demo

---

## 2. Show Project Structure (45–60 seconds)

Display your Airflow project folder and walk through:

- The `dags/` directory  
- The location of your DAG file.
- The local data directory (`/opt/airflow/data/extracted`)  

Explain briefly how Airflow picks up DAG files automatically.

---

## 3. Show Your Airflow Connections (1 minute)

Navigate in the Airflow UI to:

- **Admin → Connections**

Show and briefly describe the following configured connections:

1. **AWS connection**  
   - Conn ID: `ensf-aws`  
   - Purpose: Access S3 bucket  

2. **Postgres connection**  
   - Conn ID: `user_postgres`  
   - Purpose: Load transformed data  

Do NOT reveal secret keys — just show that the connections exist.

---

## 4. Walk Through Your DAG Code (2–3 minutes)

Open your `etl_pipeline_dag.py` file and explain:

- The DAG definition (schedule, start date, tags)  
- Key constants (bucket name, paths, connection IDs)  
- Each major task:

### Tasks to Explain
- `ExtractFromS3`  
- `FileAvailabilitySensor`  
- `BranchingTask`  
- `TransformData`  
- `ErrorReport`  
- `CreateTable`  
- `LoadData`  
- `Notification`

For each task, briefly state:
- What it does  
- Why it’s needed  
- How it connects to the next task  

Do not read code line‑by‑line — describe functionality and purpose.

---

## 5. Run the DAG (2–3 minutes)

Demonstrate the DAG running in Airflow:

1. In the UI, **enable** and **trigger** the DAG  
2. Show tasks appearing in the graph view  
3. Click on tasks to show logs  
4. Highlight:
   - Successful extraction  
   - The sensor checking file availability  
   - Branching behavior  
   - The transformation step  
   - Table creation and Postgres loading  
   - Final notification  

Explain what is happening as tasks turn green.

---

## 6. Validate Data Load in Postgres (45–60 seconds)

Use a SQL client or Adminer/pgAdmin to run:

```sql
SELECT COUNT(*) FROM public.walmart_sales_transformed;
SELECT * FROM public.walmart_sales_transformed LIMIT 10;
```

Show:

- The table exists  
- New rows appear after the DAG run  

Explain how this proves the ETL pipeline executed end‑to‑end.

---

## 7. Closing Summary (30–45 seconds)

Conclude with:

- What the pipeline accomplishes  
- What worked well  
- What you might improve (e.g., error handling, incremental loads, partitioning)

Example:
> “This pipeline successfully automates extraction, validation, transformation, and loading of S3 data into Postgres. In future improvements, I would add notifications and partitioned storage for scalability.”

---

## Recommended Time Distribution

| Section | Time |
|--------|------|
| Introduction | 0:30–1:00 |
| Project Structure | 0:45–1:00 |
| Connections | 1:00 |
| DAG Walkthrough | 2:00–3:00 |
| Running the DAG | 2:00–3:00 |
| Postgres Validation | 0:45–1:00 |
| Closing | 0:30–0:45 |
| **Total** | **8–10 minutes** |

---

