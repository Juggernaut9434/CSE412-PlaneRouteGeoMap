import psycopg2
from config import config

params = config()
print(params)
conn = psycopg2.connect(**params)

cur = conn.cursor()
cur.execute("SELECT * FROM airline LIMIT 10")
records = cur.fetchall()
print(records)
