from git.models import Repository


def watched_user_repos(username, repos):
    objs = []
    watched = []
    for repo in repos:
        if Repository.objects.all().filter(user__username=username,
                                           owner__iexact=repo.owner,
                                           name__iexact=repo.name):
            objs.append(repo)
            watched.append(True)
        else:
            objs.append(repo)
            watched.append(False)
    return zip(objs, watched)


def get_users_repos(username):
    return Repository.objects.all().filter(user__username=username)


def repo_watched(user, owner, name):
    result = Repository.objects.all().filter(user_id=user, owner__iexact=owner, name__iexact=name)
    if result:
        return True
    else:
        return False


def add_repo(user, owner, name, url):
    obj = Repository(user_id=user, owner=owner, name=name, url=url)
    obj.save()


def delete_repo_by_id(id):
    obj = Repository.objects.all().get(id=id)
    obj.delete()
