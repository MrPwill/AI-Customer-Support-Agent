import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def init_db():
    if not DATABASE_URL:
        print("Error: DATABASE_URL not found in .env")
        return

    # Ensure the database directory exists if using sqlite
    if DATABASE_URL.startswith("sqlite"):
        db_path = DATABASE_URL.replace("sqlite:///", "")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    engine = create_engine(DATABASE_URL)

    with open("database/schema.sql", "r") as f:
        schema_sql = f.read()

    try:
        with engine.connect() as conn:
            # Enable foreign keys for SQLite
            if "sqlite" in DATABASE_URL:
                conn.execute(text("PRAGMA foreign_keys=ON"))
            
            # Execute schema
            # Split by ; to execute multiple statements if needed, though execute(text()) might handle it depending on driver
            # For safety with some drivers, let's split
            statements = schema_sql.split(';')
            for statement in statements:
                if statement.strip():
                    conn.execute(text(statement))
            
            print("Schema initialized.")

            # Seed data
            # Check if users exist to avoid duplicates if re-running (basic check)
            result = conn.execute(text("SELECT count(*) FROM users")).scalar()
            if result == 0:
                print("Seeding data...")
                
                # Users
                conn.execute(text("""
                    INSERT INTO users (email, full_name) VALUES 
                    ('john@example.com', 'John Doe'),
                    ('jane@example.com', 'Jane Smith')
                """))
                
                # Get user IDs
                john_id = conn.execute(text("SELECT id FROM users WHERE email='john@example.com'")).scalar()
                jane_id = conn.execute(text("SELECT id FROM users WHERE email='jane@example.com'")).scalar()
                
                # Orders
                conn.execute(text("""
                    INSERT INTO orders (order_number, user_id, product_name, status, delivery_date) VALUES 
                    ('ORD-123', :john_id, 'Wireless Headphones', 'shipped', '2023-10-25 10:00:00'),
                    ('ORD-456', :john_id, 'Smartphone Case', 'delivered', '2023-10-20 14:30:00'),
                    ('ORD-789', :jane_id, 'Gaming Laptop', 'processing', NULL)
                """), {"john_id": john_id, "jane_id": jane_id})
                
                # Tickets
                conn.execute(text("""
                    INSERT INTO tickets (ticket_number, user_id, subject, description, status) VALUES 
                    ('TKT-001', :john_id, 'Defective Headphones', 'The right earcup is not working.', 'open'),
                    ('TKT-002', :jane_id, 'Shipping Delay', 'My laptop has not shipped yet.', 'in_progress')
                """), {"john_id": john_id, "jane_id": jane_id})
                
                conn.commit()
                print("Data seeded successfully.")
            else:
                print("Data already exists, skipping seed.")

    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_db()
