from django.shortcuts import render, redirect
# PLOTLY
from plotly.offline import plot
import plotly.graph_objects as go
# GITHUB LIBRARY
from github3 import login
from github3.exceptions import *
# MODELS
from git.models import User, Repository


def icons(request):
    return render(request, 'icons.html')


def notifications(request):
    return render(request, 'notifications.html')


def profile(request):
    context = {}
    if request.user.token == "":
        context['invalid_token'] = True
    if request.POST:
        token = request.POST.get("token", '')
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


def watchlist(request):
    global owner, repo_name
    context = {}
    if request.user.is_authenticated:
        repos = Repository.objects.filter(user__username=request.user.username)
        if repos:
            context['repos'] = repos
        else:
            context['no_repos'] = True
        if request.POST:
            url = request.POST.get("repo_url", '')
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


def typography(request):
    return render(request, 'typography.html')


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


def dashboard(request):
    def scatter():
        x1 = [1, 2, 3, 4, 5]
        y1 = [30, 45, 20, 55]
        trace = go.Scatter(x=x1, y=y1)
        layout = dict(title=dict(text='PLOTLY Scatter Graph', x=0.5,
                                 font=dict(family='Sheriff', size=20, color='white')),
                      paper_bgcolor='rgba(0,0,0,0.05)', plot_bgcolor='rgba(128,128,128,0.1)',
                      font=dict(family='Sheriff', size=10, color='white'))
        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div')
        return plot_div

    context = {'scatter_plot': scatter()}
    return render(request, 'dash.html', context)
