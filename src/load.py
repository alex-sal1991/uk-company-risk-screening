import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

load_dotenv()

AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER")
AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")
AZURE_SQL_USER = os.getenv("AZURE_SQL_USER")
AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")

if not all([AZURE_SQL_SERVER, AZURE_SQL_DATABASE, AZURE_SQL_USER, AZURE_SQL_PASSWORD]):
    raise ValueError

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
engine = create_engine(url, connect_args={"timeout": 60})

with engine.connect() as conn:
    print(conn.execute(text("SELECT @@VERSION")).scalar())

