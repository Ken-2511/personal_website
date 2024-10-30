#!/usr/bin/python3

import json
import chat
from pymongo import MongoClient


def print_history():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["test_database"]
    collection = db["chat_history"]
    chat_id = input("Enter chat_id: ")
    history = chat.get_history(chat_id)
    for message in history:
        # print(message)
        # 如果是user
        if message["role"] == "user":
            print("User:\n" + message["content"] + "\n")
        # 如果是assistant
        elif message["role"] == "assistant":
            # 如果使用了tool
            if "tool_calls" in message:
                for tool in message["tool_calls"]:
                    tool = tool["function"]
                    print("Assistant (tool)")
                    print(f"{tool['name']}, args: {tool['arguments']}\n")
            # 如果没有使用tool
            else:
                print("Assistant:\n" + message["content"] + "\n")
        # 如果是tool
        elif message["role"] == "tool":
            print("Tool:")
            print(json.loads(message["content"]))
            print()
        # 如果是system
        elif message["role"] == "system":
            print("System:\n" + message["content"] + "\n")
        else:
            assert False


def print_all_diaries():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["personal_website"]
    collection = db["diaries"]
    diaries = collection.find()
    for diary in diaries:
        print("-" * 100)
        print("Title:")
        print(diary["title"])
        print()
        print("Content:")
        print(diary["content"])
        print()


if __name__ == "__main__":
    print_history()
    # print_all_diaries()