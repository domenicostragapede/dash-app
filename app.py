# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import psycopg2 as pg
import pandas as pd

attributes = ['acceleration', 'cilinders', 'displacement', 'horsepower', 'model_year', 'weight', 'mpg']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def get_data_frame():
    pg_params = {
      'dbname': 'auto',
      'user': 'candidato',
      'password': 'crossnova20',
      'host': '178.22.68.101',
      'port': 5434
    }
    con = pg.connect(**pg_params)
    return pd.read_sql_query('SELECT * FROM auto;', con=con)


def make_dropdown(id, label, default='acceleration', class_name=''):
    return \
        html.Div(
            children=[
                html.Label(label),
                dcc.Dropdown(
                    id=id,
                    options=[
                        {'label': a.replace('_', ' ').capitalize(), 'value': a}
                        for a in attributes
                    ],
                    value=default,
                ),
            ],
            className=class_name
        )


def make_graph_figure(data=[], title='Auto crossnova'):
    return {
        'data': data,
        'layout': go.Layout(
            title=title
        )
    }


@app.callback(Output('auto-graph', 'figure'), [Input('x-axis', 'value'), Input('y-axis', 'value')])
def update_graph(x_axis_value, y_axix_value):
    df = get_data_frame()
    return {
        'data': [
            go.Scatter(
                x=list(df[x_axis_value].to_dict().values()),
                y=list(df[y_axix_value].to_dict().values()),
                mode='markers'
            )
        ],
        'layout': go.Layout(
            title='%s - %s' % (x_axis_value.capitalize(), y_axix_value.capitalize())
        )
    }

app.layout = html.Div(children=[
    html.H1(children='Crossnova Dash'),
    html.Div(children=[
        html.Div(
            children=[
                make_dropdown('x-axis', "X Axis", default=attributes[0]),
                make_dropdown('y-axis', "Y Axis", default=attributes[1]),
            ],
            className='four columns'),
        html.Div(
            children=[
                dcc.Graph(
                    id='auto-graph',
                    figure={
                        'data': []
                    },
                )
            ],
            className='eight columns'),
    ], className='twelve columns'),
])


if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='0.0.0.0')
