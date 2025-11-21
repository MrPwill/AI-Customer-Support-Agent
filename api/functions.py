import json
from database.queries import get_order_info_db, check_ticket_status_db, create_support_ticket_db, update_user_account_db

def get_order_info(order_id: str):
    """Fetch order details by order ID."""
    return get_order_info_db(order_id)

def check_ticket_status(ticket_id: str):
    """Check the status of a support ticket."""
    return check_ticket_status_db(ticket_id)

def create_support_ticket(user_id: str, subject: str, description: str):
    """Create a new support ticket."""
    try:
        uid = int(user_id)
    except ValueError:
        # For demo purposes, if not int, try to lookup or default. 
        # But let's just return error.
        return json.dumps({"error": "Invalid user_id. Must be numeric for this demo."})
    return create_support_ticket_db(uid, subject, description)

def update_user_account(user_id: str, email: str = None, full_name: str = None):
    """Update user account details."""
    try:
        uid = int(user_id)
    except ValueError:
        return json.dumps({"error": "Invalid user_id. Must be numeric."})
    
    updates = {}
    if email:
        updates["email"] = email
    if full_name:
        updates["full_name"] = full_name
        
    if not updates:
        return json.dumps({"error": "No updates provided."})
        
    return update_user_account_db(uid, updates)

# Tool Definitions for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_order_info",
            "description": "Get details about a specific order including status and delivery date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID, e.g., ORD-123"
                    }
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_ticket_status",
            "description": "Check the current status of a customer support ticket.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "The ticket ID, e.g., TKT-001"
                    }
                },
                "required": ["ticket_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_support_ticket",
            "description": "Create a new support ticket for a user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The ID of the user creating the ticket"
                    },
                    "subject": {
                        "type": "string",
                        "description": "The subject or title of the issue"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the issue"
                    }
                },
                "required": ["user_id", "subject", "description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_user_account",
            "description": "Update user account information like email or name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The ID of the user"
                    },
                    "email": {
                        "type": "string",
                        "description": "New email address (optional)"
                    },
                    "full_name": {
                        "type": "string",
                        "description": "New full name (optional)"
                    }
                },
                "required": ["user_id"]
            }
        }
    }
]

def execute_function(function_name, args):
    if function_name == "get_order_info":
        return get_order_info(args.get("order_id"))
    elif function_name == "check_ticket_status":
        return check_ticket_status(args.get("ticket_id"))
    elif function_name == "create_support_ticket":
        return create_support_ticket(args.get("user_id"), args.get("subject"), args.get("description"))
    elif function_name == "update_user_account":
        return update_user_account(args.get("user_id"), args.get("email"), args.get("full_name"))
    else:
        return json.dumps({"error": "Function not found"})
