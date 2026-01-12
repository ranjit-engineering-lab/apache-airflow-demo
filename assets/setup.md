# Running Airflow in Docker

> The default amount of memory available for Docker on macOS is often not enough to get Airflow up and running. If enough memory is not allocated, it might lead to the webserver continuously restarting. You should allocate at least 4GB memory for the Docker Engine (ideally 8GB).
You can check if you have enough memory by running this command:
```
docker run --rm "debian:bookworm-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'
```

## Fetching docker-compose.yaml
To deploy Airflow on Docker Compose, you should fetch docker-compose.yaml.
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.1.2/docker-compose.yaml'
```

## Initializing Environment
Before starting Airflow for the first time, you need to prepare your environment, i.e. create the necessary files, directories and initialize the database.

### Setting the right Airflow user
On Linux, the quick-start needs to know your host user id and needs to have group id set to 0. Otherwise the files created in dags, logs, config and plugins will be created with root user ownership. You have to make sure to configure them for the docker-compose:
```
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

### Initialize airflow.cfg (Optional)
If you want to initialize airflow.cfg with default values before launching the airflow service, run:
```
docker compose run airflow-cli airflow config list
```
This will seed airflow.cfg with default values in config folder.

### Initialize the database
On all operating systems, you need to run database migrations and create the first user account. To do this, run.
```
docker compose up airflow-init
```
After initialization is complete, you should see output related to files, folders, and plug-ins and finally a message like this:

```
airflow-init-1 exited with code 0
```
The account created has the login airflow and the password airflow.

## Running Airflow
Now you can start all services:
```
docker compose up
```

## Cleaning up
To stop and delete containers, delete volumes with database data and download images, run:
```
docker compose down --volumes --rmi all
```



# Analytics Database (Postgresql) Setup
## Create a connection inside Airflow to this new DB
Go to:

Airflow UI → Admin → Connections → + Add

Fill it like:


| Field     | Value           |
| --------- | --------------- |
| Conn Id   | `user_postgres` |
| Conn Type | Postgres        |
| Host      | `userdb`        |
| Schema    | `user_data`     |
| Login     | `userdb`        |
| Password  | `userdb`        |
| Port      | `5432`          |
