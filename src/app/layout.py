"""
    Dash app
"""

import dash_core_components as dcc
import dash_html_components as html

import constants as c


HEADER_HEIGHT = "48px"

def get_layout():
    """ Creates the dash layout """

    return html.Div([
        # Header
        html.Div(
            [
                html.Div(
                    [
                        html.A(
                            x[1:], href=x, id="section_{}".format(x[1:]),
                            className="w3-bar-item w3-button w3-padding-large w3-hover-white",
                            style={"font-size": "18px"}
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
            className="w3-top w3-bar w3-left-align w3-green w3-text-white w3-card",
            style={"height": HEADER_HEIGHT}
        ),

        # Filters
        html.Div(
            id="filters", style={"margin-top": HEADER_HEIGHT},
            className="w3-padding-16 w3-light-grey w3-row"
        ),

        # Body
        html.Div(id="body"),

        # Others
        html.Div(id="sync_count", style={"display": "none"}),
        dcc.Location(id='url', refresh=False),
    ])
