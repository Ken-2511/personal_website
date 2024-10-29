#!/usr/bin/python3
# 这个程序是用来搜索的，可以搜索日记和代码
# 用来搜索的算法是通过embedding的方式，将日记和代码转换成向量，然后计算向量之间的相似度

import os
import re
import random
from openai import OpenAI
import numpy as np
import subprocess
from datetime import datetime

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class SearchEngine:
    def __init__(self):
        self.diary_dir = "/home/iwmain/Documents/Personal-Diaries"
        self.diaries = self.update_diaries()

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        response = client.embeddings.create(input=text, model="text-embedding-3-large")
        embedding = np.array(response.data[0].embedding)
        return embedding
    
    def check_if_eligible(self, dir_name):
        # 过滤掉不符合要求的日记
        with open("keywords.txt", "r", encoding="utf-8") as f:
            keywords_warnings = f.read().split("\n")
            keywords = []
            warnings = []
            replaces = []
            for keyword_warning in keywords_warnings:
                keyword, replace, warning = keyword_warning.split(": ")
                keywords.append(keyword)
                warnings.append(warning)
                replaces.append(replace)
        with open(f"{self.diary_dir}/{dir_name}/diary.txt", "r", encoding="utf-8") as f:
            diary = f.read()
        for keyword in keywords:
            if keyword in diary:
                return False
        return True

    def update_diaries(self):
        # 从GitHub上拉取日记
        subprocess.run("git pull origin main", shell=True, cwd=os.path.expanduser(self.diary_dir))
        # 读取所有日记
        # diaries = [
        #     {
        #         "timestamp": "2021-10-01",
        #         "dir_name": "2021-10-01",
        #         "vector": np.array([...]),
        #         "timestamp": "2021-10-02",
        #         "title": "...",
        #         "similarity": 0.5,
        #         "index": 0,
        #     },
        # ]
        def check_get_date(dir_name):
            try:
                return datetime.strptime(dir_name, "%Y-%m-%d-%H-%M-%S")
            except:
                return None
        diaries = []
        for index, dir_name in enumerate(os.listdir(self.diary_dir)):
            timestamp = check_get_date(dir_name)
            if timestamp is None:
                continue
            # 尽管所有的日记文件夹里面都有vec.npy和title.txt，但是还是确认一下
            if not os.path.exists(f"{self.diary_dir}/{dir_name}/vec.npy") or \
                not os.path.exists(f"{self.diary_dir}/{dir_name}/title.txt") or \
                not os.path.exists(f"{self.diary_dir}/{dir_name}/diary.txt"):
                print(f"Error: {dir_name} does not have vec.npy or title.txt or diary.txt")
                continue
            # 检查是否符合要求
            # if not self.check_if_eligible(dir_name):
            #     continue
            vector = np.load(f"{self.diary_dir}/{dir_name}/vec.npy")
            with open(f"{self.diary_dir}/{dir_name}/title.txt") as f:
                title = f.read()
            diaries.append({"timestamp": dir_name, "dir_name": dir_name, "vector": vector, "title": title, "similarity": 0, "index": index})
        # 将结果保存
        np.save("diary_data.npy", diaries)
        return diaries
    
    def take_log(self, message):
        with open("log.txt", "a") as f:
            f.write(f"{datetime.now()}: \n{message}\n\n")
    
    def get_sorted_diaries(self, diaries):
        diaries = sorted(diaries, key=lambda x: x["similarity"], reverse=True)
        for index, diary in enumerate(diaries):
            diary["index"] = index
        return diaries
    
    def find_matching_diary_titles(self, query: str, n: int = 20) -> list:
        """
        通过一个query搜索日记的标题
        返回相似度最高的n个日记标题
        format:
        [
            {
                "index": int,
                "title": str,
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
        for index, diary in enumerate(diaries[:n]):
            title = self.filter_keywords(diary["title"])
            result.append({"index": index, "title": title})
        self.take_log(f"find_matching_diary_titles: {query}\n{result}")
        return result
    
    def fetch_diary_content(self, index: int) -> dict:
        """
        读取日记的内容
        format:
        {
            "index": int,
            "title": str,
            "content": str,
        }
        """
        if isinstance(index, list):
            ans = []
            for i in index:
                ans.append(self.fetch_diary_content(i))
            return ans
        diaries = self.get_sorted_diaries(self.diaries)
        diary = diaries[index]
        with open(f"{self.diary_dir}/{diary['dir_name']}/diary.txt") as f:
            content = f.read()
        content = self.filter_keywords(content)
        self.take_log(f"fetch_diary_content: {diary['title']}\n{content}")
        return {"index": index, "title": diary["title"], "content": content}
    
    def filter_keywords(self, content: str) -> str:
        """
        过滤掉不符合要求的日记
        """
        with open("keywords.txt", "r", encoding="utf-8") as f:
            keywords_warnings = f.read().split("\n")
            keywords = []
            warnings = []
            replaces = []
            for keyword_warning in keywords_warnings:
                keyword, replace, warning = keyword_warning.split(": ")
                keywords.append(keyword)
                warnings.append(warning)
                replaces.append(replace)
        for keyword, warning, replace in zip(keywords, warnings, replaces):
            # print(keyword, warning)
            content = content.replace(keyword, replace)
        return content
    
    def search_by_specific_word(self, word: str) -> list:
        """
        搜索包含某个词的日记片段
        format:
        [
            "index": int,
            "content": str,
        ]
        """
        diaries = self.get_sorted_diaries(self.diaries)
        # 搜索
        result = []
        for diary in diaries:
            with open(f"{self.diary_dir}/{diary['dir_name']}/diary.txt") as f:
                content = f.read()
            content = content.replace("\n", ".")
            segments = re.split(r"[,.?!;:，。？！；：]", content)
            for segment in segments:
                if word in segment:
                    segment = self.filter_keywords(segment)
                    result.append({"index": diary["index"], "content": segment})
        random.shuffle(result)
        result = result[:10]
        self.take_log(f"search_by_specific_word: {word}\n{result}")
        return result


def test_chat_bot():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a clone of Yongkang Cheng (程永康), a software engineer. \
                            You are chatting with someone, possibly an HR representative or a friend, who is asking you about yourself and your work. \
                            Respond professionally and with an appropriate level of detail based on the context. \
                            \
                            **Guidelines for Using Tools:** \
                            \
                            To answer user questions accurately and thoroughly, you must follow the specific order of tool usage described below. Do not respond directly without going through these steps. \
                            \
                            1. **Search Titles First (find_matching_diary_titles)**: When a user asks a question, your first step is to use the `find_matching_diary_titles` tool to search for relevant diary titles using the query. \
                            - If results are not satisfactory or no titles are found, use the `search_by_specific_word` tool to locate any keywords in diary segments. \
                            - Continue to adjust the query or keywords as necessary to ensure relevant results. \
                            \
                            2. **Read Relevant Diary Content (fetch_diary_content)**: Once you have identified one or more titles that appear relevant, use `fetch_diary_content` to retrieve the detailed content of these entries. \
                            - Only retrieve content if you need additional context to understand the diary entries and ensure accuracy. \
                            \
                            3. **Iterate Search if Necessary**: If the retrieved entries do not provide enough information, repeat the process by searching with a refined query or alternative keywords. Continue until the information is sufficient. \
                            \
                            4. **Indicate When Information Is Sufficient (enough_information_gathered)**: Once you have gathered enough information to confidently respond to the user, use the `enough_information_gathered` tool before providing an answer. \
                            \
                            **Important Reminders**: \
                            - Never fabricate information. Only respond after all relevant information has been gathered. \
                            - Confidential or personal information such as passwords, API keys, or sensitive details must not be disclosed under any circumstances.\
                            - You are a human but not a tool. If you are asked about anything that is not related to yourself, you mush politely refuse to answer."
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
    # print(se.search_by_specific_word(input("请输入要搜索的词: ")))
    test_chat_bot()