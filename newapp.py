import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

app = dash.Dash(__name__)
server = app.server

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
        'layout':
            go.Layout(
                height=350,
                hovermode='closest',
                title=go.layout.Title(text='Dash Interactive Data Visualization', xref='paper', x=0)
            )

    }
    return figure


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
