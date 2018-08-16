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
                    html.Button('Sync', id='sync', style=c.styles.SYNC_BUTTON), 1
                ),
            ],
            style=c.styles.HEADER
        ),

        # Sidebar
        html.Div(id="sidebar", style=c.styles.SIDEBAR),

        # Sub-header
        html.Div([html.H2("Filters")], style=c.styles.FILTER_DIV),

        # Body
        html.Div(id="body", style=c.styles.BODY),

        # Others
        html.Div(id="sync_count", style=c.styles.HIDDEN),
        dcc.Location(id='url', refresh=False),
    ])
