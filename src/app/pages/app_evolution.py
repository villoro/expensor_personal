"""
    Dash app
"""

import dash_core_components as dcc
import dash_html_components as html

import constants as c
from app import ui_utils as uiu


LINK = c.dash.LINK_EVOLUTION


def get_content(app, dfs):
    """
        Creates the page

        Args:
            app:    dash app
            dfs:    dict with dataframes

        Returns:
            dict with content:
                body:       body of the page
                sidebar:    content of the sidebar
    """

    content = [
        dcc.Graph(id="plot_evol", config=uiu.PLOT_CONFIG),
        [
            dcc.Graph(id="plot_evo_detail", config=uiu.PLOT_CONFIG),
            dcc.RadioItems(
                id="radio_evol_type",
                options=uiu.get_options([c.names.EXPENSES, c.names.INCOMES]),
                value=c.names.EXPENSES,
                labelStyle={'display': 'inline-block'}
            )
        ],
    ]

    sidebar = [
        ("Categories", dcc.Dropdown(id="drop_evol_categ", multi=True)),
        ("Group by", dcc.RadioItems(
            id="radio_evol_tw", value="M",
            options=[{"label": "Day", "value": "D"},
                     {"label": "Month", "value": "M"},
                     {"label": "Year", "value": "Y"}]
            )
        ),
    ]

    return {c.dash.KEY_BODY: content, c.dash.KEY_SIDEBAR: sidebar}
