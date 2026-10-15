FROM apache/airflow:3.3.2-python3.13

RUN uv pip install --no-cache \
    "apache-airflow==${AIRFLOW_VERSION}" \
    "requests==2.34.2" \
    "psycopg[binary]==3.3.6" \
    "python-dotenv==1.2.4"

RUN uv venv /home/airflow/dbt_venv \
    && uv pip install --no-cache --python /home/airflow/dbt_venv/bin/python \
        "dbt-core==1.12.5" \
        "dbt-postgres==1.11.0"