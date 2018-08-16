"""
    Dash app
"""

import dash_core_components as dcc
import dash_html_components as html

import constants as c
from app import ui_utils as uiu


def get_layout():
    """ Creates the dash layout """

    return html.Div([
        # Header
        uiu.get_row(
            [
                uiu.get_one_column(
                    html.H1(c.names.TITLE, id="title", style={"color": "white"}), 11
                ),
                uiu.get_one_column(
                    html.Button('Sync', id='sync'), 1
                ),
            ],
            style=c.styles.STYLE_HEADER
        ),

        # Sidebar
        html.Div(id="sidebar", style=c.styles.STYLE_SIDEBAR),

        # Sub-header
        html.Div([html.H2("Filters")], style=c.styles.STYLE_FILTER_DIV),

        # Body
        html.Div(id="body", style=c.styles.STYLE_BODY),

        # Others
        html.Div(id="sync_count", style=c.styles.STYLE_HIDDEN),
        dcc.Location(id='url', refresh=False),
    ])
