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
    html.Div(
        className="app-header",
        children=[
            html.Div('Plotly Dash', className="app-header--title")
        ]
    ),
    html.Div(
        children=html.Div([
            html.H5('Overview'),
            html.Div('''
                This is an example of a simple Dash app with
                local, customized CSS.
            ''')
        ])
    )
])



if __name__ == '__main__':
    APP.run_server(debug=True)
