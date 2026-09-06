import os
from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI(title="Autonomous Personal AI Agent Core")

class UserCommand(BaseModel):
    command: str

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

@app.get("/")
def home():
    return {"status": "AI Agent Brain is Online 24/7", "agent": "Einstein"}

@app.post("/ask")
async def ask_agent(data: UserCommand):
    if not GROQ_API_KEY:
        return {"error": "Groq API Key সেট করা হয়নি!"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are Einstein, a personal autonomous AI assistant."},
                    {"role": "user", "content": data.command}
                ]
            },
            timeout=30.0
        )
        res_data = response.json()
        if response.status_code != 200:
            return {"error": f"Groq API Error: {res_data}"}
        
        try:
            answer = res_data["choices"][0]["message"]["content"]
            return {"agent_response": answer}
        except Exception as e:
            return {"error": f"Parsing Error: {str(e)}, Response: {res_data}"}
