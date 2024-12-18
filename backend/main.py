#!/usr/bin/env python

# filename: main.py

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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


@app.post("/api/chat-stream")
async def chatgpt_stream(cm: ChatMessage):
    async def response_generator():
        response = ""
        # for chunk in chat.request_chatgpt_stream(cm.chat_id):
        for chunk in chat.get_response_stream(cm.chat_id, cm.message):
            response += chunk
            yield chunk
        chat.append_message(cm.chat_id, {"role": "assistant", "content": response})
    return StreamingResponse(response_generator())


@app.post("/api/3ace6bf23d0dceb63ef7ad28469f336465ef6ce7f818a355cbb1f71907becc39")
async def chatgpt_stream(cm: ChatMessage):
    async def response_generator():
        response = ""
        # for chunk in chat.request_chatgpt_stream(cm.chat_id):
        for chunk in chat.get_response_stream_3ace6bf23d0dceb63ef7ad28469f336465ef6ce7f818a355cbb1f71907becc39(cm.chat_id, cm.message):
            response += chunk
            yield chunk
        chat.append_message(cm.chat_id, {"role": "assistant", "content": response})
    return StreamingResponse(response_generator())


@app.get("/api/chat-id")
async def get_chat_id():
    return {"chat_id": chat.get_new_chat_id()}


@app.get("/api/chat-history")
async def get_chat_history(chat_id: str):
    # 只保留assistant和user的信息，并且只保留有content的信息
    temp_history = chat.get_history(chat_id)
    history = []
    for message in temp_history:
        if message["role"] != "assistant" and message["role"] != "user":
            continue
        if not message["content"]:
            continue
        history.append({
            "role": message["role"],
            "content": message["content"]
        })
    return {"history": history}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    else:
        subprocess.run(["python3", "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"])
