import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

load_dotenv()

AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER")
AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")
AZURE_SQL_USER = os.getenv("AZURE_SQL_USER")
AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")

if not all([AZURE_SQL_SERVER, AZURE_SQL_DATABASE, AZURE_SQL_USER, AZURE_SQL_PASSWORD]):
    raise ValueError("Missing Azure SQL settings in .env")

ddl = Path("sql/01_create_silver.sql").read_text()

url = URL.create(
    "mssql+pyodbc",
    username=AZURE_SQL_USER,
    password=AZURE_SQL_PASSWORD,
    host=AZURE_SQL_SERVER,
    port=1433,
    database=AZURE_SQL_DATABASE,
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "Encrypt": "yes",
        "TrustServerCertificate": "no",
    }
)
engine = create_engine(url, connect_args={"timeout": 60}, fast_executemany=True)

with engine.begin() as conn:
    conn.execute(text(ddl))

loads = [
    ("companies", "data/silver/companies.csv", ["incorporation_date", "date_of_cessation"]),
    ("officers", "data/silver/officers.csv", ["appointed_on", "resigned_on"]),
    ("psc", "data/silver/psc.csv", ["notified_on", "ceased_on"])
]

for table, path, date_cols in loads:
    df = pd.read_csv(path, dtype={"company_number":str, "sic_codes":str}, parse_dates=date_cols)
    df.to_sql(table, engine, schema="silver", if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into silver.{table}")

with engine.connect() as conn:
    for table, _, _ in loads:
        count = conn.execute(text(f"SELECT COUNT(*) FROM silver.{table}")).scalar()
        print(f"silver.{table}: {count} rows")