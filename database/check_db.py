import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("Users:")
    result = conn.execute(text("SELECT * FROM users"))
    for row in result:
        print(row)
        
    print("\nOrders:")
    result = conn.execute(text("SELECT * FROM orders"))
    for row in result:
        print(row)

    print("\nTickets:")
    result = conn.execute(text("SELECT * FROM tickets"))
    for row in result:
        print(row)
