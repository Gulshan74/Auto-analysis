import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables
conn = psycopg2.connect(

        host=os.getenv("ydpg-cvhr222qgecs73d3qg50-a"),
        database=os.getenv("autoanalysis_db"),
        user=os.getenv("autoanalysis_db_user"),
        password=os.getenv("qaHNfDYLep42gBhQq94KNUVYQFrGolKr")
    )
cursor = conn.cursor()

# Load Excel Data from the correct relative path
df = pd.read_excel("../data/sales.csv")

# Insert Data into SQL
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO sales (date, product, revenue, cost, profit) VALUES (%s, %s, %s, %s, %s)",
        (row["Date"], row["Product"], row["Revenue"], row["Cost"], row["Profit"])
    )
conn.commit()
cursor.close()
conn.close()

print("✅ Data Uploaded to SQL")
