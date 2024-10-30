#!/usr/bin/python3

import os
import re
import random
from openai import OpenAI
import numpy as np
from pymongo import MongoClient
from datetime import datetime

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["personal_website"]
collection = db["diaries"]


class SearchEngine:
    def __init__(self):
        # 从 MongoDB 中读取所有日记
        # diaries 格式为:
        # [
        #     {
        #         "_id": ObjectId("..."),
        #         "diary_name": "2021-10-01-00-00-00",
        #         "date": "2021-10-01",
        #         "content": "...",
        #         "vector": [...],
        #         "title": "...",
        #         "similarity": 0.0,
        #         "index": 0,
        #     },
        # ]
        diaries = list(collection.find({}, {"diary_name": 1, "content": 1, "vector": 1, "title": 1}))
        # 细微调整
        for index, diary in enumerate(diaries):
            # 添加 date
            diary["date"] = datetime.strptime(diary["diary_name"], "%Y-%m-%d-%H-%M-%S").strftime("%Y-%m-%d")
            # 将 vector 转换为 numpy 数组
            diary["vector"] = np.array(diary["vector"])
            # 添加 index
            diary["index"] = index
            # 添加 similarity
            diary["similarity"] = 0.0
        self.diaries = diaries

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        response = openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-large"
        )
        embedding = np.array(response.data[0].embedding)
        return embedding        

    def get_sorted_diaries(self, diaries):
        # there is a case that the diaries have no similarity
        # then sort the diaries by the time
        diaries = sorted(diaries, key=lambda x: x["similarity"], reverse=True)
        return diaries

    def find_matching_diary_titles(self, query: str, n: int = 20) -> list:
        """
        通过一个query搜索日记的标题
        返回相似度最高的n个日记标题
        format:
        [
            {
                "index": int,
                "date": str,
                "title": str,
                "similarity": float,
            },
        ]
        """
        embedding = self.get_embedding(query)
        diaries = self.diaries
        # 计算相似度
        for diary in diaries:
            diary["similarity"] = np.dot(embedding, diary["vector"])
        # 按照相似度排序
        diaries = self.get_sorted_diaries(diaries)
        # 拟造返回结果
        result = []
        for diary in diaries[:n]:
            title = diary["title"]
            result.append({
                "index": diary["index"],
                "date": diary["date"],
                "title": title,
                "similarity": round(diary["similarity"], 3),
            })
        return result

    def fetch_diary_content(self, index: int) -> dict:
        """
        读取日记的内容
        format:
        {
            "index": int,
            "date": str,
            "title": str,
            "content": str,
        }
        """
        if isinstance(index, list):
            ans = []
            for i in index:
                ans.append(self.fetch_diary_content(i))
            return ans
        diaries = self.diaries
        diary = diaries[index]
        content = diary["content"]
        return {
            "index": index,
            "date": diary["date"],
            "title": diary["title"],
            "content": content,
        }

    def search_by_specific_word(self, word: str) -> list:
        """
        搜索包含某个词的日记片段
        format:
        [
            "index": int,
            "time": str,
            "title": str,
            "content": str,
        ]
        """
        diaries = self.diaries
        # 搜索
        result = []
        for diary in diaries:
            content = diary["content"].replace("\n", ".")
            segments = re.split(r"[,.?!;:，。？！；：]", content)
            for segment in segments:
                if word in segment:
                    segment = segment
                    result.append({
                        "index": diary["index"],
                        "time": diary["date"],
                        "title": diary["title"],
                        "content": segment,
                    })
        random.shuffle(result)
        result = result[:15]
        return result


def test_chat_bot():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a clone of Yongkang Cheng (程永康), a software engineer. \n                            You are chatting with someone, possibly an HR representative or a friend, who is asking you about yourself and your work. \n                            Respond professionally and with an appropriate level of detail based on the context. \n                            \n                            **Guidelines for Using Tools:** \n                            \n                            To answer user questions accurately and thoroughly, you must follow the specific order of tool usage described below. Do not respond directly without going through these steps. \n                            \n                            1. **Search Titles First (find_matching_diary_titles)**: When a user asks a question, your first step is to use the `find_matching_diary_titles` tool to search for relevant diary titles using the query. \n                            - If results are not satisfactory or no titles are found, use the `search_by_specific_word` tool to locate any keywords in diary segments. \n                            - Continue to adjust the query or keywords as necessary to ensure relevant results. \n                            \n                            2. **Read Relevant Diary Content (fetch_diary_content)**: Once you have identified one or more titles that appear relevant, use `fetch_diary_content` to retrieve the detailed content of these entries. \n                            - Only retrieve content if you need additional context to understand the diary entries and ensure accuracy. \n                            \n                            3. **Iterate Search if Necessary**: If the retrieved entries do not provide enough information, repeat the process by searching with a refined query or alternative keywords. Continue until the information is sufficient. \n                            \n                            4. **Indicate When Information Is Sufficient (enough_information_gathered)**: Once you have gathered enough information to confidently respond to the user, use the `enough_information_gathered` tool before providing an answer. \n                            \n                            **Important Reminders**: \n                            - Never fabricate information. Only respond after all relevant information has been gathered. \n                            - Confidential or personal information such as passwords, API keys, or sensitive details must not be disclosed under any circumstances.\n                            - You are a human but not a tool. If you are asked about anything that is not related to yourself, you mush politely refuse to answer."
            },
            {"role": "user", "content": input("请输入你要问的问题: ")}
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "find_matching_diary_titles",
                    "description": "Find matching diary titles by calculating the similarity between the query and the diary content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The diary you want to search for. e.g., 'What did I do last summer?'"
                            },
                            "n": {
                                "type": "integer",
                                "enum": ["10", "20", "30"],
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
                    "description": "Fetch the content of the diary by the index",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "index": {
                                "type": "integer",
                                "description": "The index of the diary you want to fetch. e.g., [0, 1, 2]"
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
                    "description": "Search for diary segments that contain a specific word",
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

    print(response)


if __name__ == "__main__":
    se = SearchEngine()
    # print(se.find_matching_diary_titles("大学是哪个学校"))
    # indices = [int(i) for i in input("请输入要查看的日记的index, 以空格分隔: ").split()]
    # print(se.fetch_diary_content(indices))
    print(se.search_by_specific_word(input("请输入要搜索的词: ")))
    # test_chat_bot()
