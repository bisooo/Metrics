import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('yearly_pr_wait', external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.H5('YEARLY PR WAIT TIME', style={'text-align': 'center', 'color': 'white'}),
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
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
])


@app.callback(
    Output('slider-graph', 'figure'),
    [Input('select-goal', 'value')])
def display_value(*args, **kwargs):
    goal = kwargs['callback_context'].inputs['select-goal.value']
    print("SELECTED A GOAL OF " + str(goal) + " HOURS")

    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    y = [10, 20, 5, 40, 50, 60, 40, 30, 60, 100, 55, 80, 95]
    graph = go.Scatter(x=x, y=y)
    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[min(x), max(x)], title="DAY"),
        yaxis=dict(range=[min(y), max(y)], title="SUCCESS RATE ﹪"),
        font=dict(color='white'),
    )
    return {'data': [graph], 'layout': layout}
