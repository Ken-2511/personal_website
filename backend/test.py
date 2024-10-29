#!/usr/bin/python3

from chat import *


def test_get_response():
    delete_chat("test")
    # append_message("test", {"role": "user", "content": "Hello"})
    response = get_response_experimental("test", "what's your college?")


if __name__ == "__main__":
    text = "Hello, World! Hello World!"
    print(text.replace("Hello", "Hi"))