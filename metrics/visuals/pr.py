# PLOTLY DASH
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from django_plotly_dash import DjangoDash
# PANDAS
import pandas as pd
# REPO SERVICES
from git.services.repo import get_repo_by_id
# PR SERVICES
from git.services.prs import get_last_week_prs


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('pr', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H5('WEEKLY PR LIFELINE', style={'text-align': 'center', 'color': 'white'}),
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    html.Div(id='none', children=[], style={'display': 'none'}),
])


@app.callback(
    Output('slider-graph', 'figure'),
    [Input('none', 'children')])
def display_value(*args, **kwargs):
    session = kwargs['session_state']
    repo = get_repo_by_id(session['repo_id'])
    prs = get_last_week_prs(repo.owner, repo.name)

    df = pd.DataFrame(prs)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df.sort_values(by='created_at')
    # MOVING AVERAGE
    window = 5
    df['+'] = df['additions'].rolling(window=window, min_periods=1).mean()
    df['-'] = df['deletions'].rolling(window=window, min_periods=1).mean()

    fig = px.line(df, x=df['created_at'], y=[df['+'], df['-']])
    fig.update_layout(
        template='plotly_dark',
        xaxis_title="DAY",
        yaxis_title="PR SIZE",
        legend_title="ADDS / DELS",
    )
    return fig
