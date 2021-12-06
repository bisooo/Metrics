import django.db

from git.models import Repository, WatchList, PullRequestWait, PullRequest
from django.db import connection
from django.db.utils import OperationalError


# REPOSITORY
def get_repo_by_id(id):
    return Repository.objects.all().get(id=id)


def get_repo_by_name(owner, name):
    with connection.cursor():
        try:
            return Repository.objects.all().get(owner__iexact=owner, name__iexact=name)
        except OperationalError:
            print("DB OPERATIONAL ERROR")


def add_repo(owner, name, url):
    try:
        obj = Repository.objects.all().get(owner__iexact=owner, name__iexact=name)
        return obj
    except Repository.DoesNotExist:
        obj = Repository(owner=owner, name=name, url=url)
        obj.save()
        return obj


# WATCHLIST
def get_repos_watched():
    return WatchList.objects.all().values('repo__owner', 'repo__name').distinct()


def get_users_watchlist(user):
    return WatchList.objects.all().filter(user_id=user.id).only('repo')


def watchlist_remove(user, repo):
    try:
        obj = WatchList.objects.all().get(user_id=user.id, repo_id=repo.id)
        obj.delete()
    except WatchList.DoesNotExist:
        print("WATCHLIST OBJECT DOES NOT EXIST")


def watchlist_add(user, repo):
    obj = WatchList(user_id=user.id, repo_id=repo.id)
    obj.save()


def repo_watched(user, owner, name):
    result = WatchList.objects.all().filter(user_id=user, repo__owner__iexact=owner, repo__name__iexact=name)
    if result:
        return True
    else:
        return False


def watched_user_repos(user, repos):
    objs = []
    watched = []
    for repo in repos:
        if WatchList.objects.all().filter(user_id=user.id, repo__owner__iexact=repo.owner,
                                          repo__name__iexact=repo.name):
            objs.append(repo)
            watched.append(True)
        else:
            objs.append(repo)
            watched.append(False)
    return zip(objs, watched)


# PULL REQUEST WAIT
def get_lastweek_prs(owner, name):
    with connection.cursor():
        try:
            prs = PullRequestWait.objects.all().filter(repo__owner=owner, repo__name=name)
            return prs
        except OperationalError:
            print("DB OPERATIONAL ERROR")


def pr_add(repo, number, created_at, merged_at, updated_at, closed_at, merged):
    with connection.cursor():
        try:
            obj = PullRequestWait.objects.get_or_create(repo_id=repo, number=number, created_at=created_at,
                                                        merged_at=merged_at, updated_at=updated_at,
                                                        closed_at=closed_at, merged=merged)
            return obj
        except OperationalError:
            print("DB OPERATIONAL ERROR")


def pull_request_add(repo, number, created_at, add, delete, commits, merged):
    with connection.cursor():
        try:
            obj = PullRequest.objects.get_or_create(repo_id=repo, number=number, created_at=created_at,
                                                    additions=add, deletions=delete, commits=commits,
                                                    merged=merged)
            return obj
        except OperationalError:
            print("DB OPERATIONAL ERROR")
