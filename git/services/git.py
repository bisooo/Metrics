# GITHUB API LIBRARY
from github3 import login
from github3.exceptions import *


class GitWrapper:

    def __init__(self, token):
        self.git = login(token=token)

    def validate_login(self):
        if self.git:
            try:
                self.git.me()
                return True
            except (GitHubError, GitHubException) as e:
                print("ERROR")
                if e.message:
                    print(e.message)
                return False

    def get_user_repos(self):
        repos = []
        for repo in self.git.repositories():
            repos.append(repo)
        return repos

    def get_repo_by_name(self, owner, name):
        try:
            repo = self.git.repository(owner, name)
            return repo
        except (GitHubError, GitHubException) as e:
            print("ERROR")
            if e.message:
                print(e.message)
                return None
