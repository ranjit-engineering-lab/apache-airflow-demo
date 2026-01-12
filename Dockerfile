FROM apache/airflow:3.1.2
COPY requirements.txt /
ENV AIRFLOW_VERSION=3.1.2
ENV AIRFLOW___CORE__LOAD_EXAMPLES=False
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
