from django.shortcuts import render, redirect
# GITHUB LIBRARY
from github3 import login
from github3.exceptions import *
# MODELS
from git.models import Repository


def watchlist(request):
    context = {}
    if request.user.is_authenticated:
        repos = Repository.objects.filter(user__username=request.user.username)
        if repos:
            context['repos'] = repos
        else:
            context['no_repos'] = True
        if request.POST:
            url = request.POST["repo_url"]
            if url:
                if url.startswith("https://"):
                    try:
                        owner = url.split('/')[3]
                        repo_name = url.split('/')[4]
                    except IndexError:
                        print("INDEX ERROR")
                        context['url_submitted'] = True
                        context['invalid_url'] = True
                        return render(request, 'watchlist.html', context)
                else:
                    try:
                        owner = url.split('/')[1]
                        repo_name = url.split('/')[2]
                    except IndexError:
                        print("INDEX ERROR")
                        context['url_submitted'] = True
                        context['invalid_url'] = True
                        return render(request, 'watchlist.html', context)
                token = request.user.token
                git = login(token=token)
                if git and owner and repo_name:
                    try:
                        repo = git.repository(owner, repo_name)
                        repo_url = repo.html_url
                        check = Repository.objects.filter(user_id=request.user.id, owner=owner, name=repo_name)
                        if not check:
                            repo_obj = Repository(user_id=request.user.id, owner=owner, name=repo_name, url=repo_url)
                            repo_obj.save()
                            context['already_exists'] = False
                        else:
                            context['already_exists'] = True
                        context['url_submitted'] = True
                        context['invalid_url'] = False
                    except (GitHubError, GitHubException) as e:
                        print("ERROR")
                        if e.message:
                            context['is_error'] = True
                            context['error'] = e.message
            else:
                context['url_submitted'] = True
                context['invalid_url'] = True
        else:
            context['url_submitted'] = False
    else:
        return redirect('login')
    return render(request, 'watchlist.html', context)
