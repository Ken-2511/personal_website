#!/usr/bin/python3

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import subprocess
import chat


class ChatMessage(BaseModel):
    message: str
    chat_id: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# def get_response(message):
#     response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": message}],
#     )
#     return str(response.choices[0].message.content)


@app.post("/api/echo")
async def echo(message: str):
    return {"message": message}


@app.get("/api/hello")
async def hello():
    return {"message": "Hello, World!"}


@app.post("/api/chat")
async def chatgpt(cm: ChatMessage):
    response = chat.get_response(cm.chat_id, cm.message)
    return {"response": response}


@app.get("/api/chat-id")
async def get_chat_id():
    return {"chat_id": chat.get_new_chat_id()}


@app.get("/api/chat-history")
async def get_chat_history(chat_id: str):
    return {"history": chat.get_history(chat_id)}


if __name__ == '__main__':
    # note that when deploying, use host=127.0.0.1
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
