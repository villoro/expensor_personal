"""
    Dash app
"""

import dash_core_components as dcc
import dash_html_components as html

import constants as c
from ui_utils import get_options
from data_loader import DFS

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
                    [
                        html.Div(
                            "Smoothing:",
                            id="title_time_average",
                            className="w3-bar-item w3-padding-large",
                            style=c.dash.SHOW_DICT(False)
                        ),
                        dcc.Input(
                            id='input_time_average',
                            type='number',
                            value=c.dash.DEFAULT_SMOOTHING,
                            min=0, max=12,
                            className="w3-bar-item w3-padding-large w3-green",
                            style=c.dash.SHOW_DICT(False)
                        ),
                        html.Div(
                            "Grouping:",
                            id="title_timewindow",
                            className="w3-bar-item w3-padding-large",
                            style=c.dash.SHOW_DICT(False)
                        ),
                        dcc.RadioItems(
                            id="radio_timewindow", value="M",
                            options=[{"label": "Month ", "value": "M"},
                                     {"label": "Year ", "value": "Y"}],
                            className="w3-bar-item w3-padding-large",
                            style=c.dash.SHOW_DICT(False)
                        ),
                        html.Button(
                            'Sync', id='sync',
                            className="w3-bar-item w3-button w3-padding-large w3-hover-white"
                        ),
                    ],
                    className="w3-right"
                )
            ],
            className="w3-bar w3-left-align w3-green w3-text-white w3-card",
            style={"z-index": 10000}
        ),

        # Filters
        html.Div(
            [
                html.Div(
                    html.H5("Categories"),
                    className="w3-col l1 m2 s4 w3-padding"
                ),
                html.Div(
                    dcc.Dropdown(
                        id="drop_categories", multi=True,
                        options=get_options(DFS[c.dfs.TRANS][c.cols.CATEGORY].unique())
                    ),
                    className="w3-col l11 m10 s8",
                    style={
                        "padding-top": "14px",
                        "padding-bottom": "14px",
                        "padding-left": "16px",
                        "padding-right": "16px",
                    }
                )
            ],
            id="filters",
            className="w3-row w3-card",
            style=c.dash.SHOW_DICT(False)
        ),

        # Body
        html.Div(id="body"),

        # Others
        html.Div(id="sync_count", style={"display": "none"}),
        dcc.Location(id='url', refresh=False),
    ])
