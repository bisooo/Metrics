from django.shortcuts import render, redirect
# GITHUB API LIBRARY SERVICES
from git.services.git import GitWrapper as git


def lifeline(request):

    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    token = request.user.token
    valid_token = git(token).validate_login()
    if valid_token:
        context['valid_token'] = True

    return render(request, 'lifeline.html', context)
