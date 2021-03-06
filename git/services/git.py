# GITHUB API LIBRARY
from github3 import login
from github3.exceptions import GitHubError, GitHubException
# PYTHON LIBRARY
import datetime
import pytz
# REPOSITORY SERVICES
from .repo import get_repo_by_name
# PR SERVICES
from .prs import pr_add, get_lastweek_pr_waits, pr_wait_add


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

    def get_lastyear_pr_waits(self, owner, name):
        try:
            repo = self.git.repository(owner, name)
            repo_obj = get_repo_by_name(owner, name)
            utc = pytz.UTC
            lastyear_date = (datetime.datetime.now() - datetime.timedelta(days=365)).replace(tzinfo=utc)
            for pr in repo.pull_requests(state='all'):
                creation_date = pr.created_at.replace(tzinfo=utc)
                if creation_date > lastyear_date:
                    if pr.merged_at:
                        merged = True
                    else:
                        merged = False
                    pr_wait_add(repo_obj.id, pr.number, pr.created_at,
                                pr.merged_at, pr.updated_at, pr.closed_at, merged)
                else:
                    break
            return True
        except (GitHubError, GitHubException) as e:
            print("GITHUB ERROR")
            if e.message:
                print(e.message)
            return False

    def get_lastweek_prs(self, owner, name):
        try:
            repo = get_repo_by_name(owner, name)
            prs = get_lastweek_pr_waits(owner, name)
            for pr in prs:
                number = pr.number
                pull_request = self.git.pull_request(owner, name, number)
                created_at = pr.created_at
                pr_add(repo.id, number, created_at, pull_request.additions_count,
                       pull_request.deletions_count, pull_request.commits_count,
                       pull_request.merged)
            return True
        except (GitHubError, GitHubException) as e:
            print("GITHUB ERROR")
            if e.message:
                print(e.message)
            return False
