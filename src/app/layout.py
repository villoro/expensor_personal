"""
    Dash app
"""

import dash_core_components as dcc
import dash_html_components as html

import constants as c


def get_layout():
    """ Creates the dash layout """

    return html.Div([
        # Header
        html.Div([
            html.H1("ExpensORpy", id="title", style={"color": "white"})
        ], style=c.styles.STYLE_HEADER),

        # Sidebar
        html.Div(id="sidebar", style=c.styles.STYLE_SIDEBAR),

        # Sub-header
        html.Div([html.H2("Filters")], style=c.styles.STYLE_FILTER_DIV),

        # Body
        html.Div(id="page-content", style=c.styles.STYLE_BODY),

        # Others
        dcc.Location(id='url', refresh=False),
    ])
