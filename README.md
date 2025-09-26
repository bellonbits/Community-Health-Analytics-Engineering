# Community Health Analytics Engineering Project

## Project Overview

This project is a complete data analytics engineering pipeline designed to collect, process, and analyze community health data. The goal is to provide a unified, structured, and accessible data source for health administrators to monitor key metrics, evaluate program performance, and make data-driven decisions.

The pipeline automates the entire data lifecycle, from ingesting raw data from a mobile application API and CSV files to loading it into a structured data warehouse for business intelligence and visualization.

## Architecture

The project's architecture is built on a modern data stack, orchestrated by Apache Airflow.

### Components

1. **Data Sources**
   - **Mobile API Logs:** Operational data from a mobile application used by Community Health Workers (CHWs)
   - **Static CSV Files:** Structured data on CHWs, households, and visits

2. **Orchestration (Apache Airflow)**
   - Manages and schedules data pipelines
   - Ensures daily data fetching and processing
   - Provides workflow monitoring and alerting

3. **Storage Layer**
   - **MinIO:** Temporary object storage for raw CSV files
   - **PostgreSQL:** Staging database for mobile API logs before warehouse loading

4. **Data Warehousing (Snowflake)**
   - Central data warehouse with star schema design
   - **Fact Table:** `CHW_VISITS_FACT`
   - **Dimension Tables:** `CHW_DIM`, `HOUSEHOLD_DIM`

5. **Visualization & Monitoring**
   - **Power BI:** Business intelligence dashboards and reporting
   - **Grafana:** Real-time monitoring of operational logs and application performance

## File Structure

```
community-health-analytics/
├── .gitignore
├── dags/
│   ├── chw_data_minio.py          # DAG for CSV ingestion to MinIO
│   └── mobile_pipeline.py         # DAG for mobile API log ingestion
├── scripts/
│   ├── fetch_mobile_logs.py       # Fetches data from mobile API
│   ├── load_to_snowflake.py       # ELT process to Snowflake
│   └── upload_csv_to_minio.py     # Uploads CSV files to MinIO
└── sql/
    └── snowflake_schema.sql       # Star schema definitions
```

## Prerequisites

### Infrastructure
- Virtual Machine (VM) for running Airflow and MinIO
- PostgreSQL instance access
- Snowflake data warehouse with configured user and role

### Python Libraries
```bash
apache-airflow
pandas
requests
sqlalchemy
psycopg2
boto3
snowflake-connector-python
```

## Getting Started

### 1. Environment Setup

Clone the repository to your Airflow VM:
```bash
git clone <repository-url>
cd community-health-analytics
```

Install required Python libraries:
```bash
pip install apache-airflow pandas requests sqlalchemy psycopg2 boto3 snowflake-connector-python
```

### 2. Configure Airflow Connections

Configure the following connections in the Airflow UI under **Admin > Connections**:

#### Snowflake Connection
- **Connection ID:** `snowflake_default`
- **Connection Type:** Snowflake
- **Account:** Your Snowflake account identifier
- **User:** Snowflake username
- **Password:** Snowflake password
- **Warehouse:** Target warehouse name
- **Database:** Target database name
- **Schema:** Target schema name
- **Role:** Snowflake role with appropriate permissions

#### PostgreSQL Connection
- **Connection ID:** `postgres_default`
- **Connection Type:** Postgres
- **Host:** PostgreSQL host address
- **Database:** Database name
- **User:** PostgreSQL username
- **Password:** PostgreSQL password
- **Port:** 5432 (default)

#### MinIO Connection
- **Connection ID:** `minio_default`
- **Connection Type:** AWS S3
- **Extra:** JSON configuration with MinIO endpoint and credentials

### 3. Prepare Data Files

Transfer your source CSV files to the Airflow VM:
```bash
scp CHW_Master.csv user@airflow-vm:/path/to/data/
scp Households.csv user@airflow-vm:/path/to/data/
scp CHW_Visits.csv user@airflow-vm:/path/to/data/
```

Update the file paths in `upload_csv_to_minio.py` to match your directory structure.

### 4. Initialize Snowflake Schema

Run the schema creation script in your Snowflake environment:
```sql
-- Execute sql/snowflake_schema.sql in Snowflake
```

### 5. Run the Data Pipelines

#### Option A: Scheduled Execution
The DAGs are configured to run daily automatically. Monitor progress in the Airflow UI.

#### Option B: Manual Trigger
1. Navigate to the Airflow UI
2. Locate the following DAGs:
   - `mobile_pipeline` - Fetches mobile API logs
   - `chw_data_minio` - Uploads CSV files to MinIO
3. Click the "Trigger DAG" button for each

#### Option C: Manual Script Execution
```bash
# Fetch mobile logs
python scripts/fetch_mobile_logs.py

# Upload CSV files to MinIO
python scripts/upload_csv_to_minio.py

# Load data to Snowflake
python scripts/load_to_snowflake.py
```

### 6. Connect Visualization Tools

#### Power BI
1. Open Power BI Desktop
2. Select **Get Data > Database > Snowflake**
3. Enter your Snowflake credentials
4. Connect to the analytics database and schema
5. Build dashboards using the fact and dimension tables

#### Grafana
1. Add Snowflake or PostgreSQL data source
2. Create dashboards for operational monitoring
3. Set up alerts for critical metrics

## Data Pipeline Flow

```
Mobile API → fetch_mobile_logs.py → PostgreSQL → load_to_snowflake.py → Snowflake
CSV Files → upload_csv_to_minio.py → MinIO → load_to_snowflake.py → Snowflake
                                                                           ↓
                                                                  Power BI / Grafana
```

## Monitoring and Maintenance

### Airflow Monitoring
- Monitor DAG runs in the Airflow UI
- Check task logs for errors
- Set up email alerts for failed tasks

### Data Quality Checks
- Validate row counts after each load
- Check for null values in critical fields
- Monitor data freshness timestamps

### Troubleshooting
- Check Airflow logs: `/path/to/airflow/logs/`
- Verify connection credentials in Airflow UI
- Ensure network connectivity to all data sources
- Validate file permissions on the VM

## Best Practices

1. **Security**
   - Store credentials in Airflow connections, not in code
   - Use role-based access control in Snowflake
   - Encrypt data in transit and at rest

2. **Performance**
   - Schedule DAGs during off-peak hours
   - Implement incremental loading where possible
   - Monitor warehouse credit usage in Snowflake

3. **Data Governance**
   - Document data lineage
   - Maintain data dictionary
   - Implement data retention policies

## Future Enhancements

- [ ] Implement data quality validation framework
- [ ] Add automated testing for pipeline components
- [ ] Create CI/CD pipeline for deployment
- [ ] Implement incremental loading strategies
- [ ] Add dbt for advanced transformations
- [ ] Set up data cataloging and metadata management

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Peter Gatitu Mwangi**  
Data & Analytics Engineer

- Email: [Petergatitu61@gmail.com]


## Acknowledgments

- Apache Airflow community for orchestration capabilities
- Snowflake for providing a robust data warehouse platform
- The Community Health Workers who generate the data that makes this project possible

---

*Last Updated: September 2025*
