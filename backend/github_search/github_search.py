#!/usr/bin/env python3
# filename: github_search.py

import os
import json
import requests


class GithubSearch:
    def __init__(self):
        self.GITHUB_API_URL = "https://api.github.com"
        self.GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
        self.HEADERS = {"Authorization": f"Bearer {self.GITHUB_TOKEN}"}

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

    def request_github_search(self, query):
        return self.send_github_request("GET", "/search/code", params={"q": query})

    def search_specific_word(self, word):
        response = self.send_github_request("GET", "/search/code", params={"q": f"{word} user:Ken-2511"})
        if response["status"] == "success":
            return response["data"]
        else:
            return response

    def get_repo(self, repo_name):
        response = self.send_github_request("GET", f"/repos/Ken-2511/{repo_name}")
        if response["status"] == "success":
            return response["data"]
        else:
            return response

    def get_repo_stats(self, repo_name):
        # 获取指定仓库的信息
        response = self.send_github_request("GET", f"/repos/Ken-2511/{repo_name}")
        if response["status"] == "success":
            response = response["data"]
        return response


if __name__ == '__main__':
    gs = GithubSearch()
    print(gs.get_repo_stats("github-search"))