from django.shortcuts import render, redirect
# GITHUB API LIBRARY SERVICES
from git.services.git import GitWrapper as git


def homepage(request):

    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    token = request.user.token
    valid_token = git(token).validate_login()
    if valid_token:
        repos = git(token).get_user_repos()
        context['repos'] = repos
        context['invalid_token'] = False
    else:
        context['invalid_token'] = True

    return render(request, 'homepage.html', context)
