from django.shortcuts import render, redirect
# PLOTLY
from plotly.offline import plot
import plotly.graph_objects as go
# GITHUB LIBRARY
from github3 import login


def icons(request):
    return render(request, 'icons.html')


def notifications(request):
    return render(request, 'notifications.html')


def profile(request):
    return render(request, 'profile.html')


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
            repos = []
            for repo in git.repositories():
                repos.append(repo)
            context['repos'] = repos
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
