"""
    Dash app
"""

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

import constants as c


# Create dash app with styles
app = Dash('auth')
app.config.supress_callback_exceptions = True

app.title = c.names.TITLE

app.layout = html.Div([
    # Header
    html.Div(
        [
            html.Div(
                [
                    html.A(
                        x[1:], href="/", id="section_{}".format(x[1:]),
                        className="w3-bar-item w3-button w3-padding-large w3-hover-white"
                    ) for x in c.dash.LINKS_ALL
                ]
            ),
            html.Div(
                html.Button(
                    'Sync', id='sync',
                    className="w3-bar-item w3-button w3-padding-large w3-hover-white"
                ),
                className="w3-right"
            )
        ],
        className="w3-top w3-bar w3-left-align w3-green w3-text-white"
    ),

    # Sidebar
    html.Div(id="sidebar", className="w3-sidebar w3-light-grey"),

    # Body
    html.Div(html.H1("Test"), id="body", className="w3-display-container"),

    # Others
    html.Div(id="sync_count", style=c.styles.HIDDEN),
    dcc.Location(id='url', refresh=False),
])


if __name__ == '__main__':
    app.run_server(debug=True)
