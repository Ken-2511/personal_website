#!/usr/bin/env python3

import os
import re
import json
import pickle
import random
import numpy as np
from openai import OpenAI
from diary_database.diary_database import DiaryDatabase, DiaryEntry

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class SearchEngine:
    def __init__(self, pkl_path: str = "diary_database/diary_processed.pkl"):
        """
        初始化时，直接加载 DiaryDatabase 而不进行转 JSON。
        """

        class CustomUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                if module == "diary_database" and name == "DiaryDatabase":
                    return DiaryDatabase
                elif module == "diary_database" and name == "DiaryEntry":
                    return DiaryEntry
                return super().find_class(module, name)

        if not os.path.exists(pkl_path):
            raise FileNotFoundError(f"未找到 {pkl_path} 文件，无法初始化搜索引擎。")

        with open(pkl_path, "rb") as f:
            self.db: DiaryDatabase = CustomUnpickler(f).load()
        # self.db.entries 是一个 List[DiaryEntry]
        # self.db.embeddings 是一个二维 np.ndarray，形状类似 (N, D)

    def get_embedding(self, text: str) -> np.ndarray:
        """
        使用 OpenAI 的 embedding API 生成文本向量。
        具体模型名称可根据需要替换。
        """
        text = text.replace("\n", " ")
        response = openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-large"  # 请根据实际可用的模型名称进行替换
        )
        embedding = np.array(response.data[0].embedding)
        return embedding

    def find_matching_diary_titles(self, query: str, n: int = 20) -> list:
        """
        通过一个 query 搜索日记（基于 content）的相似度，返回相似度最高的前 n 个日记标题。
        不使用 Python for 循环进行向量搜索，而是利用 NumPy 的向量化运算。
        
        返回结果示例：
        [
            {
                "index": int,
                "date": str,      # 形如 "2024-11-27"
                "title": str,
                "similarity": float,
            },
            ...
        ]
        """
        if self.db.embeddings is None or len(self.db.entries) == 0:
            return []

        # 1. 获取 query 的 embedding (D,)
        query_embedding = self.get_embedding(query)

        # 2. 计算与每篇日记的相似度 —— 利用向量化 @ 运算 (N, D) x (D,) -> (N,)
        similarities = self.db.embeddings @ query_embedding

        # 3. 按相似度从大到小获取索引
        sorted_indices = np.argsort(-similarities)  # np.argsort默认升序, 加负号变成降序
        top_n_indices = sorted_indices[:n].tolist()
        top_n_similarities = similarities[top_n_indices].tolist()

        # 4. 将结果组装成 list[dict]；这里使用列表推导式替代常规 for 循环
        results = [
            {
                "index": idx,
                "date": self.db.entries[idx].datetime[:10],  # 仅截取到 yyyy-mm-dd
                "title": self.db.entries[idx].title,
                "similarity": round(float(sim_score), 3),
            }
            for idx, sim_score in zip(top_n_indices, top_n_similarities)
        ]
        return results

    def fetch_diary_content(self, index: int) -> dict:
        """
        根据 index 获取对应日记的完整内容。
        返回结果示例：
        {
            "index": int,
            "date": str,
            "title": str,
            "content": str,
        }
        """
        # assert isinstance(index, int), "index 必须是整数。"
        if index < 0 or index >= len(self.db.entries):
            raise IndexError(f"索引 {index} 超出范围。")

        entry = self.db.entries[index]
        return {
            "index": index,
            "date": entry.datetime[:10],
            "title": entry.title,
            "content": entry.content,
        }

    def search_by_specific_word(self, word: str) -> list:
        """
        搜索包含某个词的日记片段。这里依然需要遍历每篇文章，
        但这部分与向量搜索无关，若你需要彻底去除 Python 循环，可改用全文检索工具等。
        返回结果示例：
        [
            {
                "index": int,
                "time": str,     # 形如 "2024-11-27"
                "title": str,
                "content": str,  # 匹配到的片段
            },
            ...
        ]
        """
        results = []
        for idx, entry in enumerate(self.db.entries):
            # 简单地根据标点把内容切分再查找
            content = entry.content.replace("\n", ".")
            segments = re.split(r"[,.?!;:，。？！；：]", content)
            for seg in segments:
                if word in seg:
                    results.append({
                        "index": idx,
                        "time": entry.datetime[:10],
                        "title": entry.title,
                        "content": seg.strip(),
                    })

        # 打乱后返回最多 15 条
        random.shuffle(results)
        return results[:15]


def test_chat_bot():
    """
    示例方法，演示如何在此文件中做测试性调用。
    也可替换为你项目中真正需要的聊天逻辑。
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",  # Replace with your actual model name
        messages=[
            {
                "role": "system",
                "content": "You're the diary content retrieval assistant for Yongkang Cheng. Your task is to efficiently retrieve relevant content from the structured diary database based on the user's query, prioritizing vector search for matching diary titles and content. Responsibilities and goals: 1. **Vector search first**: Use the `vector_search` tool to perform a vector search and return the most relevant diary titles (default is 10). 2. **Supplemental search**: If vector search results are insufficient, use `search_by_specific_word` to search for more diary content based on keywords in the query. 3. **Detailed content extraction**: Use `read_full_diary` to extract detailed diary content when necessary. 4. **Task completion**: Once enough information is gathered, use `enough_information_gathered` to notify task completion. Tool usage: 1. **vector_search**: Use this tool for vector search to return relevant diary titles. 2. **read_full_diary**: Extract diary content by index to supplement relevant information. 3. **search_by_specific_word**: Perform a keyword search to supplement diary snippets. 4. **enough_information_gathered**: Notify task completion when enough information is gathered.",
            },
            {"role": "user", "content": input("请输入你的问题: ")},
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "vector_search",
                    "description": "Find matching diary titles by calculating the similarity between the query and the diary content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The diary you want to search for."
                            },
                            "n": {
                                "type": "integer",
                                "enum": ["10", "20", "30"],
                                "description": "The number of diary titles you want to return."
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_full_diary",
                    "description": "Fetch the content of the diary by the index",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "index": {
                                "type": "integer",
                                "description": "The index of the diary you want to fetch."
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
                                "description": "The word you want to search for."
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

    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    se = SearchEngine("diary_database/diary_processed.pkl")

    # ===============  测试数据类型  ===============
    # print(se.db)
    
    # ===============  测试向量搜索  ===============
    # query = input("请输入搜索的内容(query): ")
    # matched_titles = se.find_matching_diary_titles(query, n=5)
    # print("\n[向量搜索] 相似度最高的5条日记：")
    # for item in matched_titles:
    #     print(item)

    # if matched_titles:
    #     # 测试 fetch_diary_content
    #     idx_for_detail = matched_titles[0]["index"]
    #     detail = se.fetch_diary_content(idx_for_detail)
    #     print("\n[查看最高相似度日记的内容]：")
    #     print(detail)
    #     print(json.dumps(detail, ensure_ascii=False, indent=4))

    # =============== 测试关键词检索  ===============
    # word_to_search = input("\n请输入要搜索的关键词: ")
    # segs = se.search_by_specific_word(word_to_search)
    # print("\n[关键词检索] 返回片段：")
    # for i, seg in enumerate(segs):
    #     print(i, seg)

    # =============== 测试聊天机器人  ===============
    test_chat_bot()