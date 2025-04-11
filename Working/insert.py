import pandas as pd
import psycopg2
import random

# Load health_monitoring.csv
df = pd.read_csv("Data/health_monitoring.csv")
unique_device_ids = df['Device-ID/User-ID'].unique()

# PostgreSQL Connection
conn = psycopg2.connect(
    dbname="Health",
    user="postgres",
    password="Saahit21@",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Insert caretakers CT001 to CT010 if not already present
for i in range(1, 11):
    caretaker_id = f"CT{str(i).zfill(3)}"
    cur.execute(
        "INSERT INTO caretakers (caretaker_id, password) VALUES (%s, %s) ON CONFLICT (caretaker_id) DO NOTHING",
        (caretaker_id, caretaker_id)
    )

# Insert devices with random caretaker_id
for device_id in unique_device_ids:
    rand_caretaker_id = f"CT{str(random.randint(1, 10)).zfill(3)}"
    cur.execute(
        "INSERT INTO devices (device_id, password, caretaker_id) VALUES (%s, %s, %s) ON CONFLICT (device_id) DO NOTHING",
        (device_id, device_id, rand_caretaker_id)
    )

conn.commit()
cur.close()
conn.close()

print("Device IDs and caretaker entries inserted.")
