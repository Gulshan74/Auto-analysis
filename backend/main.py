from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .auth import create_user, authenticate_user
from .models import User,Dataset
from datetime import datetime
import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS (adjust allowed origins in production)
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication endpoints
@app.post("/signup/")
def signup(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="User already exists")
    user = create_user(db, username, password)
    return {"message": "User created successfully", "username": user.username}

@app.post("/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful", "username": user.username}

# Endpoint to fetch data from CSV (data folder at repo root)
@app.get("/get-sales-csv/")
def get_sales_csv():
    try:
        # With Docker build context set to repo root, the CSV is in data/sales.csv.
        df = pd.read_csv("data/sales.csv")
        data = df.to_dict(orient="records")
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Advanced: A predictive analytics endpoint (example using Linear Regression)
from sklearn.linear_model import LinearRegression
import numpy as np

@app.get("/predict/")
def predict_revenue():
    try:
        df = pd.read_csv("data/sales.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        df["Date_ordinal"] = df["Date"].apply(lambda x: x.toordinal())
        X = df[["Date_ordinal"]]
        y = df["Revenue"]
        model = LinearRegression()
        model.fit(X, y)
        tomorrow = datetime.now().date().toordinal() + 1
        prediction = model.predict(np.array([[tomorrow]]))
        return {"predicted_revenue": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
