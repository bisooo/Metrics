from django.shortcuts import render

# PLOTLY
from plotly.offline import plot
import plotly.graph_objects as go

def homepage(requests):

    def scatter():
        x1 = [1,2,3,4,5]
        y1 = [30,45,20,55]
        trace = go.Scatter(x=x1, y=y1)
        layout = dict(title='PLOTLY Scatter Graph')
        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    context = { 'scatterplot' : scatter() }

    return render(requests, 'homepage.html', context)
