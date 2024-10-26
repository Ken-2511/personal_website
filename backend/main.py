from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os


class ChatMessage(BaseModel):
    message: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("OPENAI_API_KEY")
print(api_key)
client = OpenAI(api_key=api_key)

def get_response(message):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": message}],
    )
    return str(response.choices[0].message.content)


@app.post("/echo")
async def echo(message: str):
    return {"message": message}

@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}

@app.post("/api/chat")
async def chat(cm: ChatMessage):
    print("Message: ", cm.message)
    response = get_response(cm.message)
    print(response)
    return {"response": response}