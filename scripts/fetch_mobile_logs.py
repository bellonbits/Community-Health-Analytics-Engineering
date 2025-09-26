import requests
import pandas as pd
from sqlalchemy import create_engine

api = "https://api-logs-yf3a.vercel.app/data"

response= requests.get(api)
data = response.json()

df = pd.DataFrame(data["data"])

engine = create_engine("postgresql://peter:1234@4.222.216.225:5432/community_db")

df.to_sql("mobile_data", engine, schema="api_log", if_exists="append", index=False)
