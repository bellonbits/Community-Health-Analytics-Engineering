Community Health Analytics Engineering Project
Project Overview
This project is a complete data analytics engineering pipeline designed to collect, process, and analyze community health data. The goal is to provide a unified, structured, and accessible data source for health administrators to monitor key metrics, evaluate program performance, and make data-driven decisions.

The pipeline automates the entire data lifecycle, from ingesting raw data from a mobile application API and CSV files to loading it into a structured data warehouse for business intelligence and visualization.

Architecture
The project's architecture is built on a modern data stack, orchestrated by Apache Airflow.

Data Sources: Data is collected from two primary sources:

Mobile API Logs: Operational data from a mobile application used by Community Health Workers (CHWs).

Static CSV Files: Structured data on CHWs, households, and visits.

Orchestration (Airflow): Apache Airflow manages and schedules the data pipelines, ensuring that data is fetched and processed on a daily basis.

Storage:

MinIO: Serves as a temporary object storage for raw CSV files.

PostgreSQL: A staging database for mobile API logs before they are loaded into the data warehouse.

Data Warehousing (Snowflake): The central data warehouse where data is structured into a star schema for optimal analytics performance.

Fact Table: CHW_VISITS_FACT

Dimension Tables: CHW_DIM, HOUSEHOLD_DIM

Visualization & Monitoring:

Power BI: Used for high-level business intelligence dashboards and reporting.

Grafana: Used for real-time monitoring of operational logs and application performance.

File Structure
community-health-analytics/
├── .gitignore
├── dags/
│   ├── chw_data_minio.py
│   └── mobile_pipeline.py
├── scripts/
│   ├── fetch_mobile_logs.py
│   ├── load_to_snowflake.py
│   └── upload_csv_to_minio.py
└── sql/
    └── snowflake_schema.sql

Prerequisites
A virtual machine (VM) to run Airflow and MinIO.

Access to a PostgreSQL instance.

Access to a Snowflake data warehouse with a user and role configured.

The following Python libraries installed: apache-airflow, pandas, requests, sqlalchemy, psycopg2, boto3, snowflake-connector-python.

Getting Started
1. Set up your Environment
Clone this repository to your Airflow VM.

Install the required Python libraries.

2. Configure Airflow Connections and Variables
Snowflake: Configure a Snowflake connection in Airflow with the necessary credentials (account, user, password, warehouse, database, schema, role).

PostgreSQL: Configure a PostgreSQL connection.

MinIO: Configure a MinIO connection.

3. Place CSV Files
Manually transfer your source CSV files (CHW_Master.csv, Households.csv, CHW_Visits.csv) to the designated local directory on your Airflow VM as specified in upload_csv_to_minio.py.

4. Run the DAGs
The Airflow DAGs are scheduled to run daily. You can also manually trigger them from the Airflow UI to start the data ingestion process.

The mobile_pipeline.py DAG will run the fetch_mobile_logs.py script to get data from the API and store it in PostgreSQL.

The chw_data_minio.py DAG will run the upload_csv_to_minio.py script to load the static CSV files into MinIO.

The load_to_snowflake.py script (which you can run manually or integrate into its own DAG) will then pull the data from MinIO and Snowflake, performing the final ELT (Extract, Load, Transform) steps.

5. Manual Steps
Move Files: Use scp to securely copy your local CSV files to the Airflow VM.

Visualize: Connect your Power BI instance to your Snowflake data warehouse to build your dashboards and reports.

Author
Peter Gatitu Mwangi - Data & Analytics Engineer
