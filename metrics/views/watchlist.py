from django.shortcuts import render, redirect
# GIT API LIBRARY SERVICES
from git.services.git import GitWrapper as git
# REPOSITORY SERVICES
from git.services.repo import *
# UTILITY SERVICES
from git.services.utlis import *


def watchlist(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('login')

    repos = get_users_repos(request.user.username)
    if repos:
        context['repos'] = repos
    else:
        context['no_repos'] = True
    if request.POST:
        url = request.POST["repo_url"]
        try:
            owner, name = validate_url(url)
            token = request.user.token
            valid_token = git(token).validate_login()
            if valid_token:
                repo = git(token).get_repo_by_name(owner, name)
                print(repo)
                if repo:
                    already_watched = repo_watched(request.user.id, owner, name)
                    url = repo.html_url
                    if not already_watched:
                        watch_repo(request.user.id, owner, name, url)
                        context['already_exists'] = False
                    else:
                        context['already_exists'] = True
                    context['url_submitted'] = True
                    context['invalid_url'] = False
                else:
                    context['url_submitted'] = True
                    context['git_error'] = True
            else:
                return redirect('profile')
        except TypeError:
            context['url_submitted'] = True
            context['invalid_url'] = True
            return render(request, 'watchlist.html', context)

    return render(request, 'watchlist.html', context)
