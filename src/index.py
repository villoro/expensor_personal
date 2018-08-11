"""
    Dash app
"""

import os

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = [
    [os.environ["EXPENSOR_USER"], os.environ["EXPENSOR_PASSWORD"]]
]

APP = dash.Dash('auth')
SERVER = APP.server

auth = dash_auth.BasicAuth(
    APP,
    VALID_USERNAME_PASSWORD_PAIRS
)

APP.layout = html.Div([
    html.H1('Welcome to the APP'),
    html.H3('You are successfully authorized'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['A', 'B']],
        value='A'
    ),
    dcc.Graph(id='graph')
], className='container')

@APP.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_graph(dropdown_value):
    return {
        'layout': {
            'title': 'Graph of {}'.format(dropdown_value),
            'margin': {
                'l': 20,
                'b': 20,
                'r': 10,
                't': 60
            }
        },
        'data': [{'x': [1, 2, 3], 'y': [4, 1, 2]}]
    }

APP.scripts.config.serve_locally = True
APP.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})



if __name__ == '__main__':
    APP.run_server(debug=True)
