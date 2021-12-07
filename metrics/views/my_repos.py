from django.shortcuts import render, redirect
# GITHUB API LIBRARY SERVICES
from git.services.git import GitWrapper as git
# USER SERVICES
from git.services.user import get_user_by_username
# REPOSITORY SERVICES
from git.services.repo import watched_user_repos, add_repo, watchlist_add
# CELERY TASKS
from git.tasks import lastyear_pr_waits


def my_repos(request):

    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    token = request.user.token
    valid_token = git(token).validate_login()
    if valid_token:
        repos = git(token).get_user_repos()
        watched_repos = watched_user_repos(request.user, repos)
        context['repos'] = watched_repos
        context['valid_token'] = True
    else:
        context['valid_token'] = False

    return render(request, 'myrepos.html', context)


def repo_add(request, owner, name):

    git_url = "https://github.com" + "/" + owner + "/" + name
    repo = add_repo(owner, name, git_url)
    user = get_user_by_username(request.user.username)
    watchlist_add(user, repo)
    lastyear_pr_waits.delay(request.user.token, owner, name)

    return my_repos(request)
