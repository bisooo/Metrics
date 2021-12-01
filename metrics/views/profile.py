from django.shortcuts import render, redirect
# GITHUB LIBRARY
from github3 import login
from github3.exceptions import *
# MODELS
from git.models import User


def profile(request):
    context = {}
    if request.user.token == "":
        context['invalid_token'] = True
    if request.POST:
        token = request.POST["token"]
        git = login(token=token)
        if git:
            try:
                git.me()
                context['invalid_token'] = False
                user = User.objects.get(username=request.user.username)
                user.token = token
                user.save()
                return redirect('profile')
            except (GitHubError, GitHubException) as e:
                print("ERROR")
                if e.message:
                    print(e.message)
                context['invalid_token'] = True
    return render(request, 'profile.html', context)
