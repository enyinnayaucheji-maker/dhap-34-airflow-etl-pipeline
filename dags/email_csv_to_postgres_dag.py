from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import csv
import os
import yaml
import psycopg2


CSV_PATH = "/opt/airflow/sample_data/dataset.csv"
SCHEMA_PATH = "/opt/airflow/config/schema_expected.yaml"
SQL_PATH = "/opt/airflow/sql/create_table.sql"


def validate_files():
    for path in [CSV_PATH, SCHEMA_PATH, SQL_PATH]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing file: {path}")
    print("All required files found.")


def validate_csv_schema():
    with open(SCHEMA_PATH, "r") as f:
        schema = yaml.safe_load(f)

    expected_columns = [col["name"] for col in schema["columns"]]

    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        actual_columns = reader.fieldnames

    if actual_columns != expected_columns:
        raise ValueError(f"Schema mismatch. Expected {expected_columns}, got {actual_columns}")

    print("CSV schema validation passed.")


def create_table():
    with open(SQL_PATH, "r") as f:
        sql = f.read()

    conn = psycopg2.connect(
        host="postgres",
        port=5432,
        database="airflow",
        user="airflow",
        password="airflow"
    )

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

    print("Table created successfully.")


def load_csv_to_postgres():
    conn = psycopg2.connect(
        host="postgres",
        port=5432,
        database="airflow",
        user="airflow",
        password="airflow"
    )

    cur = conn.cursor()

    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    cur.execute("TRUNCATE TABLE public.email_support_dataset;")

    for row in rows:
        cur.execute(
            """
            INSERT INTO public.email_support_dataset (
                subject, sender, receiver, timestamp, message_body,
                thread_id, email_types, email_status, email_criticality,
                product_types, agent_effectivity, agent_efficiency,
                customer_satisfaction
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row["subject"],
                row["sender"],
                row["receiver"],
                row["timestamp"],
                row["message_body"],
                row["thread_id"],
                row["email_types"],
                row["email_status"],
                row["email_criticality"],
                row["product_types"],
                row["agent_effectivity"],
                row["agent_efficiency"],
                row["customer_satisfaction"],
            )
        )

    conn.commit()
    cur.close()
    conn.close()

    print(f"Loaded {len(rows)} rows into PostgreSQL.")


with DAG(
    dag_id="email_csv_to_postgres_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    task_validate_files = PythonOperator(
        task_id="validate_files",
        python_callable=validate_files
    )

    task_validate_schema = PythonOperator(
        task_id="validate_csv_schema",
        python_callable=validate_csv_schema
    )

    task_create_table = PythonOperator(
        task_id="create_table"
    ,   python_callable=create_table
    )

    task_load_csv = PythonOperator(
        task_id="load_csv_to_postgres",
        python_callable=load_csv_to_postgres
    )

    task_validate_files >> task_validate_schema >> task_create_table >> task_load_csv