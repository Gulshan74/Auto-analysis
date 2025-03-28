from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from .database import get_db_connection
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Enable CORS so your frontend can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# A simple root endpoint (optional)
@app.get("/")
def read_root():
    return {"message": "Backend is running"}

# Existing endpoint: returns data from database (if needed)
@app.get("/get-sales-db")
def get_sales_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales")
        data = cursor.fetchall()
        conn.close()
        return {"data": data}
    except Exception as e:
        # Log error details (you can also use logging module)
        return {"error": str(e)}

# New endpoint: read and return data from CSV file
@app.get("/get-sales-csv")
def get_sales_csv():
    try:
        # Use "data/sales.csv" (because the "data" folder is at /app/data)
        df = pd.read_csv("data/sales.csv")
        data = df.to_dict(orient="records")
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
