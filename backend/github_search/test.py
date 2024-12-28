#!/usr/bin/env python3
# filename: test.py

import os
import json
import base64
import requests

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}


# =====================测试=====================
def send_github_request(method, endpoint, params=None):
    url = f"{GITHUB_API_URL}{endpoint}"
    params = params or {}
    if "per_page" not in params:
        params["per_page"] = 30
    if "page" not in params:
        params["page"] = 1
    response = requests.request(method, url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return {
            "status": "success",
            "data": response.json()
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "error": response.text
        }


def request_github_search(query):
    return send_github_request("GET", "/search/code", params={"q": query})


def search_specific_word(word):
    response = send_github_request("GET", "/search/code", params={"q": f"{word} user:Ken-2511"})
    if response["status"] == "success":
        return response["data"]
    else:
        return response


def get_repo(repo_name):
    response = send_github_request("GET", f"/repos/Ken-2511/{repo_name}")
    if response["status"] == "success":
        return response["data"]
    else:
        return response

# =====================准备=====================
def get_repo_stats(repo_name):
    # 获取指定仓库的信息
    response = send_github_request("GET", f"/repos/Ken-2511/{repo_name}")
    if response["status"] == "success":
        response = response["data"]
        response = {
            "name": response["name"],
            "full_name": response["full_name"],
            "description": response["description"],
            "html_url": response["html_url"],
            "created_at": response["created_at"],
            "updated_at": response["updated_at"],
            "language": response["language"],
            "size": response["size"],
            "default_branch": response["default_branch"],
        }
        return response
    else:
        return response


def list_repo_files(repo_name, per_page=30, page=1):
    # 获取指定仓库的文件
    response = send_github_request("GET", f"/repos/Ken-2511/{repo_name}/contents", params={"per_page": per_page, "page": page})
    if response["status"] == "success":
        response = response["data"]
        files = []
        for file in response:
            files.append({
                "name": file["name"],
                "path": file["path"],
                "download_url": file["download_url"],
                "type": file["type"],
                "size": file["size"],
            })
        return files
    else:
        return response


def get_file_content(repo_name, file_path):
    # 获取指定仓库的文件内容
    response = send_github_request("GET", f"/repos/Ken-2511/{repo_name}/contents/{file_path}")
    if response["status"] == "success":
        response = response["data"]
        if isinstance(response, dict) and "content" in response:  # 是文件
            try:
                content = base64.b64decode(response["content"]).decode("utf-8")
            except UnicodeDecodeError:
                content = response["content"]
            return {
                "name": response["name"],
                "path": response["path"],
                "content": content[:500],
                "html_url": response["html_url"],
                "type": response["type"],
                "size": response["size"],
            }
        else:  # 不是文件
            return {
                "status": "error",
                "error": "Not a file"
            }
    else:
        return response


def list_repositories():
    # 获取用户的所有仓库
    response = send_github_request("GET", "/user/repos")
    if response["status"] == "success":
        response = response["data"]
        repos = []
        for repo in response:
            repos.append({
                "name": repo["name"],
                "full_name": repo["full_name"],
                "description": repo["description"],
                "html_url": repo["html_url"],
                "created_at": repo["created_at"],
                "updated_at": repo["updated_at"],
                "language": repo["language"],
                "size": repo["size"],
                "default_branch": repo["default_branch"],
            })
        return repos
    else:
        return response


def search_specific_word_1(word):
    params = {
        "q": f"{word} user:Ken-2511",
        "per_page": 30,
        "page": 1
    }
    response = send_github_request("GET", "/search/code", params=params)
    if response["status"] == "success":
        response = response["data"]
        items = []
        for item in response["items"]:
            items.append({
                "name": item["name"],
                "path": item["path"],
                "html_url": item["html_url"],
                "repository": item["repository"]["full_name"],
            })
        return items
    else:
        return response


if __name__ == "__main__":
    # response = get_file_content("personal_website", "backend")
    # response = list_repo_files("personal_website")
    # response = get_repo_stats("personal_website")
    # response = list_repositories()
    response = search_specific_word_1("import")
    print(json.dumps(response, indent=4))