from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import json

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
# Note: For production, use a connection pool
engine = create_engine(DATABASE_URL)

def get_order_info_db(order_number: str):
    """Fetch order details by order number from the database."""
    try:
        with engine.connect() as conn:
            query = text("SELECT order_number, product_name, status, delivery_date FROM orders WHERE order_number = :order_number")
            result = conn.execute(query, {"order_number": order_number}).mappings().first()
            
            if result:
                # Convert to dict and handle date serialization if needed
                return json.dumps({
                    "order_id": result["order_number"],
                    "product": result["product_name"],
                    "status": result["status"],
                    "delivery_date": str(result["delivery_date"]) if result["delivery_date"] else "TBD"
                })
            return json.dumps({"error": "Order not found"})
    except Exception as e:
        return json.dumps({"error": f"Database error: {str(e)}"})

def check_ticket_status_db(ticket_number: str):
    """Check the status of a support ticket from the database."""
    try:
        with engine.connect() as conn:
            query = text("SELECT ticket_number, subject, status FROM tickets WHERE ticket_number = :ticket_number")
            result = conn.execute(query, {"ticket_number": ticket_number}).mappings().first()
            
            if result:
                return json.dumps({
                    "ticket_id": result["ticket_number"],
                    "subject": result["subject"],
                    "status": result["status"]
                })
            return json.dumps({"error": "Ticket not found"})
    except Exception as e:
        return json.dumps({"error": f"Database error: {str(e)}"})

def create_support_ticket_db(user_id: int, subject: str, description: str):
    """Create a new support ticket in the database."""
    try:
        # Generate a simple ticket number (in real app, use UUID or sequence)
        import random
        ticket_number = f"TKT-{random.randint(1000, 9999)}"
        
        with engine.begin() as conn: # Use begin() for transaction
            query = text("""
                INSERT INTO tickets (ticket_number, user_id, subject, description, status)
                VALUES (:ticket_number, :user_id, :subject, :description, 'open')
            """)
            conn.execute(query, {
                "ticket_number": ticket_number,
                "user_id": user_id,
                "subject": subject,
                "description": description
            })
            
            return json.dumps({
                "ticket_id": ticket_number,
                "status": "open",
                "message": "Ticket created successfully"
            })
    except Exception as e:
        return json.dumps({"error": f"Database error: {str(e)}"})

def update_user_account_db(user_id: int, updates: dict):
    """Update user account information in the database."""
    try:
        valid_fields = ["email", "full_name"]
        filtered_updates = {k: v for k, v in updates.items() if k in valid_fields}
        
        if not filtered_updates:
            return json.dumps({"error": "No valid fields to update"})
            
        set_clause = ", ".join([f"{k} = :{k}" for k in filtered_updates.keys()])
        
        with engine.begin() as conn:
            query = text(f"UPDATE users SET {set_clause} WHERE id = :user_id")
            params = {"user_id": user_id, **filtered_updates}
            result = conn.execute(query, params)
            
            if result.rowcount > 0:
                return json.dumps({
                    "status": "success",
                    "message": "Account updated successfully",
                    "updated_fields": list(filtered_updates.keys())
                })
            return json.dumps({"error": "User not found"})
            
    except Exception as e:
        return json.dumps({"error": f"Database error: {str(e)}"})
