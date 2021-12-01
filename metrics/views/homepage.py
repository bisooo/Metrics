from django.shortcuts import render, redirect
# GITHUB LIBRARY
from github3 import login
from github3.exceptions import *


def homepage(request):
    context = {}
    if request.user.is_authenticated:
        token = request.user.token
        git = login(token=token)
        if git:
            try:
                git.me()
                repos = []
                for repo in git.repositories():
                    repos.append(repo)
                context['repos'] = repos
                context['invalid_token'] = False
            except (GitHubError, GitHubException) as e:
                print("ERROR")
                if e.message:
                    print(e.message)
                context['invalid_token'] = True
        else:
            context['invalid_token'] = True
    else:
        return redirect('login')
    return render(request, 'homepage.html', context)
