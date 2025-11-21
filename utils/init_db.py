import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def init_db():
    engine = create_engine(DATABASE_URL)
    
    # Read schema.sql
    with open("database/schema.sql", "r") as f:
        schema_sql = f.read()
        
    try:
        with engine.connect() as conn:
            # Create tables
            # Split by ';' to execute statements individually if needed, or just execute block
            # SQLAlchemy execute might not handle multiple statements in one go depending on driver
            # But let's try executing the whole script or split it.
            # Splitting is safer.
            statements = schema_sql.split(';')
            for statement in statements:
                if statement.strip():
                    conn.execute(text(statement))
            
            # Seed data
            print("Seeding data...")
            
            # Check if users exist
            result = conn.execute(text("SELECT count(*) FROM users")).scalar()
            if result == 0:
                conn.execute(text("""
                    INSERT INTO users (email, full_name) VALUES 
                    ('alice@example.com', 'Alice Smith'),
                    ('bob@example.com', 'Bob Jones')
                """))
                
                # Get user IDs
                alice_id = conn.execute(text("SELECT id FROM users WHERE email='alice@example.com'")).scalar()
                
                conn.execute(text("""
                    INSERT INTO orders (order_number, user_id, product_name, status, delivery_date) VALUES 
                    ('ORD-123', :uid, 'Wireless Headphones', 'shipped', '2023-10-25'),
                    ('ORD-456', :uid, 'Gaming Mouse', 'processing', NULL)
                """), {"uid": alice_id})
                
                conn.execute(text("""
                    INSERT INTO tickets (ticket_number, user_id, subject, description, status) VALUES 
                    ('TKT-001', :uid, 'Login Issue', 'Cannot reset password', 'open')
                """), {"uid": alice_id})
                
            conn.commit()
            print("Database initialized and seeded successfully.")
            
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_db()
