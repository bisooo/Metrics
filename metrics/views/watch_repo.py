from django.shortcuts import render, redirect
# GIT API LIBRARY SERVICES
from git.services.git import GitWrapper as git
# USER SERVICES
from git.services.user import get_user_by_username
# REPOSITORY SERVICES
from git.services.repo import repo_watched, add_repo, watchlist_add
# UTILITY SERVICES
from git.services.utlis import validate_url
# CELERY TASKS
from git.tasks import lastyear_pr_waits


def watch_repo(request):

    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    if request.POST:
        url = request.POST["repo_url"]
        try:
            owner, name = validate_url(url)
            token = request.user.token
            valid_token = git(token).validate_login()
            if valid_token:
                repo = git(token).get_repo_by_name(owner, name)
                if repo:
                    already_watched = repo_watched(request.user, owner, name)
                    if not already_watched:
                        repo = add_repo(owner, name, repo.html_url)
                        user = get_user_by_username(request.user.username)
                        watchlist_add(user, repo)
                        lastyear_pr_waits.delay(token, owner, name)
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
            return render(request, 'watch_repo.html', context)

    return render(request, 'watch_repo.html', context)
