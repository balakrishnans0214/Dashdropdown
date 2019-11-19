import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
import os
import pandas as pd
import plotly.graph_objs as go


server = Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'secret')
app = dash.Dash(name = __name__, server = server)
app.config.supress_callback_exceptions = True

df = pd.read_csv('https://raw.githubusercontent.com/balakrishnans0214/Dashdropdown/master/All.csv')

names = df.columns[1:-1]
available_indicators = df['Sector'].unique()


app.layout = html.Div(
    [
        html.Div([
            dcc.Dropdown(
                id='drop',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Energy',
                style={'width': '50%'}
            ),
            dcc.Dropdown(
                id='ddl_x',
                options=[{'label': i, 'value': i} for i in names],
                value='Price',
                style={'width': '50%'}
            ),
            dcc.Dropdown(
                id='ddl_y',
                options=[{'label': i, 'value': i} for i in names],
                value='Market Cap',
                style={'width': '50%'}
            ),
        ], style={'width': '100%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph1')
        ], style={'width': '100%', 'display': 'inline-block'})
    ]
)

@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [
        Input(component_id='drop', component_property='value'),
        Input(component_id='ddl_x', component_property='value'),
        Input(component_id='ddl_y', component_property='value')
    ]
)
def update_output(drop, ddl_x_value, ddl_y_value):
    dff = df[df.Sector.str.contains(drop)]

    figure = {
        'data': [
            go.Scatter(
                x=dff[ddl_x_value],
                y=dff[ddl_y_value],
            )
        ],
        'layout': {
           'title': 'Dash Data Visualization'
        }

    }
    return figure

