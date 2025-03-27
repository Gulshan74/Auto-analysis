import psycopg2

def create_table():
    conn = psycopg2.connect(
        host="your-db-host.render.com",
        database="business_db",
        user="your-db-user",
        password="your-db-password"
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
