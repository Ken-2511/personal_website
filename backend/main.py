from fastapi import FastAPI
from pydantic import BaseModel


class ChatMessage(BaseModel):
    message: str


app = FastAPI()

@app.post("/echo")
async def echo(message: str):
    return {"message": message}

@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}

@app.post("/api/chat")
async def chat(cm: ChatMessage):
    return {"response": cm.message}