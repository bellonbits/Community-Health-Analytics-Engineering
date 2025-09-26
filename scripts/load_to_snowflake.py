import boto3
import pandas as pd
import snowflake.connector
from io import StringIO
from snowflake.connector.pandas_tools import write_pandas

# --- Connect to MinIO ---
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

# --- Connect to Snowflake ---
conn = snowflake.connector.connect(
    account=SNOWFLAKE_ACCOUNT,
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    role=SNOWFLAKE_ROLE,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA
)

# --- Helper: Load CSV from MinIO safely ---
def load_csv_from_minio(key):
    """Load CSV file from MinIO bucket into a Pandas DataFrame."""
    try:
        obj = s3.get_object(Bucket=BUCKET, Key=key)
        data = obj['Body'].read().decode('utf-8')
        return pd.read_csv(StringIO(data))
    except s3.exceptions.NoSuchKey:
        print(f"❌ File {key} not found in {BUCKET}")
        return pd.DataFrame()

# --- Print available files in bucket for debugging ---
print("📂 Available files in MinIO:")
for obj in s3.list_objects_v2(Bucket=BUCKET).get('Contents', []):
    print(" -", obj['Key'])

# 1️⃣ Load CHW_DIM
chw_df = load_csv_from_minio("CHW_Master.csv")
chw_df.columns = ['CHW_ID','NAME','GENDER','PHONE','COUNTY','HIRE_DATE']

# 2️⃣ Load HOUSEHOLD_DIM
house_df = load_csv_from_minio("Households.csv")
house_df.columns = ['HOUSEHOLD_ID','HEAD_NAME','COUNTY','SUBCOUNTY','GPS_LAT','GPS_LONG','NUM_CHILDREN','WATER_SOURCE']

# 3️⃣ Load CHW_VISITS_FACT
visits_df = load_csv_from_minio("CHW_Visits.csv")
visits_df.columns = ['VISIT_ID','VISIT_DATE','CHW_ID','HOUSEHOLD_ID','DIAGNOSIS','TREATMENT_GIVEN','FOLLOW_UP_REQUIRED','OUTCOME']

# --- Upload to Snowflake tables ---
if not chw_df.empty:
    write_pandas(conn, chw_df, 'CHW_DIM')
    print("✅ CHW_DIM loaded")

if not house_df.empty:
    write_pandas(conn, house_df, 'HOUSEHOLD_DIM')
    print("✅ HOUSEHOLD_DIM loaded")

if not visits_df.empty:
    write_pandas(conn, visits_df, 'CHW_VISITS_FACT')
    print("✅ CHW_VISITS_FACT loaded")

print("🎉 All available data loaded into Snowflake Star Schema successfully.")

conn.close()
