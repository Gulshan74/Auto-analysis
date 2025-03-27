import pandas as pd
import psycopg2

# Connect to Database
conn = psycopg2.connect(
    host="ydpg-cvhr222qgecs73d3qg50-a",
    database="autoanalysis_db",
    user="autoanalysis_db_user",
    password="qaHNfDYLep42gBhQq94KNUVYQFrGolKr"
)
cursor = conn.cursor()

# Load Excel Data
df = pd.read_excel("sales.csv")

# Insert Data into SQL
for _, row in df.iterrows():
    cursor.execute("INSERT INTO sales (date, product, revenue, cost, profit) VALUES (%s, %s, %s, %s, %s)",
                   (row["Date"], row["Product"], row["Revenue"], row["Cost"], row["Profit"]))

conn.commit()
cursor.close()
conn.close()

print("✅ Data Uploaded to SQL")
