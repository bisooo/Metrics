from django.shortcuts import render, redirect
# REPOSITORY SERVICES
from git.services.repo import *
# GITHUB API LIBRARY SERVICES
from git.services.git import GitWrapper as git


def watchlist(request):

    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    token = request.user.token
    valid_token = git(token).validate_login()
    if valid_token:
        context['valid_token'] = True

    repos = get_users_repos(request.user.username)
    if repos:
        context['repos'] = repos
    else:
        context['no_repos'] = True

    return render(request, 'watchlist.html', context)


def delete_repo(request, repo_id):

    if not request.user.is_authenticated:
        return redirect('login')

    delete_repo_by_id(repo_id)
    return watchlist(request)
