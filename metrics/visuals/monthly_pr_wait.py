# PLOTLY DASH
import dash
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
from git.services.prs import get_pr_waits_by_month


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('monthly_pr_wait', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H5('MONTHLY PR WAIT TIME', style={'text-align': 'center', 'color': 'white'}),
    html.P('SELECT A GOAL', style={'text-align': 'center', 'color': 'grey'}),
    dcc.Slider(
        id='select-goal',
        marks={
            6: '6 HOURS', 12: '12 HOURS', 18: '18 HOURS',
            24: '24 HOURS', 30: '30 HOURS', 36: '36 HOURS',
            42: '42 HOURS', 48: '48 HOURS', 54: '54 HOURS',
            60: '60 HOURS', 66: '66 HOURS', 72: '72 HOURS'
        },
        min=1,
        max=78,
        value=72,
        step=None,
        updatemode='drag',
    ),
    dcc.Slider(
        id='select-month',
        marks={
            1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR',
            5: 'MAY', 6: 'JUNE', 7: 'JULY', 8: 'AUG',
            9: 'SEPT', 10: 'OCT', 11: 'NOV', 12: 'DEC',
        },
        min=1,
        max=12,
        value=1,
        included=False,
    ),
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
])


@app.callback(
    Output('slider-graph', 'figure'),
    [Input('select-goal', 'value'),
     Input('select-month', 'value')])
def display_value(*args, **kwargs):
    goal = dash.callback_context.inputs['select-goal.value']
    month = dash.callback_context.inputs['select-month.value']
    session = kwargs['session_state']
    repo = get_repo_by_id(session['repo_id'])

    prs = get_pr_waits_by_month(repo.owner, repo.name, month)
    df = pd.DataFrame(prs)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['merged_at'] = pd.to_datetime(df['merged_at'])
    df = df.sort_values(by='created_at')

    def merge_time(row):
        if row['merged']:
            diff = row['merged_at'] - row['created_at']
            days = diff.days
            hours, remainder = divmod(diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time = (days * 24) + hours + (minutes / 60)
        else:
            time = 0
        return time

    df['merge_time'] = df.apply(merge_time, axis=1)
    pr_wait = pd.DataFrame()
    for day in df.created_at.dt.date.unique():
        # TOTAL NO. OF PRs MERGED ON THAT DAY
        created_on_day = pd.to_datetime(df.created_at.dt.date) == str(day)
        total_prs = df[(created_on_day) & (df.merged)].shape[0]
        # TOTAL NO. OF PRs THAT WERE MERGED WITHIN THE GOAL TIME
        success_prs = df[(created_on_day) & (df.merged) & (df.merge_time <= goal)].shape[0]
        if total_prs != 0:
            success_rate = (success_prs / total_prs) * 100
        else:
            success_rate = 0
        pr_wait = pr_wait.append({'day': day, 'success': success_rate}, ignore_index=True)

    # MOVING AVERAGE
    window = 3
    pr_wait['MA'] = pr_wait.success.rolling(window=window, center=True).mean()

    fig = px.line(pr_wait, x="day", y=["success", "MA"])
    fig.update_layout(
        template='plotly_dark',
        xaxis_title="DAY",
        yaxis_title="SUCCESS RATE",
        legend_title="TRUE VS MA",
        xaxis_range=[min(pr_wait['day']), max(pr_wait['day'])],
        yaxis_range=[0, 100]
    )
    return fig
