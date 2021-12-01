from django.shortcuts import render, redirect
# USER SERVICES LAYER
from git.services.user import *
# GIT API LIBRARY SERVICES
from git.services.git import GitWrapper as git


def profile(request):

    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    if request.POST:
        token = request.POST["token"]
        valid_token = git(token).validate_login()
        if valid_token:
            context['invalid_token'] = False
            user = get_user_by_username(request.user.username)
            update_token(user, token)
        else:
            context['invalid_token'] = True

    return render(request, 'profile.html', context)
