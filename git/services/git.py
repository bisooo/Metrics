# GITHUB API LIBRARY
from github3 import login
from github3.exceptions import *
# PYTHON LIBRARY
import datetime
import pytz


class GitWrapper:

    def __init__(self, token):
        self.git = login(token=token)

    def validate_login(self):
        if self.git:
            try:
                self.git.me()
                return True
            except (GitHubError, GitHubException) as e:
                print("GITHUB ERROR")
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
            print("GITHUB ERROR")
            if e.message:
                print(e.message)
                return None

    def get_lastweek_prs(self, owner, name):
        try:
            repo = self.git.repository(owner, name)
            prs = []
            utc = pytz.UTC
            lastweek_date = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(tzinfo=utc)
            for pr in repo.pull_requests():
                creation_date = pr.created_at.replace(tzinfo=utc)
                if creation_date > lastweek_date:
                    prs.append(pr)
                else:
                    break
            return prs
        except (GitHubError, GitHubException) as e:
            print("GITHUB ERROR")
            if e.message:
                print(e.message)

    def get_lastmonth_prs(self, owner, name):
        try:
            repo = self.git.repository(owner, name)
            prs = []
            utc = pytz.UTC
            lastmonth_date = (datetime.datetime.now() - datetime.timedelta(days=30)).replace(tzinfo=utc)
            for pr in repo.pull_requests():
                creation_date = pr.created_at.replace(tzinfo=utc)
                if creation_date > lastmonth_date:
                    prs.append(pr)
                else:
                    break
            return prs
        except (GitHubError, GitHubException) as e:
            print("GITHUB ERROR")
            if e.message:
                print(e.message)

    def get_lastyear_prs(self, owner, name):
        try:
            repo = self.git.repository(owner, name)
            prs = []
            utc = pytz.UTC
            lastyear_date = (datetime.datetime.now() - datetime.timedelta(days=365)).replace(tzinfo=utc)
            for pr in repo.pull_requests():
                creation_date = pr.created_at.replace(tzinfo=utc)
                if creation_date > lastyear_date:
                    prs.append(pr)
                else:
                    break
            return prs
        except (GitHubError, GitHubException) as e:
            print("GITHUB ERROR")
            if e.message:
                print(e.message)
