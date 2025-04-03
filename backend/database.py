# import psycopg2
# import os
# from dotenv import load_dotenv

# load_dotenv()  # Load environment variables

# def get_db_connection():
#     return psycopg2.connect(
#         host=os.getenv("ydpg-cvhr222qgecs73d3qg50-a"),
#         database=os.getenv("autoanalysis_db"),
#         user=os.getenv("autoanalysis_db_user"),
#         password=os.getenv("qaHNfDYLep42gBhQq94KNUVYQFrGolKr")
#     )





import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read database connection settings from environment variables
DB_HOST = os.getenv("ydpg-cvhr222qgecs73d3qg50-a")
DB_NAME = os.getenv("autoanalysis_db")
DB_USER = os.getenv("autoanalysis_db_user")
DB_PASS = os.getenv("qaHNfDYLep42gBhQq94KNUVYQFrGolKr")

# If all PostgreSQL variables are set, use PostgreSQL, else fallback to SQLite
if DB_HOST and DB_NAME and DB_USER and DB_PASS:
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"  # Local fallback

# Create engine; echo=True helps during debugging (set to False in production)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

