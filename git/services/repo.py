from git.models import Repository, WatchList


def get_repo_by_id(id):
    return Repository.objects.all().get(id=id)


def add_repo(owner, name, url):
    try:
        obj = Repository.objects.all().get(owner__iexact=owner, name__iexact=name)
        return obj
    except Repository.DoesNotExist:
        obj = Repository(owner=owner, name=name, url=url)
        obj.save()
        return obj


def get_repos_watched(user):
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
        if WatchList.objects.all().filter(user_id=user.id, repo__owner__iexact=repo.owner, repo__name__iexact=repo.name):
            objs.append(repo)
            watched.append(True)
        else:
            objs.append(repo)
            watched.append(False)
    return zip(objs, watched)
