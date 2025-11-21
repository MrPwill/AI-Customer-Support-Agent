import json
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# GET root
root_response = client.get('/')
print('GET / status:', root_response.status_code)
print('GET / body:')
print(root_response.text)

# POST /chat
payload = {
    "message": "Check order ORD-123",
    "conversation_history": []
}
chat_response = client.post('/chat', json=payload)
print('POST /chat status:', chat_response.status_code)
print('POST /chat body:')
print(chat_response.text)
