#!/usr/bin/python3

# filename: chat.py

# this program is responsible for handling the chat functionality
# and retrieving the chat history from the database

import os
from openai import OpenAI
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["test_database"]

collection = db["chat_history"]

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


"""
message data structure:
{
    "_id": str,
    "chat_id": str,
    "messages": [
        {
            "role": str,
            "content": str
        },
        ...
    ]
}
"""


def append_message(chat_id, role, message):
    result = collection.find_one({"chat_id": chat_id})
    if not result:
        result = collection.insert_one({"chat_id": chat_id, "history": []})
        document_id = result.inserted_id
    else:
        document_id = result["_id"]
    collection.update_one(
        {"_id": document_id},
        {"$push": {"history": {"role": role, "content": message}}}
    )


def request_chatgpt_stream(chat_id, model="gpt-4o-mini"):
    messages = get_history(chat_id)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


def get_response_stream(chat_id, message=None):
    if message:
        append_message(chat_id, "user", message)
    messages = get_history(chat_id)
    response = ""
    for chunk in request_chatgpt_stream(messages):
        append_message(chat_id, "assistant", chunk)
        response += chunk
        yield chunk
    append_message(chat_id, "assistant", response)
    return response


def get_new_chat_id():
    count = 0
    while True:
        chat_id = str(count)
        if not collection.find_one({"chat_id": chat_id}):
            return chat_id
        count += 1


def get_history(chat_id):
    result = collection.find_one({"chat_id": chat_id})
    if result:
        return result["history"]
    return []


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--print", help="Print chat history", action="store_true")
    parser.add_argument("--clear", help="Clear chat history", action="store_true")
    parser.add_argument("--test", help="Test", action="store_true")
    args = parser.parse_args()
    if args.print:
        chats = collection.find()
        for chat in chats:
            print(chat, end="\n\n")
    if args.clear:
        ans = input("Are you sure you want to delete the chat history? (y/n) ")
        if ans.lower() == "y":
            collection.drop()
            print("Collection deleted.")
        else:
            print("No changes made")
    if args.test:
        print("Test")
