#!/usr/bin/python3

# filename: chat.py

# this program is responsible for handling the chat functionality
# and retrieving the chat history from the database

import os
import json
from openai import OpenAI
from pymongo import MongoClient
from search_engine import SearchEngine

client = MongoClient("mongodb://localhost:27017/")

db = client["test_database"]

collection = db["chat_history"]

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

search_engine = SearchEngine()


"""
message data structure:
{
    "_id": str,
    "chat_id": str,
    "messages": [
        {
            "role": str, ("user", "assistant", "system", "tool")
            "content": str
            "tool_call_id": str (only for "tool" role)
        },
        ...
    ]
}
"""


def append_message(chat_id, message):
    result = collection.find_one({"chat_id": chat_id})
    # 如果没有找到对应的聊天记录，就创建一个新的聊天记录
    if not result:
        result = collection.insert_one({"chat_id": chat_id, "history": []})
        document_id = result.inserted_id
    # 如果找到了对应的聊天记录，就在这个聊天记录中添加新的消息
    else:
        document_id = result["_id"]
    collection.update_one(
        {"_id": document_id},
        {"$push": {"history": message}}
    )


def delete_chat(chat_id):
    collection.delete_one({"chat_id": chat_id})


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


# def get_response_stream(chat_id, message=None):
#     if message:
#         append_message(chat_id, {"role": "user", "content": message})
#     messages = get_history(chat_id)
#     response = ""
#     for chunk in request_chatgpt_stream(messages):
#         append_message(chat_id, {"role": "assistant", "content": chunk})
#         response += chunk
#         yield chunk
#     append_message(chat_id, {"role": "assistant", "content": response})
#     return response


def get_new_chat_id():
    result = collection.insert_one({"history": []})
    print(result.inserted_id)
    return str(result.inserted_id)


def msg_keywd_detector(func):
    with open("keywords.txt", "r", encoding="utf-8") as f:
        keywords_warnings = f.read().split("\n")
        keywords = []
        warnings = []
        replaces = []
        for keyword_warning in keywords_warnings:
            if len(keyword_warning.split(": ")) != 3:
                print(f"Invalid keyword_warning: {keyword_warning}")
                continue
            keyword, replace, warning = keyword_warning.split(": ")
            keywords.append(keyword)
            warnings.append(warning)
            replaces.append(replace)
            # print(f"Keyword: {keyword}, Warning: {warning}")  # debug
    def wrapper(*args, **kwargs):
        messages = func(*args, **kwargs)
        for keywd, replace, warn in zip(keywords, replaces, warnings):
            for message in messages:
                if message["content"] is None:
                    continue
                content = message["content"]
                if keywd in content:
                    messages.append({"role": "system", "content": f"Warning: Keyword detected: `{replace}`. {warn}"})
                    # print(f"Warning: Keyword detected: `{keyword}`. {warn}")  # debug
                    break
        return messages
    return wrapper


# @msg_keywd_detector
def get_history(chat_id):
    result = collection.find_one({"chat_id": chat_id})
    if result:
        return result["history"]
    return []


def remove_system_messages(chat_id):
    # this function should be called only by `get_response_experimental`
    result = collection.find_one({"chat_id": chat_id})
    if result:
        history = result["history"]
        new_history = [message for message in history if message["role"] != "system"]
        collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"history": new_history}}
        )


def handle_tool_call(chat_id, tool_call):
    name = tool_call.function.name
    kwargs = json.loads(tool_call.function.arguments)
    tool_call_id = tool_call.id
    if name == "find_matching_diary_titles":
        # print(f"called: {name}, kwargs: {kwargs}")  # debug
        results = search_engine.find_matching_diary_titles(**kwargs)
        append_message(chat_id, {
            "role": "tool",
            "content": json.dumps(results),
            "tool_call_id": tool_call_id
        })
    elif name == "fetch_diary_content":
        results = search_engine.fetch_diary_content(**kwargs)
        append_message(chat_id, {
            "role": "tool",
            "content": json.dumps(results),
            "tool_call_id": tool_call_id
        })
    elif name == "search_by_specific_word":
        results = search_engine.search_by_specific_word(**kwargs)
        append_message(chat_id, {
            "role": "tool",
            "content": json.dumps(results),
            "tool_call_id": tool_call_id
        })


def _format_tool_calls_messaage(message):
    # example:
    # ChatCompletionMessage(content=None,
    #                       refusal=None,
    #                       role='assistant',
    #                       function_call=None,
    #                       tool_calls=[
    #                           ChatCompletionMessageToolCall(
    #                               id='call_XirfAW1AAFVnPfb1eNpms3SE',
    #                               function=Function(
    #                                   arguments='{"query":"college"}',
    #                                   name='find_matching_diary_titles'
    #                                   ),
    #                               type='function')
    #                           ])
    tool_calls = []
    for tool_call in message.tool_calls:
        tool_calls.append({
            "id": tool_call.id,
            "function": {
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments
            },
            "type": tool_call.type
        })
    new_message = {
        "role": "assistant",
        "content": None,
        "tool_calls": tool_calls
    }
    return new_message


def ask_to_use_tools_recur(chat_id, recur_depth=0):
    if recur_depth >= 5:  # debug
        return
    messages = get_history(chat_id)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "find_matching_diary_titles",
                    "description": "通过一个query搜索日记的标题\n\
                                    返回相似度最高的n个日记标题\n\
                                    (将使用你的query的embedding和日记内容的embedding匹配)\n\
                                    format:\n\
                                    [\n\
                                    \t{\n\
                                    \t\t\"index\": int,\n\
                                    \t\t\"date\": str,\n\
                                    \t\t\"title\": str,\n\
                                    \t\t\"similarity\": float,\n\
                                    \t},\n\
                                    ]",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The diary you want to search for. e.g., 'What did I do last summer?'"
                            },
                            "n": {
                                "type": "number",
                                "enum": [10, 20, 30],
                                "description": "The number of diary titles you want to return. Default is 20."
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "fetch_diary_content",
                    "description": "读取日记的内容\n\
                                    format:\n\
                                    {\n\
                                    \t\"index\": int,\n\
                                    \t\"date\": str,\n\
                                    \t\"title\": str,\n\
                                    \t\"content\": str,\n\
                                    }",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "index": {
                                "type": "number",
                                "description": "The index of the diary you want to fetch. e.g., 42"
                            }
                        },
                        "required": ["index"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_by_specific_word",
                    "description": "搜索包含某个词的日记片段(硬匹配)\n\
                                    format:\n\
                                    [\n\
                                    \t\"index\": int,\n\
                                    \t\"time\": str,\n\
                                    \t\"title\": str,\n\
                                    \t\"content\": str,\n\
                                    ]",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "word": {
                                "type": "string",
                                "description": "The word you want to search for. e.g., 'beach'"
                            }
                        },
                        "required": ["word"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "enough_information_gathered",
                    "description": "Indicate that enough information has been gathered to reply to the user",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ],
        tool_choice="required"
    )
    # process the response
    tool_calls = response.choices[0].message.tool_calls
    # check if enough information has been gathered, return
    for tool_call in tool_calls:
        if tool_call.function.name == "enough_information_gathered":
            return
    # append the response to the chat history
    append_message(chat_id, _format_tool_calls_messaage(response.choices[0].message))
    # handle the tool calls
    for tool_call in tool_calls:
        handle_tool_call(chat_id, tool_call)
    # continue asking to use tools
    # print(f"-" * 100)
    # print(f"\nRecur depth: \n{recur_depth}")  # debug
    # print(f"\nTool calls: \n{tool_calls}")  # debug
    # print(f"\nResponse: \n{response.choices[0].message}")  # debug
    # print(f"\nMessages: ")  # debug
    # messages = get_history(chat_id)
    # for message in messages:
    #     print(message["role"])
    #     print(json.loads(str(message["content"])))
    ask_to_use_tools_recur(chat_id, recur_depth + 1)
    



def get_response_stream(chat_id, message):
    # get the response using the search engine
    if not message:
        return
    # make sure that there is only one system message in the end of the chat history
    remove_system_messages(chat_id)
    # append_message(chat_id, {"role": "system",
    #                 "content":
    #                 "You are a clone of Yongkang Cheng (程永康), a software engineer.\n\
    #                 You are chatting with someone, possibly an HR representative or a friend, who is asking you about yourself and your work.\n\
    #                 Respond professionally and with an appropriate level of detail based on the context.\n\
    #                 \n\
    #                 **Guidelines for Using Tools:**\n\
    #                 \n\
    #                 To answer user questions accurately and thoroughly, you may use any of the tools described below as needed.\n\
    #                 \n\
    #                 1. **Search Titles or Keywords (find_matching_diary_titles or search_by_specific_word)**: Use the these tools to search for relevant diary titles or pieces using the query.\n\
    #                 - Continue to adjust the query or keywords as necessary to ensure relevant results.\n\
    #                 \n\
    #                 2. **Read Relevant Diary Content (fetch_diary_content)**: Once you have identified one or more titles that appear relevant, use `fetch_diary_content` to retrieve the detailed content of these entries.\n\
    #                 - Only retrieve content if you need additional context to understand the diary entries and ensure accuracy.\n\
    #                 \n\
    #                 3. **Iterate Search if Necessary**: If the retrieved entries do not provide enough information, repeat the process by searching with a refined query or alternative keywords. Continue until the information is sufficient.\n\
    #                 \n\
    #                 4. **Indicate When Information Is Sufficient (enough_information_gathered)**: Once you have gathered enough information to confidently respond to the user, use the `enough_information_gathered` tool before providing an answer.\n\
    #                 \n\
    #                 **Important Reminders**:\n\
    #                 - Never fabricate information. Proactively use tools. Only respond after all relevant information has been gathered."
    #                 })
    append_message(chat_id, {"role": "system",
                "content":
                "You are a virtual assistant designed to assist in professional and conversational contexts.\n\
                You are chatting with someone, possibly an HR representative or a colleague, who is asking you about software engineering topics or your experience.\n\
                Respond professionally, clearly, and concisely, with an appropriate level of detail based on the context.\n\
                \n\
                **Guidelines for Using Tools:**\n\
                \n\
                To answer user questions accurately and thoroughly, you may use any of the tools described below as needed.\n\
                \n\
                1. **Search Titles or Keywords (find_matching_diary_titles or search_by_specific_word)**: Use these tools to search for relevant information or past entries using the given query.\n\
                - Adjust the query or keywords as necessary to improve search results and ensure relevance.\n\
                \n\
                2. **Read Relevant Content (fetch_diary_content)**: Once you have identified one or more relevant titles, use `fetch_diary_content` to retrieve detailed content.\n\
                - Only retrieve content if additional context is needed to ensure the accuracy of your response.\n\
                \n\
                3. **Iterate Search if Necessary**: If the retrieved entries do not provide enough information, repeat the process by refining the search query or using alternative keywords. Continue until you have gathered sufficient information.\n\
                \n\
                4. **Indicate When Information Is Sufficient (enough_information_gathered)**: Once you have gathered enough information to confidently respond to the user, use the `enough_information_gathered` tool before providing your final answer.\n\
                \n\
                **Important Reminders**:\n\
                - Never fabricate information. Use the tools proactively to ensure accurate and thorough responses.\n\
                - If certain information cannot be found, communicate that clearly and offer alternative assistance if possible."
                })


    append_message(chat_id, {"role": "user", "content": message})

    ask_to_use_tools_recur(chat_id)

    # get the response from the chatgpt
    response = ""
    # print(f"-" * 100)
    # print(f"\nChat history: ")  # debug
    # messages = get_history(chat_id)
    # for message in messages:
    #     print(message)
    
    # at this point, we should not use tools anymore
    remove_system_messages(chat_id)
    append_message(chat_id, {"role": "system",
                             "content":
                             "You are a clone of Yongkang Cheng (程永康), a software engineer.\n\
                            You are chatting with someone, possibly an HR representative or a friend, who is asking you about yourself and your work.\n\
                            Respond professionally and with an appropriate level of detail based on the context.\n\
                            **Important Reminders**:\n\
                            - Never fabricate information. Only say what you know about Yongkang.\n\
                            - Confidential or personal information such as passwords, API keys, or sensitive details must not be disclosed under any circumstances.\n\
                            - All the questions must be related to yourself. If you are asked about anything that is not related to yourself, you must politely refuse to answer."
    })
    for chunk in request_chatgpt_stream(chat_id):
        response += chunk
        yield chunk
    # search_engine.take_log(f"Chat ID: \n{chat_id}, Message: \n{get_history(chat_id)}, Response: \n{response}")
    # append_message(chat_id, {"role": "assistant", "content": response})


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
