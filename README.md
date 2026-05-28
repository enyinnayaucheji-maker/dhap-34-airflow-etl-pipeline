# DHAP-34 Data Pipeline

This project builds a Dockerized Apache Airflow pipeline that loads a local CSV dataset into PostgreSQL.

## Pipeline Flow

CSV file → Schema validation → Create PostgreSQL table → Load data into PostgreSQL

## Tools Used

- Docker
- Docker Compose
- Apache Airflow
- PostgreSQL
- Python
- YAML
- SQL

## Project Structure

```text
DHAP-34/
├── dags/
├── config/
├── sample_data/
├── sql/
├── docker-compose.yml
└── README.md