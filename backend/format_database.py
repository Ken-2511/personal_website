#!/usr/bin/python3
# filename: format_database.py

import os
import json
import numpy as np
from pymongo import MongoClient
from openai import OpenAI
from datetime import datetime

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["personal_website"]

class DiaryFormatter:
    # This class is responsible for converting the private diaries to the format that the public can access
    # basically, filter the confidential information, and also make the diaries more readable

    # Structure of the diaries:
    # diaries = [
    #     {
    #         "diary_name": "2024-10-25-00-00-00",
    #         "content": "...",
    #         "comment": "...",
    #         "vector": np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
    #         "processed": False,
    #         "reformatted": ["...", "..."],
    #     },
    #     ...
    # ]

    def __init__(self):
        self.static_diary_dir = "/home/ken/Documents/Personal-Diaries"  # we should not modify anything in this directory
        self.diary_dir = "/home/ken/Documents/personal_website/backend/personal_diaries"  # we can modify this
        self.data_dir = "/home/ken/Documents/personal_website/backend/data"  # we can modify this
        self.collection = db["diaries"]
        
        # load all diaries from the static directory
        all_folders = []
        # filter out the folders that are not eligible
        for folder in os.listdir(self.static_diary_dir):
            # if the folder is not in the format of "yyyy-mm-dd-hh-mm-ss", we skip it
            try:
                datetime.strptime(folder, "%Y-%m-%d-%H-%M-%S")
            except ValueError:
                continue
            # also if the folder does not contain the necessary files, we skip it
            if not os.path.exists(f"{self.static_diary_dir}/{folder}/diary.txt") or \
                not os.path.exists(f"{self.static_diary_dir}/{folder}/comment.txt") or \
                not os.path.exists(f"{self.static_diary_dir}/{folder}/vec.npy"):
                continue
            all_folders.append(folder)
        all_folders.sort(key=lambda x: datetime.strptime(x, "%Y-%m-%d-%H-%M-%S"))
        
        # load the diaries
        self.diaries = []
        for folder in all_folders:
            diary_name = folder
            with open(f"{self.static_diary_dir}/{folder}/diary.txt", "r", encoding="utf-8") as f:
                content = f.read()
            with open(f"{self.static_diary_dir}/{folder}/comment.txt", "r", encoding="utf-8") as f:
                comment = f.read()
            vector = np.load(f"{self.static_diary_dir}/{folder}/vec.npy")
            self.diaries.append(
                {
                    "diary_name": diary_name,
                    "content": content,
                    "comment": comment,
                    "vector": vector,
                    "processed": False,
                    "reformatted": []
                }
            )
        # update the diaries in the dynamic directory
        for diary in self.diaries:
            if not os.path.exists(f"{self.diary_dir}/{diary['diary_name']}"):
                os.mkdir(f"{self.diary_dir}/{diary['diary_name']}")
            with open(f"{self.diary_dir}/{diary['diary_name']}/diary.txt", "w", encoding="utf-8") as f:
                f.write(diary["content"])
            with open(f"{self.diary_dir}/{diary['diary_name']}/comment.txt", "w", encoding="utf-8") as f:
                f.write(diary["comment"])
            np.save(f"{self.diary_dir}/{diary['diary_name']}/vec.npy", diary["vector"])
            # we check if processed by check if the "processed" file is in the directory
            diary["processed"] = os.path.exists(f"{self.diary_dir}/{diary['diary_name']}/processed")
    
    def format_diaries(self):
        # format the diaries
        # after calling this function, we ensure that the `diary["reformatted"]` is a list of reformatted diaries
        system_prompt = "你的名字是\"程永康/Ken\"。你的任务是通过阅读自己的一篇日记及其对应的评价，并将日记中有用的内容变得更加readable。\n\
                        你记录的内容将作为公开的数据集被世界上任何一个人看见。因此，请你根据如下规则做出决策：\n\
                        *规则*\n\
                        1. 如果有*负面情绪*的日记，例如看某个人不顺眼，可以尽量不带感情地描述；\n\
                        2. 如果*特别负面*，例如讨厌某个人，就不记录；\n\
                        3. 如果日记内容体现了对某人的*爱慕之情*，就不记录；\n\
                        4. 如果日记中是有关*个人隐私*的，不记录；\n\
                        5. *如果以上规则都不适用*，记录时尽量保留全部信息，并且保留作者的情感。\n\
                        6. 如果日记里记录了多于一件事，同时记录下来。"
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "make_decision",
                    "description": "Make a decision based on the diary content and comment.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "decision": {
                                "type": "string",
                                "enum": ["record", "not record"],
                                "description": "The decision should be either 'record', or 'not record'."
                            },
                            "content": {
                                "type": "string",
                                "description": "If you do not record the diary, write down the reason here; otherwise, directly write down the reformatted content of the diary."
                            }
                        },
                        "required": ["decision", "content"]
                    }
                }
            },
        ]
        
        for diary in self.diaries:
            if diary["processed"]:
                diary["reformatted"] = json.load(open(f"{self.diary_dir}/{diary['diary_name']}/reformatted.json", "r", encoding="utf-8"))
                continue
            # format the diary
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": diary["content"] + "\n\n" + diary["comment"]},
                ],
                tools=tools,
                tool_choice="required"
            )
            tool_calls = response.choices[0].message.tool_calls
            # one by one (it should be monitored by the user)
            for tool_call in tool_calls:
                kwargs = json.loads(tool_call.function.arguments)
                decision = kwargs["decision"]
                content = kwargs["content"]
                print("-" * 100)
                print("\033[32mDiary Name:\033[0m")
                print(diary["diary_name"])
                print("\033[32mContent:\033[0m")
                print(diary["content"])
                print("\033[32mComment:\033[0m")
                print(diary["comment"])
                print("\033[32mDecision:\033[0m")
                print(decision)
                print("\033[32mContent:\033[0m")
                print(content)
                # input("\033[32mPress Enter to continue...\033[0m")  # uncomment this line if you want to monitor the process
                if decision == "record":
                    diary["reformatted"].append(content)
            # save the reformatted diaries in json format
            with open(f"{self.diary_dir}/{diary['diary_name']}/reformatted.json", "w", encoding="utf-8") as f:
                json.dump(diary["reformatted"], f, ensure_ascii=False, indent=4)
            # mark the diary as processed
            diary["processed"] = True
            with open(f"{self.diary_dir}/{diary['diary_name']}/processed", "w"):
                pass
        print("All diaries have been processed.")
    
    def embed_diaries(self):
        # embed the reformatted diaries
        def get_embedding(text):
            text = text.replace("\n", " ")
            response = openai_client.embeddings.create(
                input=[text],
                model="text-embedding-3-large"
            )
            return response.data[0].embedding
        for diary in self.diaries:
            # we check if the diary is embedded by check if the "embedded" file is in the directory
            if os.path.exists(f"{self.diary_dir}/{diary['diary_name']}/embedded"):
                continue
            print(f"Embedding diary: {diary['diary_name']}")
            # embed the diary
            embeddings = []
            for reformatted in diary["reformatted"]:
                embeddings.append(get_embedding(reformatted))
            # save the embeddings in json format
            json.dump(embeddings, open(f"{self.diary_dir}/{diary['diary_name']}/embeddings.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
            # mark the diary as embedded
            with open(f"{self.diary_dir}/{diary['diary_name']}/embedded", "w"):
                pass
            # input("\033[32mPress Enter to continue...\033[0m")  # uncomment this line if you want to monitor the process
        print("All diaries have been embedded.")
    
    def get_titles(self):
        # get the titles of the diaries
        def get_title(text):
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "你的名字是\"程永康/Ken\"。你的任务是通过阅读自己的一篇日记，为这篇日记写一个标题。\n\
                                                    请根据日记的内容，写一个简洁的标题，让读者一眼就能明白这篇日记的主题。\n\
                                                    直接说标题，不要写其他内容或者标点符号。"},
                    {"role": "user", "content": text},
                ]
            )
            return response.choices[0].message.content
        for diary in self.diaries:
            titles = []
            if not os.path.exists(f"{self.diary_dir}/{diary['diary_name']}/reformatted.json"):
                continue
            if os.path.exists(f"{self.diary_dir}/{diary['diary_name']}/titled"):
                continue
            with open(f"{self.diary_dir}/{diary['diary_name']}/reformatted.json", "r", encoding="utf-8") as f:
                reformatted = json.load(f)
            for i in range(len(reformatted)):
                titles.append(get_title(reformatted[i]))
            # save the titles in json format
            with open(f"{self.diary_dir}/{diary['diary_name']}/titles.json", "w", encoding="utf-8") as f:
                json.dump(titles, f, ensure_ascii=False, indent=4)
            # mark the diary as titled
            with open(f"{self.diary_dir}/{diary['diary_name']}/titled", "w"):
                pass
            # input("\033[32mPress Enter to continue...\033[0m")  # uncomment this line if you want to monitor the process
        print("All titles have been added.")
    
    def extract_processed_diaries(self):
        # before calling this function, we should ensure that all diaries have been reformatted and embedded
        # extract the processed diaries and save them into the file `backend/data/diaries.json`
        def check_eligibility(diary):
            if not os.path.exists(f"{self.diary_dir}/{diary['diary_name']}/embeddings.json") or \
                not os.path.exists(f"{self.diary_dir}/{diary['diary_name']}/reformatted.json"):
                return False
            embeddings = json.load(open(f"{self.diary_dir}/{diary['diary_name']}/embeddings.json", "r", encoding="utf-8"))
            reformatted = json.load(open(f"{self.diary_dir}/{diary['diary_name']}/reformatted.json", "r", encoding="utf-8"))
            if len(embeddings) != len(reformatted):
                print(f"Diary {diary['diary_name']} is not eligible. (this should not happen)")
                return False
            if len(embeddings) == 0:
                return False
            return True
        # extract the processed diaries
        diaries = []
        for diary in self.diaries:
            if not check_eligibility(diary):
                continue
            with open(f"{self.diary_dir}/{diary['diary_name']}/reformatted.json", "r", encoding="utf-8") as f:
                reformatted = json.load(f)
            with open(f"{self.diary_dir}/{diary['diary_name']}/embeddings.json", "r", encoding="utf-8") as f:
                embeddings = json.load(f)
            with open(f"{self.diary_dir}/{diary['diary_name']}/titles.json", "r", encoding="utf-8") as f:
                titles = json.load(f)
            for i in range(len(reformatted)):
                diaries.append(
                    {
                        "diary_name": diary["diary_name"],
                        "content": reformatted[i],
                        "vector": embeddings[i],
                        "title": titles[i]
                    }
                )
        with open(f"{self.data_dir}/diaries.json", "w", encoding="utf-8") as f:
            json.dump(diaries, f, ensure_ascii=False, indent=4)
        print("All reformatted diaries have been extracted.")

    def filter_people_names(self):
        # filter the people names in the diaries for privacy protection
        # we assume that the `data/diaries.json` file has been updated
        # we also assume that there is a file `data/people_names.json` that contains the people names
        people_names = json.load(open(f"{self.data_dir}/people_names.json", "r", encoding="utf-8"))
        diaries = json.load(open(f"{self.data_dir}/diaries.json", "r", encoding="utf-8"))
        for diary in diaries:
            for name in people_names:
                diary["content"] = diary["content"].replace(name, "`somebody`")
                diary["title"] = diary["title"].replace(name, "`somebody`")
        # save the diaries in json format
        with open(f"{self.data_dir}/diaries.json", "w", encoding="utf-8") as f:
            json.dump(diaries, f, ensure_ascii=False, indent=4)
        print("All people names have been filtered.")

    def update_database_for_diaries(self):
        # we assume that the `data/diaries.json` file has been updated
        # update the database for the diaries
        diaries = json.load(open(f"{self.data_dir}/diaries.json", "r", encoding="utf-8"))
        for diary in diaries:
            result = self.collection.find_one({"diary_name": diary["diary_name"]})
            if result:
                # update
                self.collection.update_one({"_id": result["_id"]}, {"$set": diary})
            else:
                # insert
                self.collection.insert_one(diary)
        print("The database has been updated for the diaries.")


if __name__ == "__main__":
    formatter = DiaryFormatter()
    formatter.format_diaries()
    formatter.embed_diaries()
    formatter.get_titles()
    formatter.extract_processed_diaries()
    formatter.filter_people_names()
    formatter.update_database_for_diaries()