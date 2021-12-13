# PLOTLY DASH
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
# PANDAS
import pandas as pd
# REPO SERVICES
from git.services.repo import get_users_watchlist
# PR SERVICES
from git.services.prs import *


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('pr', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H5('WEEKLY PR STATS', style={'text-align': 'center', 'color': 'white'}),
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    html.Div(id='none', children=[], style={'display': 'none'}),
])


@app.callback(
    Output('slider-graph', 'figure'),
    [Input('none', 'children')])
def display_value(*args, **kwargs):
    session = kwargs['session_state']
    print("PASSED SESSION STATE = " + str(session))

    x = [0, 1, 2, 3, 4, 5, 6 , 7, 8, 9, 10, 11, 12]
    y = [10, 20, 5, 40, 50, 60, 40, 30, 60, 100, 55, 80, 95]
    graph = go.Scatter(x=x, y=y)
    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(range=[min(y), max(y)]),
        font=dict(color='white'),
    )
    return {'data': [graph], 'layout': layout}
