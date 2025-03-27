from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("ydpg-cvhr222qgecs73d3qg50-a"),
        database=os.getenv("autoanalysis_db"),
        user=os.getenv("autoanalysis_db_user"),
        password=os.getenv("qaHNfDYLep42gBhQq94KNUVYQFrGolKr")
    )

@app.get("/sales-data")
def get_sales():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales")
    data = cursor.fetchall()
    conn.close()
    return {"data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
