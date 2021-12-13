from django.shortcuts import render, redirect
# GITHUB API LIBRARY SERVICES
from git.services.git import GitWrapper as git
# REPOSITORY SERVICES
from git.services.repo import get_users_watchlist


def lifeline(request):

    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    token = request.user.token
    valid_token = git(token).validate_login()
    if valid_token:
        context['valid_token'] = True

    watchlist = get_users_watchlist(request.user)
    if watchlist:
        context['watchlist'] = watchlist
    else:
        context['no_repos'] = True

    if request.method == "POST":
        context['selected_id'] = int(request.POST['repo_id'])
        del request.session['django_plotly_dash']
        session = request.session
        repo = session.get('django_plotly_dash', {})
        repo['repo_id'] = int(request.POST['repo_id'])
        session['django_plotly_dash'] = repo

    return render(request, 'lifeline.html', context)
