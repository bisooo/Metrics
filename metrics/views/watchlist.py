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

    watchlist = get_repos_watched(request.user)
    if watchlist:
        context['watchlist'] = watchlist
    else:
        context['no_repos'] = True

    return render(request, 'watchlist.html', context)


def delete_repo(request, repo_id):

    repo = get_repo_by_id(repo_id)
    watchlist_remove(request.user, repo)

    return watchlist(request)
