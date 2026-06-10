# DHAP-34 — Dockerized Airflow ETL Pipeline

## Project Overview

This project implements a containerized ETL pipeline using Apache Airflow, PostgreSQL, Docker, and Python.

The pipeline ingests a local CSV dataset, validates the schema against a YAML contract, creates a PostgreSQL table using SQL DDL, and loads the validated records into PostgreSQL.

---

## Architecture Flow

```text
CSV Dataset
    ↓
Schema Validation (YAML)
    ↓
SQL Table Creation
    ↓
PostgreSQL Load
    ↓
Verification Queries
```

---

## Technologies Used

- Apache Airflow
- PostgreSQL
- Docker
- Docker Compose
- Python
- YAML
- SQL
- psycopg2

---

## Project Structure

```text
DHAP-34/
│
├── dags/
│   └── email_csv_to_postgres_dag.py
│
├── config/
│   └── schema_expected.yaml
│
├── sample_data/
│   └── dataset.csv
│
├── sql/
│   └── create_table.sql
│
├── .env
├── .env.example
├── docker-compose.yml
└── README.md
```

---

## Airflow DAG Workflow

The Airflow DAG performs the following steps:

1. Validate required files exist
2. Validate CSV schema against YAML schema contract
3. Create PostgreSQL table using SQL DDL
4. Load CSV records into PostgreSQL
5. Verify successful ingestion

---
## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository_url>
cd DHAP-34
```

---

### 2. Configure Environment Variables

Create a `.env` file:

```env
PG_HOST=postgres
PG_PORT=5432
PG_DB=airflow
PG_USER=airflow
PG_PASSWORD=airflow
```

---

### 3. Start Docker Services

```bash
docker compose up -d
```

---

### 4. Access Airflow

Open:

```text
http://localhost:8080
```

Login credentials:

```text
Username: airflow
Password: airflow
```

---

### 5. Trigger the DAG

Run the DAG:

```text
email_csv_to_postgres_pipeline
```

---

## PostgreSQL Verification

Enter PostgreSQL container:

```bash
docker exec -it dhap_postgres psql -U airflow -d airflow
```

Verify row count:

```sql
SELECT COUNT(*) FROM public.email_support_dataset;
```

Expected result:

```text
2259 rows
```

Preview records:

```sql
SELECT subject, sender, customer_satisfaction
FROM public.email_support_dataset
LIMIT 5;
```

---

## Troubleshooting

### Airflow UI Not Opening

Restart services:

```bash
docker compose down
docker compose up -d
```

---

### DAG Not Appearing

Restart Airflow services:

```bash
docker compose restart airflow-scheduler airflow-webserver
```

---

### Check Running Containers

```bash
docker compose ps
```

---

## Project Status

 Dockerized Airflow environment completed  
 PostgreSQL integration completed  
 CSV schema validation implemented  
 SQL table creation automated  
 CSV successfully loaded into PostgreSQL  
 Data verification completed
