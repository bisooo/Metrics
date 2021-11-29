from django.shortcuts import render, redirect
# PLOTLY
from plotly.offline import plot
import plotly.graph_objects as go
# GITHUB LIBRARY
from github3 import login
from github3.exceptions import *
# MODELS
from git.models import User


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


def tables(request):
    return render(request, 'tables.html')


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
