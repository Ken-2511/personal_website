#!/usr/bin/env python3
# filename: github_search.py

import os
import json
import base64
import requests

json_deco_enable = True


def json_decorator(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if not json_deco_enable:
            return response
        if isinstance(response, dict):
            # Already a dictionary, assume it's JSON-serializable
            return json.dumps(response, indent=4)
        try:
            # Try to serialize to JSON
            return json.dumps(response, indent=4)
        except TypeError:
            # Fallback for non-serializable responses
            return json.dumps({"status": "error", "message": "Non-serializable response"})
    return wrapper


class GithubSearch:
    def __init__(self):
        self.GITHUB_API_URL = "https://api.github.com"
        self.GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
        self.HEADERS = {"Authorization": f"Bearer {self.GITHUB_TOKEN}"}
        self.usr_name = "Ken-2511"

    def send_github_request(self, method, endpoint, params=None):
        url = f"{self.GITHUB_API_URL}{endpoint}"
        params = params or {}
        if "per_page" not in params:
            params["per_page"] = 30
        if "page" not in params:
            params["page"] = 1
        response = requests.request(method, url, headers=self.HEADERS, params=params)
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

    @json_decorator
    def list_repo_files(self, repo_name, per_page=30, page=1):
        # 获取指定仓库的文件列表
        response = self.send_github_request("GET", f"/repos/{self.usr_name}/{repo_name}/contents", params={"per_page": per_page, "page": page})
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

    @json_decorator
    def get_repo_stats(self, repo_name):
        # 获取指定仓库的信息
        response = self.send_github_request("GET", f"/repos/{self.usr_name}/{repo_name}")
        if response["status"] == "success":
            response = response["data"]
            return {
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
        else:
            return response

    @json_decorator
    def get_file_content(self, repo_name, file_path):
        # 获取指定仓库的文件内容
        response = self.send_github_request("GET", f"/repos/{self.usr_name}/{repo_name}/contents/{file_path}")
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

    @json_decorator
    def list_repositories(self):
        # 获取用户的所有仓库
        response = self.send_github_request("GET", "/user/repos")
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


if __name__ == '__main__':
    gs = GithubSearch()
    print(gs.list_repositories())