from django.shortcuts import render

# PLOTLY
from plotly.offline import plot
import plotly.graph_objects as go


def icons(requests):
    return render(requests, 'icons.html')


def notifications(requests):
    return render(requests, 'notifications.html')


def profile(requests):
    return render(requests, 'profile.html')


def tables(requests):
    return render(requests, 'tables.html')


def typography(requests):
    return render(requests, 'typography.html')


def login(requests):
    return render(requests, 'login.html')


def homepage(requests):
    return render(requests, 'homepage.html')


def dashboard(requests):
    def scatter():
        x1 = [1, 2, 3, 4, 5]
        y1 = [30, 45, 20, 55]
        trace = go.Scatter(x=x1, y=y1)
        layout = dict(title='PLOTLY Scatter Graph', paper_bgcolor='rgba(0,0,0,0.05)',
                      plot_bgcolor='rgba(128,128,128,0.1)')
        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div')
        return plot_div

    context = {'scatterplot': scatter()}
    return render(requests, 'dash.html', context)
