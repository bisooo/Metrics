from git.models import Repository


def get_users_repos(username):
    return Repository.objects.all().filter(user__username=username)


def repo_watched(user, owner, name):
    result = Repository.objects.all().filter(user_id=user, owner__iexact=owner, name__iexact=name)
    if result:
        return True
    else:
        return False


def watch_repo(user, owner, name, url):
    obj = Repository(user_id=user, owner=owner, name=name, url=url)
    obj.save()
