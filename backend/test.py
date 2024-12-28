#!/usr/bin/env python

import json
import chat
import subprocess
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")


def print_history(chat_id, chat_only=True):
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
                if chat_only:
                    continue
                for tool in message["tool_calls"]:
                    tool = tool["function"]
                    print("Assistant (tool)")
                    print(f"{tool['name']}, args: {tool['arguments']}\n")
            # 如果没有使用tool
            else:
                print("Assistant:\n" + message["content"] + "\n")
        # 如果是tool
        elif message["role"] == "tool":
            if chat_only:
                continue
            print("Tool:")
            print(json.loads(message["content"]))
            print()
        # 如果是system
        elif message["role"] == "system":
            if chat_only:
                continue
            print("System:\n" + message["content"] + "\n")
        else:
            assert False


def print_all_diaries():
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


def print_all_chat_ids():
    db = client["test_database"]
    collection = db["chat_history"]
    chat_ids = collection.distinct("chat_id")
    for chat_id in chat_ids:
        print(chat_id)


def print_all_history(chat_only=True):
    # get all chat ids
    db = client["test_database"]
    collection = db["chat_history"]
    chat_ids = collection.distinct("chat_id")
    for chat_id in chat_ids:
        subprocess.run(["clear"])
        print(f"Chat ID: {chat_id}")
        print_history(chat_id, chat_only)
        input("Press enter to continue")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--history", action="store_true")
    parser.add_argument("--diaries", action="store_true")
    parser.add_argument("--chat_ids", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    if args.history:
        chat_id = input("Enter chat_id: ")
        print_history(chat_id, chat_only=False)
    if args.diaries:
        print_all_diaries()
    if args.chat_ids:
        print_all_chat_ids()
    if args.all:
        print_all_history(chat_only=False)