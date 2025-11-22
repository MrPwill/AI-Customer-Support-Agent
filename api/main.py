from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Optional
import json
from api.functions import tools, execute_function
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are a helpful and professional AI customer support agent for a tech store.
Your tone should be polite, concise, and solution-oriented.
Always verify user identity before providing sensitive information (in this demo, we assume the user is authenticated via their user_id).
If you cannot help, politely offer to escalate the ticket.
"""

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()

app = FastAPI(title="AI Customer Support Agent")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENROUTER_API_KEY")
)

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[dict]] = []

@app.post("/chat")
async def chat(request: ChatRequest):
    logger.info(f"Received message: {request.message}")
    
    # Prepend system prompt if not present
    if not request.conversation_history or request.conversation_history[0].get("role") != "system":
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + request.conversation_history
    else:
        messages = request.conversation_history
        
    messages.append({"role": "user", "content": request.message})
    
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3.1", # Verify exact model name on OpenRouter
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        if response_message.tool_calls:
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                function_response = execute_function(function_name, function_args)
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
            
            # Get final response from model
            second_response = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3.1",
                messages=messages
            )
            return {"response": second_response.choices[0].message.content, "history": messages}
            
        return {"response": response_message.content, "history": messages + [{"role": "assistant", "content": response_message.content}]}
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
