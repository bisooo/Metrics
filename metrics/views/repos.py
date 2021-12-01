from django.shortcuts import render, redirect
# GITHUB API LIBRARY SERVICES
from git.services.git import GitWrapper as git
# REPOSITORY SERVICES
from git.services.repo import *


def my_repos(request):

    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    token = request.user.token
    valid_token = git(token).validate_login()
    if valid_token:
        repos = git(token).get_user_repos()
        watched_repos = watched_user_repos(request.user.username, repos)
        context['repos'] = watched_repos
        context['valid_token'] = True
    else:
        context['valid_token'] = False

    return render(request, 'myrepos.html', context)


def repo_add(request, owner, name):

    git_url = "https://github.com" + "/" + owner + "/" + name
    add_repo(request.user.id, owner, name, git_url)
    return my_repos(request)
