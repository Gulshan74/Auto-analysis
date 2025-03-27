import psycopg2

def create_table():
    conn = psycopg2.connect(
        host="ydpg-cvhr222qgecs73d3qg50-a",
        database="autoanalysis_db",
        user="autoanalysis_db_user",
        password="qaHNfDYLep42gBhQq94KNUVYQFrGolKr"
    )
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        date DATE,
        product VARCHAR(255),
        revenue FLOAT,
        cost FLOAT,
        profit FLOAT
    )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

create_table()
