import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("ydpg-cvhr222qgecs73d3qg50-a"),
        database=os.getenv("autoanalysis_db"),
        user=os.getenv("autoanalysis_db_user"),
        password=os.getenv("qaHNfDYLep42gBhQq94KNUVYQFrGolKr")
    )
