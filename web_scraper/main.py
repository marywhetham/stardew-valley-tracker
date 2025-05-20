import psycopg2
import os
from dotenv import load_dotenv
import items

env_path = "../.env.development.local"

load_dotenv(dotenv_path=env_path)
os.getenv("DATABASE_URL")
conn = psycopg2.connect(
    dbname= os.getenv("PGDATABASE"),
    user= os.getenv("PGUSER"),
    password= os.getenv("POSTGRES_PASSWORD"),
    host= os.getenv("POSTGRES_HOST"),
    port= 5432,
    sslmode="require"
)

cur = conn.cursor()

items.insert_items(cur)

conn.commit()
cur.close()
conn.close()